#!/usr/bin/env python3
"""Remove Meta/Facebook Pixel (fbq, fbevents.js, facebook.com/tr) from PHP templates."""

import argparse
import re
import sys
from pathlib import Path

PIXEL_BLOCK = re.compile(
    r"<!--\s*Facebook\s+Pixel\s+Code\s*-->.*?<!--\s*End\s+Facebook\s+Pixel\s+Code\s*-->",
    re.IGNORECASE | re.DOTALL,
)

PHP_REQUEST_PIXEL = re.compile(
    r"<\?php\s+if\s*\(\s*\$temp\s*\[\s*['\"]page['\"]\s*\]\s*==\s*['\"]request['\"]\s*\)\s*:\s*\?>"
    r".*?<!--\s*End\s+Facebook\s+Pixel\s+Code\s*-->\s*"
    r"<\?php\s+endif\s*\?>",
    re.IGNORECASE | re.DOTALL,
)

FBQ_LINE = re.compile(r"^.*\bfbq\s*\(.*$", re.MULTILINE)
FBE_EVENTS = re.compile(
    r"<script[^>]*>.*?connect\.facebook\.net/en_US/fbevents\.js.*?</script>",
    re.IGNORECASE | re.DOTALL,
)
FB_NOSCRIPT = re.compile(
    r"<noscript>\s*<img[^>]+facebook\.com/tr[^>]*>\s*</noscript>",
    re.IGNORECASE | re.DOTALL,
)
FB_SDK_LOADER = re.compile(
    r"<!--\s*Load\s+Facebook\s+SDK.*?connect\.facebook\.net.*?-->",
    re.IGNORECASE | re.DOTALL,
)

DEFAULT_REL_PATHS = [
    "template/main.php",
    "reg-tov-znak/pages/main/formHandler.php",
    "reg-tov-znak/pages/personal_data_policy/formHandler.php",
    "reg-tov-znak/pages/personal_data_policy/index.php",
    "reg-tov-znak/pages/privacy_policy/formHandler.php",
    "reg-tov-znak/pages/privacy_policy/index.php",
    "reg-tov-znak/pages/promo/formHandler.php",
]


def strip_content(text):
    text = PIXEL_BLOCK.sub("", text)
    text = PHP_REQUEST_PIXEL.sub("", text)
    text = FBE_EVENTS.sub("", text)
    text = FB_NOSCRIPT.sub("", text)
    text = FB_SDK_LOADER.sub("", text)
    text = FBQ_LINE.sub("", text)
    # Standalone noscript pixel img
    text = re.sub(
        r"<noscript>\s*<img[^>]*facebook\.com/tr[^>]*>\s*</noscript>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return text


def process_file(path, dry_run=False):
    path = Path(path)
    if not path.is_file():
        return {"path": str(path), "skipped": True, "reason": "missing"}
    original = path.read_text(encoding="utf-8", errors="replace")
    cleaned = strip_content(original)
    changed = cleaned != original
    if changed and not dry_run:
        path.write_text(cleaned, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "removed_fbq": original.count("fbq") - cleaned.count("fbq"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docroot", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("extra", nargs="*", help="Additional relative paths under docroot")
    args = ap.parse_args()
    docroot = Path(args.docroot)
    paths = DEFAULT_REL_PATHS + list(args.extra or [])
    bad = 0
    for rel in paths:
        res = process_file(docroot / rel, dry_run=args.dry_run)
        if res.get("changed"):
            print("changed", rel)
    for rel in paths:
        p = docroot / rel
        if p.is_file():
            body = p.read_text(encoding="utf-8", errors="replace")
            if re.search(r"fbq\s*\(|fbevents\.js|facebook\.com/tr", body, re.I):
                print("FAIL still has pixel:", rel)
                bad += 1
    if bad:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
