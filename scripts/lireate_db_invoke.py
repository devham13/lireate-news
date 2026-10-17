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
    slug = meta.get("slug") or ""
    canonical = (meta.get("canonical_path") or "/{0}".format(slug)).strip("/")
    seo_url = canonical.split("/")[-1] if canonical else slug.replace("-", "_")
    name = meta.get("title") or meta.get("h1") or slug
    title = meta.get("h1") or meta.get("title") or name
    keywords = meta.get("keywords") or []
    if isinstance(keywords, list):
        seo_keywords = ", ".join(keywords)
    else:
        seo_keywords = str(keywords)
    short_story = short_html or meta.get("description") or ""
    full_story = full_html or ""
    if cover_web_path:
        img = '<p><img src="{0}" alt="" /></p>'.format(cover_web_path)
        if img not in full_story:
            full_story = img + full_story
    return {
        "name": name,
        "title": title,
        "seo_title": meta.get("title") or name,
        "seo_keywords": seo_keywords,
        "seo_description": meta.get("description") or "",
        "seo_url": seo_url,
        "category": int(meta.get("lireate_category_id", 9)),
        "short_story": short_story,
        "full_story": full_story,
        "active": 1,
    }
