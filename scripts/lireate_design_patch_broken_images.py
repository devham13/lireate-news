#!/usr/bin/env python3
"""Defer lireate-broken-images.js site-wide (hide 404 imgs without touching DB)."""
import subprocess
import sys
from pathlib import Path

MARK = "lireate_design_broken_images_v1"
MIN_LINES = 6000

SNIP = f'\t<script defer src="/template/js/lireate-broken-images.js?v=20261111img1"></script>\n\t<?php /* {MARK} */ ?>\n'


def _php_lint(content: str) -> None:
    tmp = Path("/tmp/lireate-main-php-broken-img.php")
    tmp.write_text(content, encoding="utf-8")
    r = subprocess.run(
        ["php", "-l", str(tmp)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if r.returncode != 0:
        raise SystemExit(r.stderr or r.stdout)


def patch(text: str) -> str:
    if text.count("\n") + 1 < MIN_LINES:
        raise SystemExit("main.php too short")
    if MARK in text or "lireate-broken-images.js" in text:
        return text
    if "</body>" in text:
        return text.replace("</body>", SNIP + "</body>", 1)
    raise SystemExit("</body> missing")


def main() -> None:
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw)
    if out == raw:
        print("UNCHANGED")
        return
    _php_lint(out)
    path.write_text(out, encoding="utf-8")
    print("BROKEN_IMAGES_PATCH_OK")


if __name__ == "__main__":
    main()
