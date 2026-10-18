#!/usr/bin/env python3
"""Validate Lireate cover_era rotation (last 10 articles, Python 3.6+)."""

import argparse
import json
import re
import sys
from pathlib import Path

WINDOW = 10


def repo_root():
    return Path(__file__).resolve().parents[1]


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


def read_cover_era(article_dir):
    meta_path = article_dir / "article.meta.json"
    if not meta_path.is_file():
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    era = (meta.get("cover_era") or "").strip()
    return era or None


def collect_eras(root, exclude_topic=None):
    eras = []
    for _num, tid, adir in lireate_article_dirs(root):
        if exclude_topic and tid == exclude_topic.upper():
            continue
        era = read_cover_era(adir)
        if era:
            eras.append({"topic_id": tid, "cover_era": era})
    return eras


def validate_era(era, history):
    errors = []
    if not era:
        errors.append("cover_era missing or empty")
        return errors
    recent = [h["cover_era"] for h in history[-WINDOW:]]
    if era in recent:
        errors.append(
            "cover_era {0!r} repeats within last {1} L-articles: {2}".format(
                era, WINDOW, recent
            )
        )
    return errors


def check_article_dir(root, article_dir):
    article_dir = Path(article_dir)
    meta_path = article_dir / "article.meta.json"
    if not meta_path.is_file():
        return ["article.meta.json missing"]
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    topic = (meta.get("topic_id") or "").upper()
    era = (meta.get("cover_era") or "").strip()
    has_cover = (article_dir / "cover/cover.png").is_file()
    if has_cover and not era:
        return ["cover.png exists but cover_era missing in meta"]
    history = collect_eras(root, exclude_topic=topic)
    return validate_era(era, history)


def check_all_lireate(root):
    errors = []
    dirs = lireate_article_dirs(root)
    for _n, tid, adir in dirs:
        era = read_cover_era(adir)
        if not era:
            if (adir / "cover/cover.png").is_file():
                errors.append("{0}: cover.png without cover_era".format(tid))
            continue
        hist = []
        for _n2, tid2, adir2 in dirs:
            if tid2 == tid:
                break
            e2 = read_cover_era(adir2)
            if e2:
                hist.append({"topic_id": tid2, "cover_era": e2})
        for e in validate_era(era, hist):
            errors.append("{0}: {1}".format(tid, e))
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path)
    ap.add_argument("--all-lireate", action="store_true")
    args = ap.parse_args()
    root = repo_root()
    if args.all_lireate:
        errors = check_all_lireate(root)
    elif args.article_dir:
        errors = check_article_dir(root, args.article_dir)
    else:
        ap.error("pass --article-dir or --all-lireate")
    if errors:
        print("COVER ERA CHECK FAIL")
        for e in errors:
            print("  ERROR:", e)
        return 1
    print("OK COVER ERA CHECK PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
