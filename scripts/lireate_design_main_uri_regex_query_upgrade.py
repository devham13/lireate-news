#!/usr/bin/env python3
"""Upgrade lireate REQUEST_URI preg_match anchors to allow ?query (deploy verify)."""
import re
import sys
from pathlib import Path

MARK = "lireate_design_uri_query_safe_v1"
# (?:/|$) at end of path alternation → (?:[/?]|$) for verify/cache-bust query strings
OLD = "(?:/|$)#"
NEW = "(?:[/?]|$)#"


def patch(text):
    if MARK in text:
        return text, False
    if OLD not in text:
        return text, False
    # Only inside lireate-related preg_match / legacy URI patterns
    n = 0
    lines = []
    for line in text.splitlines(keepends=True):
        if "preg_match(" in line and (
            "lireate" in line
            or "poisk_tovarnyh" in line
            or "_lx_" in line
            or "/reviews" in line
            or "/portfolio" in line
            or "/spasibo" in line
            or "mktu" in line
            or "dogovory" in line
        ):
            line2, c = re.subn(re.escape(OLD), NEW, line)
            if c:
                n += c
            lines.append(line2)
        else:
            lines.append(line)
    if n == 0:
        return text, False
    out = "".join(lines)
    anchor = "/* lireate_cms_dark_body_v1 */"
    if anchor in out and MARK not in out:
        out = out.replace(anchor, f"/* {MARK} */ {anchor}", 1)
    return out, True


def main():
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out, changed = patch(raw)
    if not changed:
        print("UNCHANGED")
        return
    path.write_text(out, encoding="utf-8")
    print("URI_QUERY_SAFE_UPGRADE_OK")


if __name__ == "__main__":
    main()
