#!/usr/bin/env python3
"""
Cron entry for REG.RU shared hosting: local docroot + CMS HTTP from the same server.

Loads ~/lireate-autopub/.env, file lock, logging, idempotent publish (live URL 200).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from contextlib import contextmanager
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_cms_http import LireateCmsClient, load_http_config_path  # noqa: E402
from lireate_dotenv import load_dotenv  # noqa: E402
from lireate_local_deploy import copy_bundle_images  # noqa: E402
from lireate_publish_bundle import build_publish_bundle  # noqa: E402
from lireate_publish_live import http_status, is_already_live, record_published  # noqa: E402


def _truthy(name: str) -> bool:
    v = (os.environ.get(name) or "").strip().lower()
    return v in ("1", "yes", "true", "on")


def _default_autopub_home() -> Path:
    return Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))


def _setup_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


@contextmanager
def _file_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    import fcntl

    fh = lock_path.open("a+", encoding="utf-8")
    try:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        fh.close()
        raise SystemExit("STATUS: BLOCKER another publish run holds the lock")
    try:
        fh.seek(0)
        fh.truncate()
        fh.write(f"pid={os.getpid()}\n")
        fh.flush()
        yield
    finally:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        finally:
            fh.close()


def _append_repo_ledger(topic_id: str | None, slug: str, url: str | None, category_id: int) -> None:
    ledger = REPO_ROOT / "shared" / "published-articles-lireate.md"
    if not ledger.is_file():
        return
    line = (
        f"| {date.today().isoformat()} | {topic_id or ''} | {slug} | {url or ''} | "
        f"{category_id} | published |"
    )
    text = ledger.read_text(encoding="utf-8")
    if slug in text and "published" in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    ledger.write_text(text + line + "\n", encoding="utf-8")


def _print_status(code: str, detail: str = "") -> None:
    msg = f"STATUS: {code}"
    if detail:
        msg = f"{msg} — {detail}"
    print(msg)
    logging.info(msg)


def main() -> int:
    parser = argparse.ArgumentParser(description="Lireate hosting autopublish (REG.RU cron)")
    parser.add_argument(
        "--article-dir",
        type=Path,
        default=None,
        help="Article folder (default: LIREATE_ARTICLE_DIR or L01 in repo)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--env-file", type=Path, default=None)
    args = parser.parse_args()

    home = _default_autopub_home()
    env_file = args.env_file or Path(os.environ.get("LIREATE_ENV_FILE") or (home / ".env"))
    if env_file.is_file():
        load_dotenv(env_file, override=False)

    log_file = Path(os.environ.get("LIREATE_LOG_FILE") or (home / "logs" / "publish.log"))
    lock_file = Path(os.environ.get("LIREATE_LOCK_FILE") or (home / "var" / "publish.lock"))
    state_file = Path(os.environ.get("LIREATE_STATE_FILE") or (home / "state" / "published.json"))

    _setup_logging(log_file)

    article_dir = args.article_dir
    if article_dir is None:
        raw = (os.environ.get("LIREATE_ARTICLE_DIR") or "").strip()
        if raw:
            article_dir = Path(raw)
        else:
            article_dir = (
                REPO_ROOT
                / "memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent"
            )
    article_dir = article_dir.resolve()

    result_path = article_dir / "lireate-publish-result.json"
    meta_path = article_dir / "article.meta.json"
    html_path = article_dir / "article.html"

    site = (os.environ.get("LIREATE_PUBLIC_SITE_URL") or "").strip().rstrip("/")
    docroot = (os.environ.get("LIREATE_DOCROOT") or "").strip()
    allow = _truthy("LIREATE_ALLOW_PUBLISH")

    result: dict[str, object] = {
        "mode": "hosting",
        "verdict": "blocker",
        "env_file": str(env_file),
        "article_dir": str(article_dir),
    }

    if not meta_path.is_file() or not html_path.is_file():
        result["error"] = "missing article.meta.json or article.html"
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _print_status("BLOCKER", result["error"])
        return 2

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    slug = meta.get("slug") or article_dir.name.split("-", 1)[-1]
    topic_id = meta.get("topic_id")
    category_id = int(meta.get("lireate_category_id", 9))
    canonical = meta.get("canonical_path") or f"/{slug}"
    target_url = f"{site}{canonical}" if site else None

    result.update(
        {
            "topic_id": topic_id,
            "slug": slug,
            "canonical_path": canonical,
            "target_url": target_url,
        }
    )

    html = html_path.read_text(encoding="utf-8")
    bundle, _image_map, transformed = build_publish_bundle(article_dir, meta, html)
    result["bundle_dir"] = str(bundle)

    if args.dry_run:
        result["verdict"] = "dry_run"
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _print_status("DRY_RUN", f"bundle at {bundle}")
        return 0

    with _file_lock(lock_file):
        if target_url:
            already, st = is_already_live(site, canonical, state_file, slug)
            result["live_url_http_before"] = st
            if already:
                result["verdict"] = "already_published"
                result["live_url"] = target_url
                result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                _print_status("ALREADY_PUBLISHED", target_url)
                return 0

        if not allow:
            result["blocker"] = "LIREATE_ALLOW_PUBLISH is not yes"
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        if not site:
            result["blocker"] = "set LIREATE_PUBLIC_SITE_URL in .env"
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        if not docroot:
            result["blocker"] = "set LIREATE_DOCROOT (absolute path to site public_html)"
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        docroot_path = Path(docroot).expanduser().resolve()
        if not docroot_path.is_dir():
            result["blocker"] = f"LIREATE_DOCROOT not a directory: {docroot_path}"
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        img_ok, copied, img_detail = copy_bundle_images(docroot_path, bundle / "images")
        result["local_image_copy"] = {"ok": img_ok, "files": copied, "detail": img_detail}
        if not img_ok:
            result["blocker"] = f"image copy failed: {img_detail}"
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        admin_user = (os.environ.get("LIREATE_ADMIN_USER") or "").strip()
        admin_pass = os.environ.get("LIREATE_ADMIN_PASSWORD") or ""
        if not admin_user or not admin_pass:
            result["blocker"] = "set LIREATE_ADMIN_USER and LIREATE_ADMIN_PASSWORD in .env"
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        cms_config = load_http_config_path()
        if not cms_config.is_file():
            alt = home / "cms-config" / "lireate-cms-http-config.json"
            if alt.is_file():
                os.environ["LIREATE_CMS_HTTP_CONFIG"] = str(alt)
                cms_config = alt
        if not cms_config.is_file():
            result["blocker"] = (
                "missing CMS HTTP config — run lireate_cms_probe.py once, "
                "copy memory/lireate-cms-http-config.json to ~/lireate-autopub/cms-config/"
            )
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        client = LireateCmsClient(site)
        cms_res = client.publish_news(meta, transformed, skip_if_live=True)
        result["admin_http"] = cms_res.__dict__
        result["cms_config"] = str(cms_config)

        live_after = http_status(target_url) if target_url else None
        result["live_url_http_after"] = live_after

        if cms_res.ok and live_after == 200:
            result["verdict"] = "published"
            result["live_url"] = target_url
            record_published(state_file, slug, topic_id, target_url, category_id)
            _append_repo_ledger(topic_id, slug, target_url, category_id)
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("PUBLISHED", target_url)
            return 0

        if cms_res.ok and live_after != 200:
            result["blocker"] = (
                f"CMS step OK ({cms_res.detail}) but live URL still {live_after} — "
                "check news.fields in cms-config JSON"
            )
        else:
            result["blocker"] = f"CMS HTTP failed at {cms_res.stage}: {cms_res.detail}"

        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _print_status("BLOCKER", result["blocker"])
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
