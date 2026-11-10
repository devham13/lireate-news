#!/usr/bin/env python3
"""Inject contextual links + «Читайте также» tail for legacy news articles."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHP_PUBLISH = REPO / "scripts" / "lireate_db_publish.php"

MARKER = 'data-lireate-read-also="1"'
BLOCK_HEADING = "<h2>Читайте также</h2>"

TARGET_INBOUND = {
    "kak_podat_zayavku_po_madridskoy_sisteme_iz_rossii_poshlinyi_i_poryadok": [
        (
            "mezhdunarodnaja_registracija_tovarnogo_znaka",
            "Международная регистрация товарного знака",
        ),
        (
            "zatratyi_na_registraciyu_brenda_po_madridskoy_sisteme",
            "затраты на регистрацию по Мадридской системе",
        ),
        (
            "kak_podat_mezhdunarodnuyu_zayavku_po_madridskoy_sisteme_iz_rossii_poshlinyi_i_poryadok",
            "международную заявку по Мадридской системе",
        ),
    ],
    "kak_podat_isk_o_neispolzovanii_tovarnogo_znaka_st_1486_i_sip": [
        (
            "dosrochnoe_prekraschenie_tovarnogo_znaka_za_neispolzovanie_kak_rabotaet_3letnee_pravilo_na_praktike",
            "досрочное прекращение за неиспользование",
        ),
        (
            "dosrochnoe_prekraschenie_registracii_tovarnogo_znaka_v_rossii_pravovyie_aspektyi_i_procedura",
            "правовые аспекты досрочного прекращения",
        ),
        (
            "vozrazhenie_protiv_registracii_chuzhogo_tovarnogo_znaka_sroki_i_poryadok",
            "возражение против регистрации чужого знака",
        ),
    ],
}


def run_php_rows(docroot: str) -> list[dict]:
    code = r"""
require $argv[1].'/data/db.php';
$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME);
$r=$m->query("SELECT id, seo_url, name, full_story, category, datetime FROM news WHERE active=1 ORDER BY id");
$out=[];
while($row=$r->fetch_assoc()) $out[]=$row;
echo json_encode($out, JSON_UNESCAPED_UNICODE);
"""
    proc = subprocess.run(
        ["php", "-r", code, docroot],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise RuntimeError("php query failed")
    return json.loads(proc.stdout)


def tokenize(text: str) -> Counter:
    text = re.sub(r"<[^>]+>", " ", text.lower())
    words = re.findall(r"[а-яёa-z0-9]{4,}", text, flags=re.I)
    stop = {"этого", "которые", "товар", "знака", "можно", "нужно", "россии", "статьи", "лирейт"}
    return Counter(w for w in words if w not in stop)


def has_internal_link(html: str) -> bool:
    return bool(re.search(r'<a\s+[^>]*href="/[a-z0-9_\-]+/?"', html, flags=re.I))


def inject_inbound(rows: list[dict]) -> list[str]:
    by_slug = {r["seo_url"]: r for r in rows}
    changed: list[str] = []
    for target, sources in TARGET_INBOUND.items():
        if target not in by_slug:
            continue
        for src_slug, anchor in sources:
            src = by_slug.get(src_slug)
            if not src:
                continue
            url = f"/{target}/"
            if url in src["full_story"]:
                continue
            insert = f' <a href="{url}">{anchor}</a>.'
            # after first </p>
            body = src["full_story"]
            new_body = re.sub(r"(</p>)", r"\1" + insert, body, count=1, flags=re.I)
            if new_body == body:
                new_body = body + f"<p>Материал по теме: <a href=\"{url}\">{anchor}</a>.</p>"
            src["full_story"] = new_body
            changed.append(src_slug)
    return changed


def related_block(article: dict, pool: list[dict], n: int = 3) -> str:
    tokens = tokenize(article.get("name", "") + " " + article.get("full_story", ""))
    scores: list[tuple[float, dict]] = []
    for other in pool:
        if other["id"] == article["id"]:
            continue
        if other["seo_url"] == article["seo_url"]:
            continue
        score = sum(tokens[t] for t in tokenize(other.get("name", "")))
        if article.get("category") and other.get("category") == article["category"]:
            score += 3
        if score > 0:
            scores.append((score, other))
    scores.sort(key=lambda x: -x[0])
    picks = [x[1] for x in scores[:n]]
    if len(picks) < n:
        return ""
    lis = []
    for pick in picks:
        url = f"/{pick['seo_url']}/"
        title = pick["name"]
        lis.append(f'<li><a href="{url}">{title}</a></li>')
    return (
        f'<section class="lireate-read-also" {MARKER}>'
        f"{BLOCK_HEADING}<ul>{''.join(lis)}</ul></section>"
    )


def apply_read_also(rows: list[dict]) -> list[str]:
    changed: list[str] = []
    legacy = [r for r in rows if not r["seo_url"].startswith("kak_") or True]
    for row in rows:
        body = row["full_story"] or ""
        if MARKER in body:
            continue
        if has_internal_link(body):
            continue
        if "lireate-blog" in body or "lx-article-cover" in body:
            continue
        block = related_block(row, rows, 3)
        if not block:
            continue
        row["full_story"] = body.rstrip() + "\n" + block
        changed.append(row["seo_url"])
    return changed


def backup_news(docroot: str, out_path: Path) -> None:
    require = docroot + "/data/db.php"
    subprocess.run(
        [
            "bash",
            "-lc",
            f"php -r 'require \"{require}\";' 2>/dev/null; "
            f"mysqldump -h\"$DB_SERVER\" -u\"$DB_USER\" -p\"$DB_PASS\" \"$DB_NAME\" news > '{out_path}'",
        ],
        check=False,
    )


def push_updates(docroot: str, rows: list[dict], changed_slugs: set[str]) -> None:
    by_slug = {r["seo_url"]: r for r in rows}
    for slug in changed_slugs:
        row = by_slug[slug]
        code = r"""
require $argv[1].'/data/db.php';
$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME);
$id=(int)$argv[2];
$body=file_get_contents($argv[3]);
$st=$m->prepare('UPDATE news SET full_story=? WHERE id=?');
$st->bind_param('si',$body,$id);
$st->execute();
"""
        tmp = Path("/tmp/lireate_body_" + slug + ".html")
        tmp.write_text(row["full_story"], encoding="utf-8")
        subprocess.run(
            ["php", "-r", code, docroot, str(row["id"]), str(tmp)],
            check=True,
        )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docroot", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup", default="")
    args = ap.parse_args()
    rows = run_php_rows(args.docroot)
    if args.backup:
        backup_news(args.docroot, Path(args.backup))
    inbound_changed = inject_inbound(rows)
    read_changed = apply_read_also(rows)
    all_changed = set(read_changed) | set(inbound_changed)
    report = {
        "inbound_targets": list(TARGET_INBOUND.keys()),
        "read_also_articles": len(read_changed),
        "sample_read_also": read_changed[:15],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.apply and all_changed:
        push_updates(args.docroot, rows, all_changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
