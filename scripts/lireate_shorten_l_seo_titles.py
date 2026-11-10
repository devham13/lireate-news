#!/usr/bin/env python3
"""Shorten L* article.meta.json title/seo to <=70 chars (keep keyword prefix)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MAX_LEN = 70


def pick_title(meta):
    ab = meta.get("meta_ab") or {}
    for key in ("title_seo", "title_aeo", "title_ctr"):
        t = (ab.get(key) or "").strip()
        if t and len(t) <= MAX_LEN:
            return t
    t = (meta.get("title") or meta.get("h1") or "").strip()
    if len(t) <= MAX_LEN:
        return t
    cut = t[: MAX_LEN - 1].rstrip(" ,.-:;")
    return cut + "…" if len(t) > MAX_LEN else t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--articles-root", type=Path, default=REPO_ROOT / "memory/blog/articles")
    args = ap.parse_args()
    changed = 0
    for meta_path in sorted(args.articles_root.glob("L*/article.meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        old = meta.get("title", "")
        if len(old) <= MAX_LEN:
            continue
        new = pick_title(meta)
        if new == old:
            continue
        print(meta_path.parent.name, len(old), "->", len(new), new[:50])
        meta["title"] = new
        if not args.dry_run:
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed += 1
    print("changed", changed)


if __name__ == "__main__":
    main()
