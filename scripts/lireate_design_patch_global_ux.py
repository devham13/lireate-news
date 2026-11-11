#!/usr/bin/env python3
"""Site-wide chat avatar-only + ux-fixes on every page (idempotent)."""
import subprocess
import sys
from pathlib import Path

MARK = "lireate_design_global_ux_v1"
MIN_LINES = 6000
PAGE_CONTAINER = "page_container"

BLOCK = f"""\t<?php /* {MARK} */ ?>
\t<link rel="stylesheet" href="/template/css/lireate-ux-fixes.css?v=20261111design5" />
\t<script defer src="/template/js/lireate-floating-widget-ux.js?v=20261111design5"></script>
"""


def _validate(text: str, label: str) -> None:
    if text.count("\n") + 1 < MIN_LINES:
        raise SystemExit(f"{label}: main.php too short")
    if PAGE_CONTAINER not in text:
        raise SystemExit(f"{label}: missing {PAGE_CONTAINER}")


def _php_lint(content: str) -> None:
    tmp = Path("/tmp/lireate-main-php-global-ux.php")
    tmp.write_text(content, encoding="utf-8")
    r = subprocess.run(
        ["php", "-l", str(tmp)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if r.returncode != 0:
        raise SystemExit(f"php -l failed: {r.stderr or r.stdout}")


def patch(text: str) -> str:
    _validate(text, "before global_ux")
    if MARK in text:
        return text
    if "lireate-ux-fixes.css" in text and "lireate-floating-widget-ux.js" in text:
        return text
    if "</head>" in text:
        text = text.replace("</head>", BLOCK + "</head>", 1)
    _validate(text, "after global_ux")
    return text


def main() -> None:
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw)
    if out == raw:
        print("UNCHANGED")
        return
    _php_lint(out)
    path.write_text(out, encoding="utf-8")
    print("GLOBAL_UX_PATCH_OK")


if __name__ == "__main__":
    main()
