#!/usr/bin/env python3
"""Generate memory/blog/lireate-site/llms.txt with live canonical URLs (L* + DB)."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def site_base():
    base = (os.environ.get("LIREATE_PUBLIC_SITE_URL") or "").strip().rstrip("/")
    if not base:
        raise SystemExit("LIREATE_PUBLIC_SITE_URL required")
    if not base.startswith("http"):
        base = "https://" + base
    return base


def articles_from_repo():
    out = []
    root = REPO_ROOT / "memory" / "blog" / "articles"
    for meta_path in sorted(root.glob("L*/article.meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        seo = (meta.get("lireate_seo_url") or meta.get("slug") or "").strip().strip("/")
        if not seo:
            continue
        title = (meta.get("title") or meta.get("h1") or seo)[:120]
        desc = (meta.get("description") or "")[:200]
        out.append({"seo_url": seo, "title": title, "description": desc})
    return out


def articles_from_db(docroot):
    from lireate_db_invoke import run_sitemap_urls

    res = run_sitemap_urls(docroot)
    if not res.get("ok"):
        return []
    seen = set()
    rows = []
    for row in res.get("rows") or []:
        seo = row.get("seo_url", "").strip()
        if not seo or seo in seen:
            continue
        seen.add(seo)
        rows.append({"seo_url": seo, "title": seo.replace("_", " ")[:80], "description": ""})
    return rows


def build_llms(entries, base):
    lines = [
        "# Lireate — юридический блог",
        "> Материалы по товарным знакам, патентам и защите бренда.",
        "",
        "## Blog Articles",
        "",
    ]
    for e in sorted(entries, key=lambda x: x["seo_url"]):
        url = "{0}/{1}/".format(base, e["seo_url"])
        desc = e.get("description") or ""
        lines.append("- [{0}]({1}): {2}".format(e["title"], url, desc))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docroot", type=Path, default=None)
    ap.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "memory/blog/lireate-site/llms.txt",
    )
    args = ap.parse_args()
    base = site_base()
    by_seo = {}
    for a in articles_from_repo():
        by_seo[a["seo_url"]] = a
    if args.docroot:
        for a in articles_from_db(args.docroot):
            by_seo.setdefault(a["seo_url"], a)
    text = build_llms(list(by_seo.values()), base)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print("wrote", args.out, "entries", len(by_seo))


if __name__ == "__main__":
    main()
