#!/usr/bin/env python3
"""Suggest next cover_style for a Lireate topic (Python 3.6+)."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lireate_cover_style_check import BANNED_NEW, collect_history, load_registry, repo_root


def pick_style(root, topic_id):
    registry = load_registry(root)
    styles = [s for s in registry.get("styles") or [] if s["style_id"] not in BANNED_NEW]
    history, _ = collect_history(root, exclude_topic=topic_id)
    blocked_styles = {h["style_id"] for h in history[-3:]}
    prev_caption = history[-1].get("caption_layout_id") if history else None

    for s in styles:
        sid = s["style_id"]
        if sid in blocked_styles:
            continue
        cap = s.get("default_caption_layout_id")
        if prev_caption and cap == prev_caption:
            continue
        hero = s.get("hero_present")
        if hero == "optional":
            hero_present = True
        else:
            hero_present = bool(hero)
        return {
            "topic_id": topic_id.upper(),
            "style_id": sid,
            "layout_id": sid + "_layout",
            "caption_layout_id": cap,
            "palette_id": s.get("default_palette_id"),
            "hero_present": hero_present,
        }
    raise SystemExit("no available style after rotation rules")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic-id", required=True)
    ap.add_argument("--write-meta", type=Path, help="Merge cover_style into article.meta.json")
    args = ap.parse_args()
    root = repo_root()
    picked = pick_style(root, args.topic_id)
    print(json.dumps(picked, ensure_ascii=False, indent=2))
    if args.write_meta:
        path = Path(args.write_meta)
        meta = json.loads(path.read_text(encoding="utf-8"))
        meta["cover_style"] = picked
        path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("OK wrote cover_style to", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
