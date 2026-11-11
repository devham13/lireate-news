#!/usr/bin/env python3
"""Снять служебные пометки из news.full_story на хостинге (все seo_url, включая legacy-дубли)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from lireate_article_strip_internal_markers import STRIP_RES, DATE_ONLY  # noqa: E402

MARKER_RX = re.compile(
    r"MCP\s+недоступен|среде\s+подготовки|среде\s+исследования|research-notes",
    re.I,
)


def strip_html(text: str) -> str:
    out = text
    for rx in STRIP_RES:
        out = rx.sub("", out)
    out = DATE_ONLY.sub(r"\1 сверка с официальными источниками на \2.", out)
    return re.sub(r"  +", " ", out)


def php_load(docroot: str) -> list[dict]:
    code = r"""
require $argv[1].'/data/db.php';
$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME);
$m->set_charset('utf8mb4');
$rows=[];
$r=$m->query("SELECT id, seo_url, full_story FROM news WHERE active=1 AND full_story<>''");
while ($row=$r->fetch_assoc()) $rows[]=$row;
echo json_encode($rows, JSON_UNESCAPED_UNICODE);
"""
    proc = subprocess.run(
        ["php", "-r", code, docroot],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    return json.loads(proc.stdout)


def php_save(docroot: str, updates: list[dict]) -> dict:
    raw = json.dumps({"updates": updates}, ensure_ascii=False)
    code = r"""
require $argv[1].'/data/db.php';
$data=json_decode(file_get_contents('php://stdin'), true);
$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME);
$m->set_charset('utf8mb4');
$n=0;
foreach ($data['updates'] as $row) {
  $st=$m->prepare('UPDATE news SET full_story=? WHERE id=?');
  $st->bind_param('si', $row['full_story'], $row['id']);
  $st->execute();
  if ($st->affected_rows>0) $n++;
}
echo json_encode(['updated'=>$n]);
"""
    proc = subprocess.run(
        ["php", "-r", code, docroot],
        input=raw,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    return json.loads(proc.stdout)


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--docroot", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    rows = php_load(args.docroot)
    updates = []
    touched = []
    for row in rows:
        if not MARKER_RX.search(row["full_story"]):
            continue
        new_body = strip_html(row["full_story"])
        if new_body != row["full_story"]:
            updates.append({"id": row["id"], "full_story": new_body, "seo_url": row["seo_url"]})
            touched.append(row["seo_url"])
    print(json.dumps({"candidates": len(touched), "urls": touched}, ensure_ascii=False, indent=2))
    if args.dry_run or not updates:
        return 0
    stats = php_save(args.docroot, updates)
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
