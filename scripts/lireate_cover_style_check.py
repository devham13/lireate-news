#!/usr/bin/env python3
"""Validate Lireate cover style rotation (Python 3.6+)."""

import argparse
import json
import re
import sys
from pathlib import Path

LEGACY_STYLE = "legacy_hero_left_doc_card"
BANNED_NEW = {LEGACY_STYLE}


def repo_root():
    return Path(__file__).resolve().parents[1]


def load_registry(root):
    path = root / "memory/blog/cover-style-registry.json"
    if not path.is_file():
        raise SystemExit("missing cover-style-registry.json")
    return json.loads(path.read_text(encoding="utf-8"))


def lireate_article_dirs(root):
    base = root / "memory/blog/articles"
    if not base.is_dir():
        return []
    out = []
    for p in sorted(base.iterdir()):
        m = re.match(r"^(L\d+)-", p.name)
        if p.is_dir() and m:
            out.append((int(m.group(1)[1:]), m.group(1).upper(), p))
    out.sort(key=lambda x: x[0])
    return out


def read_cover_style(article_dir):
    meta_path = article_dir / "article.meta.json"
    if not meta_path.is_file():
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    cs = meta.get("cover_style")
    if not cs or not cs.get("style_id"):
        return None
    return cs


def validate_style(cs, history, registry_ids, strict_rotation=True):
    errors = []
    style_id = cs.get("style_id")
    caption_layout = cs.get("caption_layout_id")
    topic = cs.get("topic_id", "?")

    if style_id not in registry_ids:
        errors.append("unknown style_id: {0}".format(style_id))
    if style_id in BANNED_NEW and topic not in ("L01", "L02"):
        errors.append("style_id {0} is deprecated for new articles".format(style_id))

    if strict_rotation and style_id != LEGACY_STYLE:
        recent_styles = [h["style_id"] for h in history[-3:] if h.get("style_id") != LEGACY_STYLE]
        if style_id in recent_styles:
            errors.append(
                "style_id {0} repeats within last 3 non-legacy L-articles: {1}".format(
                    style_id, recent_styles
                )
            )
        if history:
            prev = history[-1]
            if (
                caption_layout
                and prev.get("caption_layout_id") == caption_layout
                and prev.get("style_id") != LEGACY_STYLE
            ):
                errors.append(
                    "caption_layout_id {0} repeats previous article {1}".format(
                        caption_layout, prev.get("topic_id")
                    )
                )
    return errors


def collect_history(root, exclude_topic=None):
    registry = load_registry(root)
    registry_ids = {s["style_id"] for s in registry.get("styles") or []}
    history = []
    for _num, tid, adir in lireate_article_dirs(root):
        if exclude_topic and tid == exclude_topic.upper():
            continue
        cs = read_cover_style(adir)
        if cs:
            entry = dict(cs)
            entry.setdefault("topic_id", tid)
            history.append(entry)
    return history, registry_ids


def check_article_dir(root, article_dir):
    article_dir = Path(article_dir)
    meta_path = article_dir / "article.meta.json"
    if not meta_path.is_file():
        return ["article.meta.json missing"]
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    topic = (meta.get("topic_id") or "").upper()
    cs = meta.get("cover_style")
    if not cs:
        return ["cover_style missing in article.meta.json"]
    cs = dict(cs)
    cs.setdefault("topic_id", topic)
    history, registry_ids = collect_history(root, exclude_topic=topic)
    return validate_style(cs, history, registry_ids)


def check_all_lireate(root):
    errors = []
    dirs = lireate_article_dirs(root)
    for _n, tid, adir in dirs:
        cs = read_cover_style(adir)
        if not cs:
            if (adir / "cover/cover.png").is_file():
                errors.append("{0}: cover.png exists but cover_style missing in meta".format(tid))
            continue
        hist_before = []
        for _n2, tid2, adir2 in dirs:
            if tid2 == tid:
                break
            cs2 = read_cover_style(adir2)
            if cs2:
                e = dict(cs2)
                e.setdefault("topic_id", tid2)
                hist_before.append(e)
        _, registry_ids = collect_history(root)
        errors.extend(
            ["{0}: {1}".format(tid, e) for e in validate_style(cs, hist_before, registry_ids)]
        )
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path, help="Validate one article")
    ap.add_argument("--all-lireate", action="store_true", help="Validate all L* with cover_style")
    args = ap.parse_args()
    root = repo_root()
    if args.all_lireate:
        errors = check_all_lireate(root)
    elif args.article_dir:
        errors = check_article_dir(root, args.article_dir)
    else:
        ap.error("pass --article-dir or --all-lireate")
    if errors:
        print("COVER STYLE CHECK FAIL")
        for e in errors:
            print("  ERROR:", e)
        return 1
    print("OK COVER STYLE CHECK PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
