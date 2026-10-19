#!/usr/bin/env python3
"""Render inline collage-v1 illustrations from cover/inline-specs.json."""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_collage.constants import INLINE_OUT, INLINE_RENDER, SLOT_FILES  # noqa: E402
from lireate_collage.eligibility import collage_allowed  # noqa: E402
from lireate_collage.inline_html import build_inline_html  # noqa: E402
from lireate_collage.render import render_html_to_png, resize_png  # noqa: E402
from lireate_collage.validate import validate_inline_item  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path, required=True)
    ap.add_argument("--spec", type=Path, help="inline-specs.json path")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out-dir", type=Path)
    args = ap.parse_args()

    article_dir = args.article_dir.resolve()
    if not args.force:
        ok, reason = collage_allowed(article_dir)
        if not ok:
            print("INLINE_BLOCKER: {0}".format(reason))
            return 2

    spec_path = args.spec or (article_dir / "cover" / "inline-specs.json")
    if not spec_path.is_file():
        print("INLINE_SKIP: no inline-specs.json")
        return 0

    doc = json.loads(spec_path.read_text(encoding="utf-8"))
    if doc.get("style") != "collage-v1":
        print("INLINE_BLOCKER: style must be collage-v1")
        return 2

    cover_dir = args.out_dir or (article_dir / "cover")
    cover_dir.mkdir(parents=True, exist_ok=True)
    w, h = INLINE_RENDER

    for item in doc.get("illustrations") or []:
        errs = validate_inline_item(item)
        if errs:
            print("INLINE_BLOCKER:", item.get("slot"), errs)
            return 2
        slot = item.get("slot") or "inline_1"
        fname = SLOT_FILES.get(slot)
        if not fname:
            print("INLINE_BLOCKER: bad slot", slot)
            return 2
        html = build_inline_html(item, w, h)
        raw = cover_dir / ("collage-inline-raw-{0}.png".format(slot))
        try:
            render_html_to_png(html, w, h, raw, layout_check=True, fit=False)
        except RuntimeError as e:
            print("INLINE_BLOCKER:", e)
            return 2
        resize_png(raw, cover_dir / fname, INLINE_OUT)
        (cover_dir / ("inline-{0}-template.html".format(slot))).write_text(html, encoding="utf-8")

    print("OK inline collage", len(doc.get("illustrations") or []), "files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
