#!/usr/bin/env python3
"""Self-check after install on REG.RU hosting (no secrets printed)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_dotenv import load_dotenv  # noqa: E402


def main() -> int:
    home = Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))
    env_file = Path(os.environ.get("LIREATE_ENV_FILE") or (home / ".env"))
    load_dotenv(env_file, override=False)

    report: dict[str, object] = {
        "python": sys.version.split()[0],
        "python_ok": sys.version_info >= (3, 8),
        "env_file": str(env_file),
        "env_exists": env_file.is_file(),
        "autopub_home": str(home),
    }

    required = [
        "LIREATE_PUBLIC_SITE_URL",
        "LIREATE_DOCROOT",
        "LIREATE_ALLOW_PUBLISH",
        "LIREATE_ADMIN_USER",
        "LIREATE_ADMIN_PASSWORD",
    ]
    missing = [k for k in required if not (os.environ.get(k) or "").strip()]
    report["missing_env_keys"] = missing

    docroot = (os.environ.get("LIREATE_DOCROOT") or "").strip()
    if docroot:
        p = Path(docroot).expanduser()
        report["docroot_exists"] = p.is_dir()
        blog = p / "template" / "images" / "blog"
        report["blog_dir_exists"] = blog.is_dir()
        if blog.is_dir():
            try:
                test = blog / ".lireate_write_test"
                test.write_text("ok", encoding="utf-8")
                test.unlink()
                report["blog_dir_writable"] = True
            except OSError:
                report["blog_dir_writable"] = False

    cms_cfg = home / "cms-config" / "lireate-cms-http-config.json"
    report["cms_config_path"] = str(cms_cfg)
    report["cms_config_exists"] = cms_cfg.is_file()

    repo = home / "repo"
    report["repo_dir"] = str(repo)
    report["repo_exists"] = (repo / "scripts" / "lireate_hosting_publish.py").is_file()

    ok = (
        report.get("python_ok")
        and report.get("env_exists")
        and not missing
        and report.get("docroot_exists")
        and report.get("blog_dir_writable")
        and report.get("repo_exists")
    )
    report["verdict"] = "pass" if ok else "fail"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
