#!/usr/bin/env python3
"""Parse GROK SEO table (section 3) into JSON for lireate_blog_seo_apply.php."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROW_RE = re.compile(
    r"^\|\s*/(?P<slug>[^|]+?)/\s*\|\s*(?P<date>[^|]+?)\s*\|\s*(?P<cur_title>[^|]+?)\s*\|\s*(?P<new_title>[^|]+?)\s*\|\s*(?P<new_desc>[^|]+?)\s*\|\s*(?P<cluster>[^|]+?)\s*\|\s*(?P<action>[^|]+?)\s*\|$"
)


def parse_markdown(md_text):
    rows = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line.startswith("| /"):
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        slug = m.group("slug").strip()
        new_title = m.group("new_title").strip()
        cur_title = m.group("cur_title").strip()
        keep = new_title == cur_title or "Сохранить Title" in m.group("action")
        if keep:
            seo_title = None
        else:
            seo_title = new_title
        name_h1 = None
        if "исправить заголовок" in m.group("action").lower() or "title" in m.group("action").lower():
            if seo_title:
                name_h1 = seo_title
        rows.append(
            {
                "seo_url": slug,
                "cluster": m.group("cluster").strip(),
                "current_title_hint": cur_title,
                "seo_title": seo_title,
                "seo_description": m.group("new_desc").strip(),
                "name": name_h1,
                "notes": m.group("action").strip(),
                "publication_date_hint": m.group("date").strip(),
            }
        )
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    data = parse_markdown(args.markdown.read_text(encoding="utf-8"))
    payload = {"version": 1, "source": str(args.markdown), "articles": data}
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("articles", len(data))


if __name__ == "__main__":
    main()