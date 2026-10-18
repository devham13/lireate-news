#!/usr/bin/env python3
"""Pick cover_era for Lireate topic (no repeat in last 10)."""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lireate_cover_era_check import WINDOW, collect_eras, repo_root


def load_era_list(root):
    path = root / "memory/blog/cover-action-selfie.md"
    text = path.read_text(encoding="utf-8")
    m = re.search(r"## ERA LIST\s*\n(.+)", text, re.DOTALL)
    if not m:
        raise SystemExit("ERA LIST not found in cover-action-selfie.md")
    block = m.group(1)
    eras = []
    for part in re.split(r"[;\n]", block):
        era = part.strip().strip(".")
        if era and not era.startswith("#"):
            eras.append(era)
    return eras


def pick_era(root, topic_id):
    all_eras = load_era_list(root)
    history = collect_eras(root, exclude_topic=topic_id)
    blocked = {h["cover_era"] for h in history[-WINDOW:]}
    for era in all_eras:
        if era not in blocked:
            return era
    raise SystemExit("no available cover_era after rotation window")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic-id", required=True)
    ap.add_argument("--write-meta", type=Path)
    args = ap.parse_args()
    root = repo_root()
    era = pick_era(root, args.topic_id)
    out = {"topic_id": args.topic_id.upper(), "cover_era": era}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if args.write_meta:
        meta = json.loads(Path(args.write_meta).read_text(encoding="utf-8"))
        meta["cover_era"] = era
        Path(args.write_meta).write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("OK wrote cover_era to", args.write_meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
