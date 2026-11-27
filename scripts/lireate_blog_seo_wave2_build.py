#!/usr/bin/env python3
"""DEPRECATED: mechanical truncate plan. Use editorial batches + meta_plan_validate instead.

Build wave2 SEO plan from MySQL export + optional live audit CSV.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

# Reuse truncation rules from lireate repo when available.
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lireate_meta_text import normalize_seo_description, normalize_seo_title

_PROPER_END = re.compile(r'[.!?:»"\u201d\u2026…)\]]$')


def has_proper_ending(text: str) -> bool:
    s = (text or "").rstrip()
    return bool(s and _PROPER_END.search(s))


_MANUAL = {
    "ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu": {
        "seo_description": (
            "Чем отличается формальная и содержательная экспертиза товарного знака: "
            "этапы, типичные замечания Роспатента и как подготовить материалы к ответу."
        ),
        "notes": "Исправить опечатку «существовая», убрать Workflow, нормализовать стиль.",
    },
    "skolko_stoit_registraciya_avtorskogo_prava_na_elektronnyie_kartinki": {
        "seo_description": (
            "Сколько стоит оформить авторское право на электронные иллюстрации: "
            "способы депонирования, сроки и что влияет на стоимость."
        ),
    },
    "oformlenie_tovarnogo_znaka_s_patentnyim_poverennyim_argumentyi_za": {
        "seo_description": (
            "Зачем при оформлении товарного знака подключать патентного поверенного: "
            "этапы, риски и когда самостоятельная подача оправдана."
        ),
    },
    "opredelyam_raznicu_mezhdu_patentom_tovarnyim_znakom_i_avtorskim_pravom": {
        "seo_description": (
            "Патент, товарный знак и авторское право: чем отличаются объекты, "
            "сроки охраны и что выбрать для защиты продукта или бренда."
        ),
    },
    "promyshlennyy-obrazec-ili-tovarnyy-znak-dizayn-tovara": {
        "seo_description": (
            "Промышленный образец или товарный знак для дизайна товара: "
            "сравнение охраны, сроки и когда нужны обе регистрации."
        ),
        "notes": "Цифры госпошлины — только если подтверждены в теле статьи.",
    },
}


def _slug(url_or_slug: str) -> str:
    s = (url_or_slug or "").strip().strip("/")
    if "://" in s:
        s = s.rsplit("/", 1)[-1]
    return s


def _needs_fix(row: dict) -> bool:
    tlen = len((row.get("seo_title") or "").strip())
    dlen = len((row.get("seo_description") or "").strip())
    if tlen > 60 or not row.get("seo_title"):
        return True
    if dlen < 120 or dlen > 160:
        return True
    if dlen and not has_proper_ending(row["seo_description"]):
        return True
    return False


def _propose(row: dict) -> dict:
    slug = _slug(row.get("seo_url", ""))
    out = {"seo_url": slug}
    manual = _MANUAL.get(slug, {})
    if manual.get("seo_description"):
        out["seo_description"] = manual["seo_description"]
    else:
        base = (row.get("seo_description") or row.get("name") or "").strip()
        out["seo_description"] = normalize_seo_description(base, max_len=160, ellipsis=".")
    title = (row.get("seo_title") or row.get("name") or "").strip()
    if len(title) > 60 or not title:
        out["seo_title"] = normalize_seo_title(title, max_len=60)
    elif title:
        out["seo_title"] = title
    if manual.get("notes"):
        out["notes"] = manual["notes"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", type=Path, required=True)
    ap.add_argument("--out-json", type=Path, required=True)
    ap.add_argument("--out-md", type=Path, required=True)
    ap.add_argument("--audit", type=Path, default=None, help="optional live crawl CSV")
    args = ap.parse_args()

    data = json.loads(args.export.read_text(encoding="utf-8"))
    audit_by_slug = {}
    if args.audit and args.audit.is_file():
        with args.audit.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                audit_by_slug[_slug(row.get("url", ""))] = row

    articles = []
    md_lines = [
        "# Wave 2 — предложения meta (только `news`, без правок `full_story`)",
        "",
    ]
    for row in data.get("articles", []):
        if not _needs_fix(row):
            continue
        prop = _propose(row)
        live = audit_by_slug.get(_slug(row.get("seo_url", "")), {})
        prop["current_seo_title"] = row.get("seo_title", "")
        prop["current_seo_description"] = row.get("seo_description", "")
        if live:
            prop["live_meta_description_len"] = live.get("meta_description_len", "")
            prop["live_issue_flags"] = live.get("issue_flags", "")
        articles.append(prop)
        md_lines.append("## `{}`".format(prop["seo_url"]))
        md_lines.append("- **title (DB):** {}".format(row.get("seo_title", "")[:80]))
        md_lines.append("- **description (DB):** {}…".format((row.get("seo_description") or "")[:100]))
        if live.get("meta_description_len"):
            md_lines.append(
                "- **live description len:** {}".format(live.get("meta_description_len"))
            )
        md_lines.append("- **proposed title:** {}".format(prop.get("seo_title", "")))
        md_lines.append("- **proposed description:** {}".format(prop.get("seo_description", "")))
        if prop.get("notes"):
            md_lines.append("- **notes:** {}".format(prop["notes"]))
        md_lines.append("")

    plan = {
        "version": 2,
        "source_export": str(args.export),
        "articles": [{k: v for k, v in a.items() if not k.startswith("current_") and not k.startswith("live_")} for a in articles],
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print("needs_fix={0} wrote={1}".format(len(articles), args.out_json))


if __name__ == "__main__":
    main()