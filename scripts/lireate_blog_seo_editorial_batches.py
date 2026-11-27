#!/usr/bin/env python3
"""Split news export into editorial batches for human/LLM meta writing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BATCH = 45


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--needs-fix-only", action="store_true", help="skip rows already in SERP range")
    ap.add_argument("--slug-list", type=Path, default=None)
    args = ap.parse_args()
    data = json.loads(args.export.read_text(encoding="utf-8"))
    articles = data.get("articles") or []
    if args.slug_list and args.slug_list.is_file():
        want = {
            ln.strip().strip("/")
            for ln in args.slug_list.read_text(encoding="utf-8").splitlines()
            if ln.strip()
        }
        articles = [a for a in articles if (a.get("seo_url") or "").strip("/") in want]

    def needs(a: dict) -> bool:
        if not args.needs_fix_only:
            return True
        t = (a.get("seo_title") or "").strip()
        d = (a.get("seo_description") or "").strip()
        if len(t) > 60 or len(d) > 160 or len(d) < 120:
            return True
        if d and d[-1] not in ".!?":
            return True
        return False

    filtered = [a for a in articles if needs(a)]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    batches = []
    for i in range(0, len(filtered), BATCH):
        chunk = filtered[i : i + BATCH]
        idx = i // BATCH + 1
        path = args.out_dir / "batch-{0:02d}.json".format(idx)
        path.write_text(
            json.dumps({"batch": idx, "articles": chunk}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        batches.append((idx, path, len(chunk)))
    manifest = {"batches": batches, "total_articles": len(filtered)}
    (args.out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("batches={0} articles={1}".format(len(batches), len(filtered)))


if __name__ == "__main__":
    main()