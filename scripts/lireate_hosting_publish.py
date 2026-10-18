#!/usr/bin/env python3
"""
Cron entry for REG.RU shared hosting: cover image + direct MySQL via PHP CLI.
"""

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

from lireate_compat import require_python  # noqa: E402
from lireate_db_invoke import run_publish  # noqa: E402
from lireate_dotenv import load_dotenv  # noqa: E402
from lireate_hosting_images import (  # noqa: E402
    build_hosting_image_map,
    deploy_hosting_images,
    list_planned_image_destinations,
    transform_html_paths,
)
from lireate_news_format import build_news_row  # noqa: E402
from lireate_publish_bundle import build_publish_bundle  # noqa: E402
from lireate_publish_live import http_status, is_already_live, record_published  # noqa: E402

require_python((3, 6))


def _truthy(name):
    v = (os.environ.get(name) or "").strip().lower()
    return v in ("1", "yes", "true", "on")


def _default_autopub_home():
    return Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))


def _setup_logging(log_path):
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handlers = [logging.StreamHandler(sys.stdout)]
    try:
        handlers.insert(0, logging.FileHandler(str(log_path), encoding="utf-8"))
    except TypeError:
        handlers.insert(0, logging.FileHandler(str(log_path)))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
    )


@contextmanager
def _file_lock(lock_path):
    lock_path = Path(lock_path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    import fcntl

    fh = lock_path.open("a+", encoding="utf-8")
    try:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        fh.close()
        raise SystemExit("STATUS: BLOCKER another publish run holds the lock")
    try:
        fh.seek(0)
        fh.truncate()
        fh.write("pid={0}\n".format(os.getpid()))
        fh.flush()
        yield
    finally:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        finally:
            fh.close()


def _append_repo_ledger(topic_id, slug, url, category_id):
    ledger = REPO_ROOT / "shared" / "published-articles-lireate.md"
    if not ledger.is_file():
        return
    line = "| {0} | {1} | {2} | {3} | {4} | published |".format(
        date.today().isoformat(),
        topic_id or "",
        slug,
        url or "",
        category_id,
    )
    text = ledger.read_text(encoding="utf-8")
    if slug in text and "published" in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    ledger.write_text(text + line + "\n", encoding="utf-8")


def _print_status(code, detail=""):
    msg = "STATUS: {0}".format(code)
    if detail:
        msg = "{0} — {1}".format(msg, detail)
    print(msg)
    logging.info(msg)


def _print_dry_run_preview(row, docroot_path, image_paths):
    print("=== DRY-RUN ROW PREVIEW (no writes) ===")
    print("name: {0}".format(row.get("name")))
    print("seo_url: {0}".format(row.get("seo_url")))
    print("category: {0}".format(row.get("category")))
    print("title (int): {0}".format(row.get("title")))
    print("short_story: {0!r}".format(row.get("short_story")))
    print("image_files (would write under docroot):")
    for p in image_paths:
        print("  - {0}".format(p))
    fs = row.get("full_story") or ""
    print("full_story (first 500 chars):")
    print(fs[:500])


def main():
    parser = argparse.ArgumentParser(description="Lireate hosting autopublish (REG.RU cron)")
    parser.add_argument("--article-dir", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing news row (same seo_url) and redeploy images",
    )
    parser.add_argument("--env-file", type=Path, default=None)
    args = parser.parse_args()

    home = _default_autopub_home()
    env_file = args.env_file or Path(os.environ.get("LIREATE_ENV_FILE") or (home / ".env"))
    if env_file.is_file():
        load_dotenv(env_file, override=False)

    log_file = Path(os.environ.get("LIREATE_LOG_FILE") or (home / "logs" / "publish.log"))
    lock_file = Path(os.environ.get("LIREATE_LOCK_FILE") or (home / "var" / "publish.lock"))
    state_file = Path(os.environ.get("LIREATE_STATE_FILE") or (home / "state" / "published.json"))

    if not args.dry_run:
        _setup_logging(log_file)

    article_dir = args.article_dir
    if article_dir is None:
        raw = (os.environ.get("LIREATE_ARTICLE_DIR") or "").strip()
        if raw:
            article_dir = Path(raw)
    if article_dir is None:
        # Auto mode: only the newest not-yet-published L* article. No L01 fallback, no --update.
        from lireate_topic_queue import next_unpublished_article

        if args.update:
            print("STATUS: BLOCKER — --update requires explicit --article-dir (auto mode never rewrites)")
            return 2
        article_dir = next_unpublished_article(REPO_ROOT, state_file)
        if article_dir is None:
            _print_status("NO_NEW_ARTICLE", "nothing to publish")
            return 0
    article_dir = article_dir.resolve()

    result_path = article_dir / "lireate-publish-result.json"
    meta_path = article_dir / "article.meta.json"
    html_path = article_dir / "article.html"

    site = (os.environ.get("LIREATE_PUBLIC_SITE_URL") or "").strip().rstrip("/")
    docroot = (os.environ.get("LIREATE_DOCROOT") or "").strip()
    allow = _truthy("LIREATE_ALLOW_PUBLISH")
    docroot_path = Path(docroot).expanduser().resolve() if docroot else None

    result = {
        "mode": "hosting_db",
        "verdict": "blocker",
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
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

    html = html_path.read_text(encoding="utf-8")
    bundle, _image_map, _transformed = build_publish_bundle(article_dir, meta, html)
    row_preview = build_news_row(meta, html)
    seo_url = row_preview["seo_url"]
    hosting_map = build_hosting_image_map(seo_url, article_dir)
    body_for_cms = transform_html_paths(html, hosting_map)
    row = build_news_row(meta, body_for_cms)
    payload = {
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
    if args.update:
        payload["force_update"] = True
    planned_base = docroot_path if docroot_path and docroot_path.is_dir() else Path(docroot or ".")
    planned_images = list_planned_image_destinations(planned_base, seo_url, article_dir)

    target_url = "{0}/{1}".format(site, row["seo_url"]) if site else None
    result.update(
        {
            "topic_id": topic_id,
            "slug": slug,
            "seo_url": row["seo_url"],
            "target_url": target_url,
            "bundle_dir": str(bundle),
            "payload": payload,
        }
    )

    if args.dry_run:
        base = docroot_path if docroot_path and docroot_path.is_dir() else Path(docroot or ".")
        _print_dry_run_preview(row, base, planned_images)
        result["verdict"] = "dry_run"
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _print_status("DRY_RUN", "preview only — no DB or files written")
        return 0

    with _file_lock(lock_file):
        if target_url:
            already, st = is_already_live(site, "/" + row["seo_url"], state_file, slug)
            result["live_url_http_before"] = st
            if already and not args.update:
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

        if not site or not docroot_path or not docroot_path.is_dir():
            result["blocker"] = "set LIREATE_PUBLIC_SITE_URL and LIREATE_DOCROOT"
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        db_php = docroot_path / "data" / "db.php"
        if not db_php.is_file():
            result["blocker"] = "missing {0}".format(db_php)
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        img_ok, img_paths, img_detail = deploy_hosting_images(
            docroot_path, row["seo_url"], article_dir
        )
        result["hosting_images"] = {"ok": img_ok, "paths": img_paths, "detail": img_detail}
        if not img_ok:
            result["blocker"] = "image deploy failed: {0}".format(img_detail)
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("BLOCKER", result["blocker"])
            return 1

        db_res = run_publish(docroot_path, payload)
        result["db"] = db_res

        live_after = http_status(target_url) if target_url else None
        result["live_url_http_after"] = live_after

        db_ok = db_res.get("ok") and (
            db_res.get("insert_id") or db_res.get("updated") or db_res.get("duplicate")
        )
        if db_res.get("dry_run"):
            db_ok = False

        if db_ok and live_after == 200:
            result["verdict"] = "published"
            result["live_url"] = target_url
            record_published(state_file, slug, topic_id, target_url, category_id)
            _append_repo_ledger(topic_id, slug, target_url, category_id)
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_status("PUBLISHED", target_url)
            return 0

        if db_res.get("ok") and db_res.get("duplicate") and live_after != 200:
            result["blocker"] = "duplicate in DB but live URL still {0}".format(live_after)
        elif db_res.get("ok") and live_after != 200:
            result["blocker"] = "DB insert OK but live URL still {0}".format(live_after)
        else:
            result["blocker"] = "DB publish failed: {0}".format(db_res.get("error") or db_res)

        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _print_status("BLOCKER", str(result["blocker"]))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
