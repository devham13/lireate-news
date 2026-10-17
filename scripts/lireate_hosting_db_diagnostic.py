#!/usr/bin/env python3
"""Read-only DB/news diagnostic via PHP (no secrets printed)."""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_compat import require_python  # noqa: E402
from lireate_db_invoke import run_diagnostic  # noqa: E402
from lireate_dotenv import load_dotenv  # noqa: E402

require_python((3, 6))


def main():
    home = Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))
    env_file = Path(os.environ.get("LIREATE_ENV_FILE") or (home / ".env"))
    load_dotenv(env_file, override=False)
    docroot = (os.environ.get("LIREATE_DOCROOT") or "").strip()
    if not docroot:
        print("FAIL: set LIREATE_DOCROOT in .env", file=sys.stderr)
        return 2
    data = run_diagnostic(Path(docroot).expanduser().resolve())
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if data.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
