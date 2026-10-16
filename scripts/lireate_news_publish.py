#!/usr/bin/env python3
"""Publish Lireate NEWS article via REG.RU FTP + admin bundle (LIREATE_* only)."""

from __future__ import annotations

import argparse
import ftplib
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _truthy(name: str) -> bool:
    v = (os.environ.get(name) or "").strip().lower()
    return v in ("1", "yes", "true", "on")


def _ftp_connect(host: str, port: int, user: str, password: str, root: str) -> ftplib.FTP:
    ftp = ftplib.FTP()
    ftp.connect(host, port, timeout=30)
    ftp.login(user, password)
    if root and root not in (".", "/"):
        ftp.cwd(root.lstrip("/"))
    return ftp


def _ftp_probe_data_channel(host: str, port: int, user: str, password: str, root: str) -> tuple[bool, str]:
    try:
        ftp = _ftp_connect(host, port, user, password, root)
        ftp.set_pasv(True)
        names = ftp.nlst()
        ftp.quit()
        return True, f"nlst_ok count={len(names)}"
    except Exception as e:
        try:
            ftp.quit()
        except Exception:
            pass
        return False, f"{type(e).__name__}: {e}"


def _ftp_upload_images(
    host: str,
    port: int,
    user: str,
    password: str,
    root: str,
    bundle_images: Path,
    remote_dir: str = "template/images/blog",
) -> tuple[bool, list[str], str]:
    """Upload publish-bundle/images/* to remote_dir (relative to FTP root)."""
    import io

    uploaded: list[str] = []
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
        for path in sorted(bundle_images.glob("*")):
            if not path.is_file():
                continue
            with path.open("rb") as f:
                ftp.storbinary(f"STOR {path.name}", f)
            uploaded.append(path.name)
        ftp.quit()
        return True, uploaded, "ok"
    except Exception as e:
        return False, uploaded, f"{type(e).__name__}: {e}"


def _missing_autopublish_secrets() -> list[str]:
    missing = []
    if not (os.environ.get("LIREATE_ADMIN_USER") or "").strip():
        missing.append("LIREATE_ADMIN_USER")
    if not os.environ.get("LIREATE_ADMIN_PASSWORD"):
        missing.append("LIREATE_ADMIN_PASSWORD")
    return missing


def _transform_html(html: str, image_map: dict[str, str]) -> str:
    out = html
    for local, remote in image_map.items():
        out = out.replace(f'src="{local}"', f'src="{remote}"')
        out = out.replace(f"src='{local}'", f"src='{remote}'")
    return out


def _build_image_map(article_dir: Path, slug: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    base = f"/template/images/blog/l01_{slug.replace('-', '_')}"
    files = [
        ("cover/cover.png", f"{base}_cover.png"),
        ("cover/inline-01.png", f"{base}_inline_01.png"),
        ("cover/inline-02.png", f"{base}_inline_02.png"),
        ("cover/inline-03.png", f"{base}_inline_03.png"),
    ]
    for rel, remote in files:
        local_path = article_dir / rel
        if local_path.is_file():
            mapping[rel] = remote
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(description="Lireate NEWS publish (REG.RU)")
    parser.add_argument(
        "--article-dir",
        type=Path,
        default=REPO_ROOT
        / "memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent",
    )
    parser.add_argument("--dry-run", action="store_true", help="Only build bundle, skip FTP upload")
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

    result: dict[str, object] = {
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
    canonical = meta.get("canonical_path") or f"/{slug}"
    target_url = f"{site}{canonical}" if site else None

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

    image_map = _build_image_map(article_dir, slug)
    html = html_path.read_text(encoding="utf-8")
    transformed = _transform_html(html, image_map)

    bundle = article_dir / "publish-bundle"
    if bundle.exists():
        shutil.rmtree(bundle)
    bundle.mkdir(parents=True)
    (bundle / "article-body.html").write_text(transformed, encoding="utf-8")
    (bundle / "publish-meta.json").write_text(
        json.dumps(
            {
                "topic_id": topic_id,
                "slug": slug,
                "canonical_path": canonical,
                "lireate_category_id": category_id,
                "lireate_category_name": meta.get("lireate_category_name", "Товарный знак"),
                "title": meta.get("title"),
                "description": meta.get("description"),
                "image_map": image_map,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    img_dest = bundle / "images"
    img_dest.mkdir()
    for local_rel, remote_path in image_map.items():
        src = article_dir / local_rel
        dest_name = Path(remote_path).name
        shutil.copy2(src, img_dest / dest_name)

    schema_src = article_dir / "schema.jsonld"
    if schema_src.is_file():
        shutil.copy2(schema_src, bundle / "schema.jsonld")

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

    if not all([host, user, password]):
        result["blocker"] = "missing LIREATE_SFTP_* credentials"
        result["manual_steps"] = _manual_steps(canonical, category_id, bundle)
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    ok, detail = _ftp_probe_data_channel(host, port, user, password, root)
    result["ftp_data_channel"] = {"ok": ok, "detail": detail}

    live_status = None
    if target_url:
        try:
            req = urllib.request.Request(
                target_url, method="HEAD", headers={"User-Agent": "lireate_news_publish/1"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                live_status = resp.status
        except urllib.error.HTTPError as e:
            live_status = e.code
        except Exception as e:
            live_status = str(type(e).__name__)

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

    admin_missing = _missing_autopublish_secrets()
    result["cms_autopublish"] = {
        "implemented": False,
        "missing_secrets": admin_missing,
        "hint": "shared/lireate-autopublish-requirements.md",
    }

    if upload_ok and not admin_missing:
        result["verdict"] = "blocker"
        result["blocker"] = (
            "FTP images uploaded; CMS HTTP publish not implemented yet — "
            "need one successful admin form capture or DB schema (see lireate-autopublish-requirements.md)"
        )
    elif upload_ok:
        result["verdict"] = "blocker"
        result["blocker"] = (
            f"FTP images uploaded ({len(uploaded_names)} files). "
            f"Add secrets: {', '.join(admin_missing)} for CMS step; or use manual_steps"
        )
    elif ok:
        result["verdict"] = "blocker"
        result["blocker"] = f"FTP data channel OK but image upload failed: {upload_detail}"
    else:
        result["verdict"] = "blocker"
        result["blocker"] = (
            "FTP data channel failed (LIST/STOR timeout — typical on Cursor Cloud). "
            "Use self-hosted worker or upload images manually; add LIREATE_ADMIN_* for CMS."
        )

    result["manual_steps"] = _manual_steps(canonical, category_id, bundle)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1


def _manual_steps(canonical_path: str, category_id: int, bundle: Path) -> list[str]:
    return [
        "1. Откройте ISPmanager REG.RU → WWW-домен сайта → «Менеджер файлов» (или FTP с домашнего/офисного IP, не Cloud Agent).",
        f"2. Загрузите изображения из `<article-dir>/publish-bundle/images/` в `/template/images/blog/` (имена — как в `publish-meta.json` → image_map).",
        "3. В браузере с офисного IP откройте /admin/ на публичном домене сайта → anti-bot редиректы → вход под учёткой редактора блога.",
        "4. Создайте материал в разделе «Блог / Новости» (аналог записей на /news):",
        f"   - Рубрика: «Товарный знак» (category_id={category_id})",
        f"   - ЧПУ (alias): `{canonical_path}`",
        "   - Title / H1 / description: из `article.meta.json`",
        "   - Тело: вставьте HTML из `publish-bundle/article-body.html` (пути к картинкам уже с `/template/images/blog/`).",
        "   - Обложка: файл cover из bundle/images (*_cover.png).",
        f"5. Опубликуйте, проверьте 200 по URL и карточку в /news?num=2&category={category_id}",
        "6. При необходимости вставьте JSON-LD из `publish-bundle/schema.jsonld` в SEO-поле темы или шаблон статьи.",
        "7. После успеха добавьте строку в `shared/published-articles-lireate.md` (date, L01, slug, live URL, category_id=9, published).",
    ]


if __name__ == "__main__":
    raise SystemExit(main())
