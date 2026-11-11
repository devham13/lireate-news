#!/usr/bin/env python3
"""Copy service-landings/*/index.php from repo to hosting docroot (idempotent)."""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

SLUGS = (
    "dogovory",
    "registraciya_programm_evm",
)
ASSETS_TEMPLATE_SLUG = "prodlenie_tovarnogo_znaka"


def deploy(docroot: Path, repo_root: Path) -> int:
    src_root = repo_root / "hosting-design" / "service-landings"
    changed: list[str] = []
    for slug in SLUGS:
        src = src_root / slug / "index.php"
        if not src.is_file():
            print(f"MISSING {src}", file=sys.stderr)
            return 2
        dst_dir = docroot / slug
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / "index.php"
        raw = src.read_text(encoding="utf-8", errors="replace")
        live_site = os.environ.get("LIREATE_PUBLIC_SITE_URL", "").rstrip("/")
        if live_site and live_site != "https://lireate.invalid":
            raw = raw.replace("https://lireate.invalid", live_site)
            host = live_site.split("://", 1)[-1].split("/")[0]
            if host:
                raw = raw.replace("info@lireate.invalid", f"info@{host}")
        if dst.is_file() and dst.read_text(encoding="utf-8", errors="replace") == raw:
            continue
        if dst.is_file():
            bak = dst.with_suffix(dst.suffix + ".bak-2026-11-11-svc-new")
            shutil.copy2(dst, bak)
        dst.write_text(raw, encoding="utf-8")
        changed.append(slug)
        blocks_src = src_root / "blocks" / "lireate-sticky-mobile.inc.php"
        if blocks_src.is_file():
            bdst = dst_dir / "blocks"
            bdst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(blocks_src, bdst / "lireate-sticky-mobile.inc.php")
        assets_src = docroot / ASSETS_TEMPLATE_SLUG / "assets"
        assets_dst = dst_dir / "assets"
        if assets_src.is_dir():
            if assets_dst.exists():
                shutil.rmtree(assets_dst)
            shutil.copytree(assets_src, assets_dst)
        else:
            print(f"WARN assets template missing {assets_src}", file=sys.stderr)
    print("DEPLOY_SERVICE_LANDINGS_OK", len(changed), *changed)
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} DOCROOT [REPO_ROOT]", file=sys.stderr)
        raise SystemExit(2)
    docroot = Path(sys.argv[1])
    repo_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1]
    raise SystemExit(deploy(docroot, repo_root))


if __name__ == "__main__":
    main()
