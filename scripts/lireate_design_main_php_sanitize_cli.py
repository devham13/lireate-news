#!/usr/bin/env python3
"""CLI: sanitize main.php work file after design patches."""
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lireate_design_main_php_sanitize import sanitize_main_php_head  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: main_php_sanitize_cli.py path/to/main.php")
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = sanitize_main_php_head(raw)
    if out != raw:
        path.write_text(out, encoding="utf-8")
        print("MAIN_PHP_SANITIZE_OK")
    else:
        print("MAIN_PHP_SANITIZE_UNCHANGED")
