#!/usr/bin/env python3
"""Hard gate: L07+ articles must ship collage-v1 cover + inline before publish."""

import argparse
import json
import re
import sys
from pathlib import Path

# L06 was published with legacy KIE; collage-v1 mandatory from L07.
MIN_COLLAGE_TOPIC_NUM = 7
MIN_INLINE_FIGURES = 2


def topic_num(topic_id):
    m = re.match(r"^L(\d+)$", (topic_id or "").strip(), re.I)
    return int(m.group(1)) if m else -1


def requires_collage_v1_gate(topic_id):
    return topic_num(topic_id) >= MIN_COLLAGE_TOPIC_NUM


def _load_meta(article_dir):
    meta_path = Path(article_dir) / "article.meta.json"
    if not meta_path.is_file():
        return {}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (ValueError, TypeError):
        return {}


def _qa_passed(qa_path):
    if not qa_path.is_file():
        return False, "missing {0}".format(qa_path.name)
    text = qa_path.read_text(encoding="utf-8")
    if "FAIL:" in text or "COVER_BLOCKER" in text:
        return False, "{0} contains FAIL or COVER_BLOCKER".format(qa_path.name)
    if "PASS:" not in text:
        return False, "{0} has no PASS markers".format(qa_path.name)
    return True, ""


def validate_collage_publish(article_dir, html=None, meta=None):
    """Return list of error strings. Empty list means PASS (or gate not required)."""
    article_dir = Path(article_dir)
    meta = meta if meta is not None else _load_meta(article_dir)
    topic_id = (meta.get("topic_id") or "").strip().upper()
    if not topic_id:
        m = re.match(r"^(L\d+)", article_dir.name, re.I)
        topic_id = m.group(1).upper() if m else ""

    if not requires_collage_v1_gate(topic_id):
        return []

    errors = []
    if meta.get("cover_style") != "collage-v1":
        errors.append("meta.cover_style must be collage-v1 (got {0!r})".format(meta.get("cover_style")))

    html_path = article_dir / "article.html"
    if html is None:
        if not html_path.is_file():
            errors.append("article.html missing")
            html = ""
        else:
            html = html_path.read_text(encoding="utf-8")

    if 'class="lx-article-cover"' not in html or 'data-cover-style="collage-v1"' not in html:
        errors.append("article.html missing <figure class=\"lx-article-cover\" data-cover-style=\"collage-v1\">")

    inline_count = len(re.findall(r'<figure[^>]+class="[^"]*inline-collage', html, flags=re.I))
    if inline_count < MIN_INLINE_FIGURES:
        errors.append("need >= {0} inline-collage figures, found {1}".format(MIN_INLINE_FIGURES, inline_count))

    cover_png = article_dir / "cover" / "cover.png"
    if not cover_png.is_file():
        errors.append("missing cover/cover.png")

    qa_ok, qa_detail = _qa_passed(article_dir / "cover" / "cover-collage-qa.md")
    if not qa_ok:
        errors.append("collage QA: {0}".format(qa_detail))

    spec_path = article_dir / "cover" / "inline-specs.json"
    if not spec_path.is_file():
        errors.append("missing cover/inline-specs.json")
    else:
        try:
            doc = json.loads(spec_path.read_text(encoding="utf-8"))
        except ValueError:
            errors.append("invalid cover/inline-specs.json")
            doc = {}
        if doc.get("style") != "collage-v1":
            errors.append("inline-specs.json style must be collage-v1")
        ill = doc.get("illustrations") or []
        if len(ill) < MIN_INLINE_FIGURES:
            errors.append("inline-specs need >= {0} illustrations".format(MIN_INLINE_FIGURES))
        for item in ill:
            slot = item.get("slot") or ""
            fname = {"inline_1": "inline-01.png", "inline_2": "inline-02.png", "inline_3": "inline-03.png"}.get(
                slot
            )
            if fname and not (article_dir / "cover" / fname).is_file():
                errors.append("missing cover/{0} for slot {1}".format(fname, slot))

    if (article_dir / "cover" / "kie-raw.png").is_file() and meta.get("cover_style") != "collage-v1":
        errors.append("kie-raw.png present without collage-v1 (use lireate_collage_pipeline.py)")

    return errors


def check_article_dir(article_dir):
    return validate_collage_publish(article_dir)


def check_new_lireate_articles(root):
    """Fail if any L07+ article dir in repo violates collage gate."""
    base = Path(root) / "memory/blog/articles"
    if not base.is_dir():
        return []
    errors = []
    for p in sorted(base.iterdir()):
        m = re.match(r"^(L\d+)", p.name, re.I)
        if not p.is_dir() or not m:
            continue
        tid = m.group(1).upper()
        if not requires_collage_v1_gate(tid):
            continue
        if not (p / "article.html").is_file():
            continue
        for e in validate_collage_publish(p):
            errors.append("{0}: {1}".format(tid, e))
    return errors


def main():
    ap = argparse.ArgumentParser(description="Collage-v1 publish gate for L07+ Lireate articles")
    ap.add_argument("--article-dir", type=Path)
    ap.add_argument("--all-lireate", action="store_true", help="Check every L07+ folder under memory/blog/articles")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]

    if args.all_lireate:
        errors = check_new_lireate_articles(root)
    elif args.article_dir:
        errors = check_article_dir(args.article_dir)
    else:
        ap.error("pass --article-dir or --all-lireate")

    if errors:
        print("COLLAGE_PUBLISH_GATE FAIL")
        for e in errors:
            print("  ERROR:", e)
        return 1
    print("OK COLLAGE_PUBLISH_GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
