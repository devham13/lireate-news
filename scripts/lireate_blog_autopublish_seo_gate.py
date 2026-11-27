#!/usr/bin/env python3
"""Stricter SEO gate before hosting publish (no live publish)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from lireate_publish_meta_validate import validate_article_meta

_TITLE_MAX = 60
_DESC_MIN = 120
_DESC_MAX = 160
_L_MARKER = re.compile(r"\bL\d{2}\b", re.I)


def _block(errors):
    print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False))
    return 1


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: lireate_blog_autopublish_seo_gate.py article.meta.json article.html", file=sys.stderr)
        return 2
    meta = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    html = Path(sys.argv[2]).read_text(encoding="utf-8", errors="replace")
    errors = validate_article_meta(meta, html)
    title = (meta.get("seo_title") or meta.get("title") or "").strip()
    desc = (meta.get("description") or "").strip()
    if len(title) > _TITLE_MAX:
        errors.append("seo_title over {0} chars".format(_TITLE_MAX))
    if len(desc) < _DESC_MIN or len(desc) > _DESC_MAX:
        errors.append("description must be {0}-{1} chars".format(_DESC_MIN, _DESC_MAX))
    if _L_MARKER.search(title + " " + desc):
        errors.append("internal Lxx marker in meta")
    if errors:
        return _block(errors)
    print(json.dumps({"ok": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())