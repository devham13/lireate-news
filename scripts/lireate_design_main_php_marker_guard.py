#!/usr/bin/env python3
"""After main.php patch: every lireate_design_* marker present before must remain."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER_RES = (
    r"lireate_design_[a-z0-9_]+_v\d+",
    r"lireate_cms_dark_body_v1",
    r"lireate_cms_dark_pages_v2",
    r"lireate_mktu_lu_body_v1",
)


def extract_markers(text: str) -> set[str]:
    found: set[str] = set()
    for pat in MARKER_RES:
        found.update(re.findall(pat, text))
    return found


def home_dark_present(text: str) -> bool:
    return "lireate-home-dark" in text and "$temp['page']" in text


def check_preserved(before: str, after: str) -> list[str]:
    errors: list[str] = []
    bm = extract_markers(before)
    am = extract_markers(after)
    missing = sorted(bm - am)
    if missing:
        errors.append("missing markers: " + ", ".join(missing))
    if home_dark_present(before) and not home_dark_present(after):
        errors.append("lireate-home-dark body echo missing")
    if "page_container" in before and "page_container" not in after:
        errors.append("page_container missing")
    if len(after) < len(before) - 2000:
        errors.append(f"suspicious shrink: {len(before)} -> {len(after)} bytes")
    return errors


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} BEFORE_MAIN AFTER_MAIN", file=sys.stderr)
        raise SystemExit(2)
    before = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    after = Path(sys.argv[2]).read_text(encoding="utf-8", errors="replace")
    errs = check_preserved(before, after)
    if errs:
        for e in errs:
            print("MAIN_MARKER_GUARD_FAIL:", e, file=sys.stderr)
        raise SystemExit(1)
    print("MAIN_MARKER_GUARD_OK", len(extract_markers(after)))


if __name__ == "__main__":
    main()
