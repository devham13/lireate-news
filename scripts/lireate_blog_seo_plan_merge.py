#!/usr/bin/env python3
"""Merge batch editorial JSON outputs into one apply plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="batch-*-out.json")
    ap.add_argument("--in-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--version", type=int, default=2)
    args = ap.parse_args()
    articles = []
    for path in sorted(args.in_dir.glob(args.glob)):
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data.get("articles") or []:
            articles.append(
                {
                    k: v
                    for k, v in row.items()
                    if k
                    in (
                        "seo_url",
                        "seo_title",
                        "seo_description",
                        "name",
                        "notes",
                    )
                    and v
                }
            )
    plan = {
        "version": args.version,
        "source": "editorial",
        "articles": articles,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("merged", len(articles), "->", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())