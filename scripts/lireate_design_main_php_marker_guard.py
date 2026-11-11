#!/usr/bin/env python3
"""After main.php patch: every lireate_design_* marker present before must remain."""
import re
import sys
from pathlib import Path

MARKER_RES = (
    r"lireate_design_[a-z0-9_]+_v\d+",
    r"lireate_cms_dark_body_v1",
    r"lireate_cms_dark_pages_v2",
    r"lireate_mktu_lu_body_v1",
)


def extract_markers(text):
    found = set()
    for pat in MARKER_RES:
        found.update(re.findall(pat, text))
    return found


def home_dark_present(text):
    return "lireate-home-dark" in text and "$temp['page']" in text


def legacy_cms_body_present(text):
    if "/* lireate_design_legacy_cms_services_v1 body */" in text:
        return "lireate-legacy-cms-lu" in text
    if "lireate_design_legacy_cms_services_v1" in text and "lireate-legacy-cms-lu" in text:
        return True
    return False


def check_preserved(before, after):
    errors = []
    bm = extract_markers(before)
    am = extract_markers(after)
    missing = sorted(bm - am)
    if missing:
        errors.append("missing markers: " + ", ".join(missing))
    if home_dark_present(before) and not home_dark_present(after):
        errors.append("lireate-home-dark body echo missing")
    if legacy_cms_body_present(before) and not legacy_cms_body_present(after):
        errors.append("lireate-legacy-cms-lu body echo missing")
    if "page_container" in before and "page_container" not in after:
        errors.append("page_container missing")
    if len(after) < len(before) - 2000:
        errors.append("suspicious shrink: %d -> %d bytes" % (len(before), len(after)))
    return errors


def main():
    if len(sys.argv) != 3:
        print("Usage: %s BEFORE_MAIN AFTER_MAIN" % sys.argv[0], file=sys.stderr)
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
