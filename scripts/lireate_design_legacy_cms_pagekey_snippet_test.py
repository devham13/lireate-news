#!/usr/bin/env python3
"""php -l on hosting pagekey inline fragment after _hide_pagekey."""
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lireate_design_patch_legacy_cms_services import (  # noqa: E402
    PAGEKEY_COMMENT,
    _hide_pagekey,
    _php_lint,
)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: pagekey_snippet_test.py fragment.php")
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8")
    out = _hide_pagekey(raw)
    if "echo $temp['pagekey']" in out:
        raise SystemExit("pagekey echo still present")
    if PAGEKEY_COMMENT not in out:
        raise SystemExit("pagekey comment missing")
    if "<?php /* lireate_hide_pagekey_v1" in out:
        raise SystemExit("nested <?php comment tag (invalid inside open block)")
    _php_lint(out)
    path.write_text(out, encoding="utf-8")
    print("PAGEKEY_INLINE_SNIPPET_OK")


if __name__ == "__main__":
    main()
