#!/usr/bin/env python3
"""Apply audit 2026-11-11 DB/content fixes on LIREATE hosting (news + pages)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def php_query(docroot: str) -> list[dict]:
    code = r"""
require $argv[1].'/data/db.php';
$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME);
if ($m->connect_errno) { fwrite(STDERR, $m->connect_error); exit(2); }
$m->set_charset('utf8mb4');
$out=['news'=>[],'pages'=>[]];
$r=$m->query('SELECT id,seo_url,full_story,seo_description FROM news WHERE active=1');
while($row=$r->fetch_assoc()) $out['news'][]=$row;
$r=$m->query('SELECT id,seo_url,full_story,seo_description FROM pages');
while($row=$r->fetch_assoc()) $out['pages'][]=$row;
echo json_encode($out, JSON_UNESCAPED_UNICODE);
"""
    proc = subprocess.run(
        ["php", "-r", code, docroot],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise RuntimeError("php query failed")
    return json.loads(proc.stdout)


def php_apply(docroot: str, payload: dict) -> dict:
    raw = json.dumps(payload, ensure_ascii=False)
    code = r"""
require $argv[1].'/data/db.php';
$data=json_decode(file_get_contents('php://stdin'), true);
$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME);
$m->set_charset('utf8mb4');
$stats=['news_updated'=>0,'pages_updated'=>0];
foreach ($data['news'] as $row) {
  $st=$m->prepare('UPDATE news SET full_story=?, seo_description=? WHERE id=?');
  $st->bind_param('ssi', $row['full_story'], $row['seo_description'], $row['id']);
  $st->execute();
  if ($st->affected_rows>=0) $stats['news_updated']++;
}
foreach ($data['pages'] as $row) {
  $st=$m->prepare('UPDATE pages SET full_story=?, seo_description=? WHERE id=?');
  $st->bind_param('ssi', $row['full_story'], $row['seo_description'], $row['id']);
  $st->execute();
  if ($st->affected_rows>=0) $stats['pages_updated']++;
}
echo json_encode($stats);
"""
    proc = subprocess.run(
        ["php", "-r", code, docroot],
        input=raw,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise RuntimeError("php apply failed")
    return json.loads(proc.stdout)


def replace_links(html: str, pairs: list[list[str]]) -> str:
    out = html
    for old, new in pairs:
        out = out.replace(old, new)
    return out


def demote_first_h1(html: str) -> str:
    return re.sub(r"(?is)<h1(\s[^>]*)?>", r"<h2\1>", html, count=1).replace(
        "</h1>", "</h2>", 1
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docroot", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    docroot = args.docroot

    meta_path = REPO / "shared" / "lireate-seo-audit-meta.json"
    links_path = REPO / "shared" / "lireate-seo-audit-link-replacements.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    links_cfg = json.loads(links_path.read_text(encoding="utf-8"))
    pairs = links_cfg.get("href_replacements") or []
    h1_slugs = set(meta.get("h1_demote_slug") or [])

    data = php_query(docroot)
    news_out = []
    pages_out = []
    changed = 0

    for row in data["news"]:
        slug = row["seo_url"]
        body = row["full_story"] or ""
        desc = row["seo_description"] or ""
        new_body = replace_links(body, pairs)
        if slug in h1_slugs:
            new_body = demote_first_h1(new_body)
        if slug in (meta.get("news") or {}):
            desc = meta["news"][slug]
        if new_body != body or desc != (row["seo_description"] or ""):
            changed += 1
            news_out.append(
                {
                    "id": row["id"],
                    "full_story": new_body,
                    "seo_description": desc,
                    "seo_url": slug,
                }
            )

    for row in data["pages"]:
        slug = row["seo_url"]
        body = row["full_story"] or ""
        desc = row["seo_description"] or ""
        new_body = replace_links(body, pairs)
        if slug in h1_slugs:
            new_body = demote_first_h1(new_body)
        if slug in (meta.get("pages") or {}):
            desc = meta["pages"][slug]
        if new_body != body or desc != (row["seo_description"] or ""):
            changed += 1
            pages_out.append(
                {
                    "id": row["id"],
                    "full_story": new_body,
                    "seo_description": desc,
                    "seo_url": slug,
                }
            )

    summary = {"rows_touched": changed, "news": len(news_out), "pages": len(pages_out)}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.dry_run or not (news_out or pages_out):
        return 0
    stats = php_apply(docroot, {"news": news_out, "pages": pages_out})
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
