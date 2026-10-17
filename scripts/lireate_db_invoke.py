"""Invoke lireate_db_publish.php from Python (Py3.6+)."""

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHP_SCRIPT = REPO_ROOT / "scripts" / "lireate_db_publish.php"


def pick_php_executable():
    env = (os.environ.get("LIREATE_PHP") or "").strip()
    if env:
        return env
    home = Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))
    stored = home / ".php-interpreter"
    if stored.is_file():
        line = stored.read_text(encoding="utf-8").strip()
        if line:
            return line
    import shutil

    candidates = [
        "/opt/alt/php83/usr/bin/php",
        "/opt/alt/php82/usr/bin/php",
        "/opt/alt/php81/usr/bin/php",
        "/opt/php83/bin/php",
        "/opt/php82/bin/php",
        "/opt/php81/bin/php",
        "/opt/php/php-8.3/bin/php",
        "/opt/php/php-8.2/bin/php",
        "/opt/php/php-8.1/bin/php",
        "/opt/php/php-8.0/bin/php",
        "/opt/php/php-7.4/bin/php",
        "/usr/bin/php",
        shutil.which("php"),
        shutil.which("php-cli"),
        "php",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        if candidate == "php" or Path(candidate).exists():
            return candidate
    raise RuntimeError("PHP CLI not found; set LIREATE_PHP")


def run_diagnostic(docroot):
    php = pick_php_executable()
    proc = subprocess.run(
        [php, str(PHP_SCRIPT), "diagnostic", str(docroot)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    out = proc.stdout.strip()
    err = proc.stderr.strip()
    try:
        data = json.loads(out) if out else {"ok": False, "error": "empty stdout", "stderr": err}
    except ValueError:
        data = {"ok": False, "error": "non-json stdout", "stdout": out, "stderr": err}
    data["php_executable"] = php
    data["returncode"] = proc.returncode
    return data


def run_publish(docroot, payload, env=None):
    php = pick_php_executable()
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    body = json.dumps(payload, ensure_ascii=False)
    proc = subprocess.run(
        [php, str(PHP_SCRIPT), "publish", str(docroot)],
        input=body,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=run_env,
    )
    out = proc.stdout.strip()
    err = proc.stderr.strip()
    try:
        data = json.loads(out) if out else {"ok": False, "error": "empty stdout", "stderr": err}
    except ValueError:
        data = {"ok": False, "error": "non-json stdout", "stdout": out, "stderr": err}
    data["php_executable"] = php
    data["returncode"] = proc.returncode
    return data


def build_news_payload(meta, full_html, short_html=None, cover_web_path=None):
    from lireate_news_format import build_news_row

    row = build_news_row(meta, full_html)
    return {
        "name": row["name"],
        "title": row["title"],
        "seo_title": row["seo_title"],
        "seo_keywords": row["seo_keywords"],
        "seo_description": row["seo_description"],
        "seo_url": row["seo_url"],
        "category": row["category"],
        "short_story": row["short_story"],
        "full_story": row["full_story"],
        "active": row["active"],
    }
