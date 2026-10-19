#!/usr/bin/env python3
"""Cover + inline collage-v1 + HTML inject for one article dir."""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd):
    print("+", " ".join(cmd))
    return subprocess.call(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path, required=True)
    ap.add_argument("--skip-inline", action="store_true")
    ap.add_argument("--skip-inject", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    py = sys.executable
    scripts = REPO_ROOT / "scripts"
    ad = str(args.article_dir.resolve())
    force = ["--force"] if args.force else []

    rc = run([py, str(scripts / "lireate_cover_collage.py"), "--article-dir", ad] + force)
    if rc:
        return rc
    if not args.skip_inline:
        rc = run([py, str(scripts / "lireate_inline_collage.py"), "--article-dir", ad] + force)
        if rc:
            return rc
    if not args.skip_inject:
        rc = run([py, str(scripts / "lireate_collage_inject.py"), "--article-dir", ad] + force)
        if rc:
            return rc
    print("OK collage pipeline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
