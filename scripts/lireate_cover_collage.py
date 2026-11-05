#!/usr/bin/env python3
"""Render Lireate collage-v1 list cover (860x400) via HTML + Chromium."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_collage.constants import (  # noqa: E402
    COVER_OUT,
    COVER_PREVIEW,
    COVER_RENDER,
    COVER_SMALL,
)
from lireate_collage.cover_html import build_cover_html  # noqa: E402
from lireate_collage.derive import derive_cover_spec  # noqa: E402
from lireate_collage.eligibility import collage_allowed  # noqa: E402
from lireate_collage.render import render_html_to_png, resize_png  # noqa: E402
from lireate_collage.validate import validate_cover_spec  # noqa: E402


def write_registry(cover_dir, topic_id):
    data = {
        "topic_id": topic_id,
        "cover_family": "lireate_collage_v1",
        "style_preset": "collage-v1",
        "renderer": "html_chromium",
        "file": "cover/cover.png",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "assets": [],
    }
    (cover_dir / "cover-registry.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_qa(cover_dir, spec, checks):
    lines = [
        "# Cover collage-v1 QA",
        "",
        "- **cover_style:** collage-v1",
        "- **headline:** {0}".format(" / ".join(spec.get("headline_lines") or [])),
        "- **highlight:** {0}".format(spec.get("highlight") or ""),
        "",
        "## Automated",
    ]
    for c in checks:
        lines.append("- {0}".format(c))
    (cover_dir / "cover-collage-qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path, required=True)
    ap.add_argument("--spec-json", type=Path, help="Optional cover spec override")
    ap.add_argument("--force", action="store_true", help="Skip eligibility (samples only)")
    ap.add_argument("--out-dir", type=Path, help="Write PNGs elsewhere (samples)")
    args = ap.parse_args()

    article_dir = args.article_dir.resolve()
    if not args.force:
        ok, reason = collage_allowed(article_dir)
        if not ok:
            print("COVER_BLOCKER: {0}".format(reason))
            return 2

    meta_path = article_dir / "article.meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    if args.spec_json and args.spec_json.is_file():
        spec = json.loads(args.spec_json.read_text(encoding="utf-8"))
    else:
        spec = derive_cover_spec(meta)

    errors = validate_cover_spec(spec)
    if errors:
        print("COVER_BLOCKER: spec validation", errors)
        return 2

    w, h = COVER_RENDER
    html = build_cover_html(spec, w, h)
    cover_dir = args.out_dir or (article_dir / "cover")
    cover_dir.mkdir(parents=True, exist_ok=True)
    raw = cover_dir / "collage-render-raw.png"
    try:
        render_html_to_png(html, w, h, raw, layout_check=True, fit=False)
    except RuntimeError as e:
        print("COVER_BLOCKER:", e)
        return 2
    resize_png(raw, cover_dir / "cover.png", COVER_OUT)
    resize_png(raw, cover_dir / "cover-small.png", COVER_SMALL)
    resize_png(cover_dir / "cover.png", cover_dir / "cover-preview-396x300.png", COVER_PREVIEW)
    (cover_dir / "cover-spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (cover_dir / "cover-template.html").write_text(html, encoding="utf-8")

    checks = [
        "PASS: cover.png {0}".format(COVER_OUT),
        "PASS: preview 396x300",
        "PASS: thumbnail-safe center crop (layout_check)",
    ]
    write_qa(cover_dir, spec, checks)
    if not args.out_dir:
        write_registry(cover_dir, meta.get("topic_id") or "")
        meta["cover_style"] = "collage-v1"
        meta["cover_renderer"] = "html_chromium"
        meta["cover_family"] = "lireate_collage_v1"
        if not meta.get("cover_headline") and spec.get("headline_lines"):
            meta["cover_headline"] = " ".join(spec["headline_lines"])[:80]
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("OK collage cover", cover_dir / "cover.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
