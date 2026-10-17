#!/usr/bin/env python3
"""Self-check after install on REG.RU hosting (no secrets printed)."""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_compat import require_python  # noqa: E402
from lireate_db_invoke import pick_php_executable  # noqa: E402
from lireate_dotenv import load_dotenv  # noqa: E402

require_python((3, 6))


def main():
    home = Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))
    env_file = Path(os.environ.get("LIREATE_ENV_FILE") or (home / ".env"))
    load_dotenv(env_file, override=False)

    report = {
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "python_ok": sys.version_info[:2] >= (3, 6),
        "env_file": str(env_file),
        "env_exists": env_file.is_file(),
        "autopub_home": str(home),
    }

    interpreter_file = home / ".python-interpreter"
    if interpreter_file.is_file():
        report["stored_python"] = interpreter_file.read_text(encoding="utf-8").strip()

    php_file = home / ".php-interpreter"
    if php_file.is_file():
        report["stored_php"] = php_file.read_text(encoding="utf-8").strip()
    try:
        report["php_executable"] = pick_php_executable()
        report["php_ok"] = True
    except Exception as e:
        report["php_ok"] = False
        report["php_error"] = str(e)

    required = [
        "LIREATE_PUBLIC_SITE_URL",
        "LIREATE_DOCROOT",
        "LIREATE_ALLOW_PUBLISH",
    ]
    missing = [k for k in required if not (os.environ.get(k) or "").strip()]
    report["missing_env_keys"] = missing

    docroot = (os.environ.get("LIREATE_DOCROOT") or "").strip()
    if docroot:
        p = Path(docroot).expanduser()
        report["docroot_exists"] = p.is_dir()
        report["db_php_exists"] = (p / "data" / "db.php").is_file()
        images = p / "images"
        report["images_dir_exists"] = images.is_dir()
        if images.is_dir():
            try:
                test = images / ".lireate_write_test"
                test.write_text("ok", encoding="utf-8")
                test.unlink()
                report["images_dir_writable"] = True
            except OSError:
                report["images_dir_writable"] = False
        else:
            report["images_dir_writable"] = False

        blog_tpl = p / "template" / "images" / "blog"
        report["blog_template_dir_exists"] = blog_tpl.is_dir()
        report["blog_template_dir_writable"] = False
        if blog_tpl.is_dir():
            try:
                test = blog_tpl / ".lireate_write_test"
                test.write_text("ok", encoding="utf-8")
                test.unlink()
                report["blog_template_dir_writable"] = True
            except OSError:
                report["blog_template_dir_writable"] = False

    repo = home / "repo"
    report["repo_dir"] = str(repo)
    report["repo_exists"] = (repo / "scripts" / "lireate_hosting_publish.py").is_file()
    report["db_publish_php_exists"] = (repo / "scripts" / "lireate_db_publish.php").is_file()

    ok = (
        report.get("python_ok")
        and report.get("env_exists")
        and not missing
        and report.get("docroot_exists")
        and report.get("db_php_exists")
        and report.get("images_dir_writable")
        and report.get("blog_template_dir_writable")
        and report.get("repo_exists")
        and report.get("db_publish_php_exists")
        and report.get("php_ok")
    )
    report["verdict"] = "pass" if ok else "fail"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
