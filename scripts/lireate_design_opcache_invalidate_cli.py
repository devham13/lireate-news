#!/usr/bin/env python3
"""Invalidate opcache for a PHP file (hosting PHP 3.6+)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(2)
    path = str(Path(sys.argv[1]).resolve())
    code = (
        f"if(function_exists('opcache_invalidate'))"
        f"{{opcache_invalidate({path!r},true);echo 'OPCACHE_INVALIDATE_OK';}}"
        f"else echo 'OPCACHE_UNAVAILABLE';"
    )
    r = subprocess.run(["php", "-r", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.stdout.buffer.write(r.stdout)
    if r.returncode != 0 and r.stderr:
        sys.stderr.buffer.write(r.stderr)
    raise SystemExit(0)


if __name__ == "__main__":
    main()
