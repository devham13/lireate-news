#!/usr/bin/env python3
"""Publish Lireate NEWS article via REG.RU FTP + admin bundle (LIREATE_* only)."""

import argparse
import ftplib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from lireate_cms_http import LireateCmsClient, load_http_config_path  # noqa: E402
from lireate_compat import require_python  # noqa: E402
from lireate_publish_bundle import build_publish_bundle  # noqa: E402
from lireate_publish_live import http_status  # noqa: E402

require_python((3, 6))


def _truthy(name):
    v = (os.environ.get(name) or "").strip().lower()
    return v in ("1", "yes", "true", "on")


def _ftp_connect(host, port, user, password, root):
    ftp = ftplib.FTP()
    ftp.connect(host, port, timeout=30)
    ftp.login(user, password)
    if root and root not in (".", "/"):
        ftp.cwd(root.lstrip("/"))
    return ftp


def _ftp_probe_data_channel(host, port, user, password, root):
    ftp = None
    try:
        ftp = _ftp_connect(host, port, user, password, root)
        ftp.set_pasv(True)
        names = ftp.nlst()
        ftp.quit()
        return True, "nlst_ok count={0}".format(len(names))
    except Exception as e:
        if ftp is not None:
            try:
                ftp.quit()
            except Exception:
                pass
        return False, "{0}: {1}".format(type(e).__name__, e)


def _ftp_upload_images(host, port, user, password, root, bundle_images, remote_dir="template/images/blog"):
    uploaded = []
    ftp = None
    try:
        ftp = _ftp_connect(host, port, user, password, root)
        ftp.set_pasv(True)
        parts = [p for p in remote_dir.split("/") if p]
        for part in parts:
            try:
                ftp.cwd(part)
            except ftplib.error_perm:
                try:
                    ftp.mkd(part)
                except ftplib.error_perm:
                    pass
                ftp.cwd(part)
        for path in sorted(Path(bundle_images).glob("*")):
            if not path.is_file():
                continue
            with path.open("rb") as f:
                ftp.storbinary("STOR {0}".format(path.name), f)
            uploaded.append(path.name)
        ftp.quit()
        return True, uploaded, "ok"
    except Exception as e:
        return False, uploaded, "{0}: {1}".format(type(e).__name__, e)


def _missing_autopublish_secrets():
    missing = []
    if not (os.environ.get("LIREATE_ADMIN_USER") or "").strip():
        missing.append("LIREATE_ADMIN_USER")
    if not os.environ.get("LIREATE_ADMIN_PASSWORD"):
        missing.append("LIREATE_ADMIN_PASSWORD")
    return missing


def _cms_result_dict(res):
    return {"ok": res.ok, "stage": res.stage, "detail": res.detail, "extra": res.extra}


def main():
    parser = argparse.ArgumentParser(description="Lireate NEWS publish (REG.RU)")
    parser.add_argument(
        "--article-dir",
        type=Path,
        default=REPO_ROOT
        / "memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent",
    )
    parser.add_argument("--dry-run", action="store_true", help="Only build bundle, skip FTP upload")
    parser.add_argument(
        "--cms-only",
        action="store_true",
        help="Skip FTP; only CMS HTTP (for worker after images uploaded)",
    )
    args = parser.parse_args()

    article_dir = args.article_dir.resolve()
    meta_path = article_dir / "article.meta.json"
    html_path = article_dir / "article.html"
    result_path = article_dir / "lireate-publish-result.json"

    allow = _truthy("LIREATE_ALLOW_PUBLISH")
    host = (os.environ.get("LIREATE_SFTP_HOST") or "").strip()
    port_raw = (os.environ.get("LIREATE_SFTP_PORT") or "21").strip()
    port = int(port_raw)
    if port == 22:
        print("WARN: LIREATE_SFTP_PORT=22 — переключаем на 21 (REG.RU FTP)", file=sys.stderr)
        port = 21
    user = (os.environ.get("LIREATE_SFTP_USER") or "").strip()
    password = os.environ.get("LIREATE_SFTP_PASSWORD") or ""
    root = (os.environ.get("LIREATE_REMOTE_SITE_ROOT") or "/").strip() or "/"
    site = (os.environ.get("LIREATE_PUBLIC_SITE_URL") or "").strip().rstrip("/")

    result = {
        "verdict": "blocker",
        "topic_id": None,
        "slug": None,
        "lireate_category_id": None,
        "allow_publish": allow,
        "ftp_data_channel": None,
        "admin_http": "not_attempted_no_credentials",
        "bundle_dir": str(article_dir / "publish-bundle"),
    }

    if not meta_path.is_file() or not html_path.is_file():
        result["error"] = "missing article.meta.json or article.html"
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    slug = meta.get("slug") or article_dir.name.split("-", 1)[-1]
    topic_id = meta.get("topic_id")
    category_id = meta.get("lireate_category_id", 9)
    canonical = meta.get("canonical_path") or "/{0}".format(slug)
    target_url = "{0}{1}".format(site, canonical) if site else None

    result.update(
        {
            "topic_id": topic_id,
            "slug": slug,
            "canonical_path": canonical,
            "lireate_category_id": category_id,
            "title": meta.get("title"),
            "h1": meta.get("h1"),
        }
    )

    html = html_path.read_text(encoding="utf-8")
    bundle, image_map, transformed = build_publish_bundle(article_dir, meta, html)
    img_dest = bundle / "images"

    if not allow:
        result["verdict"] = "blocker"
        result["blocker"] = "LIREATE_ALLOW_PUBLISH is not yes"
        result["manual_steps"] = _manual_steps(canonical, category_id, bundle)
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    if args.dry_run:
        result["verdict"] = "dry_run"
        result["blocker"] = "dry-run: no FTP upload"
        result["manual_steps"] = _manual_steps(canonical, category_id, bundle)
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if not args.cms_only and not all([host, user, password]):
        result["blocker"] = "missing LIREATE_SFTP_* credentials"
        result["manual_steps"] = _manual_steps(canonical, category_id, bundle)
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    ok, detail = False, "skipped_cms_only"
    if not args.cms_only:
        ok, detail = _ftp_probe_data_channel(host, port, user, password, root)
    result["ftp_data_channel"] = {"ok": ok, "detail": detail}

    live_status = http_status(target_url) if target_url else None
    result["live_url_http_before"] = live_status

    upload_ok, uploaded_names, upload_detail = False, [], "skipped"
    if ok:
        upload_ok, uploaded_names, upload_detail = _ftp_upload_images(
            host, port, user, password, root, img_dest
        )
        result["ftp_image_upload"] = {
            "ok": upload_ok,
            "files": uploaded_names,
            "detail": upload_detail,
        }
    elif args.cms_only:
        upload_ok = True
        result["ftp_image_upload"] = {"ok": False, "files": [], "detail": "cms-only mode"}

    admin_missing = _missing_autopublish_secrets()
    cms_config_path = load_http_config_path()
    cms_publish_res = None
    if not admin_missing and site:
        client = LireateCmsClient(site)
        cms_publish_res = client.publish_news(meta, transformed)
        result["admin_http"] = _cms_result_dict(cms_publish_res)

    result["cms_autopublish"] = {
        "implemented": True,
        "config_path": str(cms_config_path),
        "config_exists": cms_config_path.is_file(),
        "missing_secrets": admin_missing,
        "hint": "shared/lireate-worker-setup.md",
    }

    live_after = http_status(target_url) if target_url else None
    result["live_url_http_after"] = live_after

    cms_ok = cms_publish_res is not None and cms_publish_res.ok
    live_ok = live_after == 200

    if cms_ok and live_ok:
        result["verdict"] = "published"
        result["blocker"] = None
        result["live_url"] = target_url
        _append_ledger(topic_id, slug, target_url, category_id)
    elif cms_ok and not live_ok:
        result["verdict"] = "blocker"
        result["blocker"] = (
            "CMS step reported OK but live URL still {0} — "
            "check memory/lireate-cms-http-config.json fields or publish manually".format(live_after)
        )
    elif not admin_missing and cms_publish_res and not cms_publish_res.ok:
        result["verdict"] = "blocker"
        result["blocker"] = "CMS HTTP failed at {0}: {1}".format(
            cms_publish_res.stage, cms_publish_res.detail
        )
    elif upload_ok and admin_missing:
        result["verdict"] = "blocker"
        result["blocker"] = "FTP images OK; add {0}".format(", ".join(admin_missing))
    elif upload_ok:
        result["verdict"] = "blocker"
        result["blocker"] = (
            "FTP images uploaded ({0} files). "
            "Run on worker: python3 scripts/lireate_cms_probe.py then publish again".format(
                len(uploaded_names)
            )
        )
    elif ok:
        result["verdict"] = "blocker"
        result["blocker"] = "FTP data channel OK but image upload failed: {0}".format(upload_detail)
    else:
        result["verdict"] = "blocker"
        result["blocker"] = (
            "FTP data channel failed (typical on Cursor Cloud). "
            "Use self-hosted worker — shared/lireate-worker-setup.md"
        )

    result["manual_steps"] = _manual_steps(canonical, category_id, bundle)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("verdict") == "published" else 1


def _append_ledger(topic_id, slug, url, category_id):
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


def _manual_steps(canonical_path, category_id, bundle):
    return [
        "1. Откройте ISPmanager REG.RU → WWW-домен сайта → «Менеджер файлов» (или FTP с домашнего/офисного IP, не Cloud Agent).",
        "2. Загрузите изображения из `<article-dir>/publish-bundle/images/` в `/template/images/blog/` (имена — как в `publish-meta.json` → image_map).",
        "3. В браузере с офисного IP откройте /admin/ на публичном домене сайта → anti-bot редиректы → вход под учёткой редактора блога.",
        "4. Создайте материал в разделе «Блог / Новости» (аналог записей на /news):",
        "   - Рубрика: «Товарный знак» (category_id={0})".format(category_id),
        "   - ЧПУ (alias): `{0}`".format(canonical_path),
        "   - Title / H1 / description: из `article.meta.json`",
        "   - Тело: вставьте HTML из `publish-bundle/article-body.html` (пути к картинкам уже с `/template/images/blog/`).",
        "   - Обложка: файл cover из bundle/images (*_cover.png).",
        "5. Опубликуйте, проверьте 200 по URL и карточку в /news?num=2&category={0}".format(category_id),
        "6. При необходимости вставьте JSON-LD из `publish-bundle/schema.jsonld` в SEO-поле темы или шаблон статьи.",
        "7. После успеха добавьте строку в `shared/published-articles-lireate.md` (date, L01, slug, live URL, category_id=9, published).",
    ]


if __name__ == "__main__":
    raise SystemExit(main())
