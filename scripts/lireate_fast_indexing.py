"""Sitemap regeneration and Yandex IndexNow after Lireate publish (fail-safe)."""

import json
import logging
import os
import re
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[1]
SITEMAP_STATIC_JSON = REPO_ROOT / "shared" / "lireate-sitemap-static.json"
INDEXNOW_ENDPOINT = "https://yandex.com/indexnow"


def _site_base(site_url):
    base = (site_url or "").strip().rstrip("/")
    if not base:
        return "", ""
    parsed = urllib.parse.urlparse(base if "://" in base else "https://" + base)
    scheme = parsed.scheme or "https"
    host = parsed.netloc or parsed.path.split("/")[0]
    return "{0}://{1}".format(scheme, host), host


def normalize_article_url(site_url, article_url):
    """Canonical article URL on site host with trailing slash."""
    base, host = _site_base(site_url)
    if not base:
        return (article_url or "").strip()
    raw = (article_url or "").strip()
    if not raw:
        return ""
    parsed = urllib.parse.urlparse(raw if "://" in raw else base + raw)
    if host and parsed.netloc and parsed.netloc.lower() != host.lower():
        return raw
    path = parsed.path or "/"
    if not path.endswith("/"):
        path = path + "/"
    return base + path


def datetime_to_lastmod(ts):
    try:
        n = int(ts)
    except (TypeError, ValueError):
        return None
    return datetime.fromtimestamp(n, tz=timezone.utc).strftime("%Y-%m-%d")


def load_sitemap_static_config(path=None):
    path = Path(path) if path else SITEMAP_STATIC_JSON
    if not path.is_file():
        return {"paths": [], "exclude_article_slugs": [], "dedupe_article_slugs": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "paths": data.get("paths") or [],
        "exclude_article_slugs": set(data.get("exclude_article_slugs") or []),
        "dedupe_article_slugs": set(data.get("dedupe_article_slugs") or []),
        "sitemap_index": data.get("sitemap_index") or {},
    }


def _static_loc(base, path):
    path = (path or "/").strip()
    if path == "/":
        return base + "/"
    if not path.startswith("/"):
        path = "/" + path
    return base + path


def build_sitemap_xml(site_url, entries, static_config=None, news_list_path="/news"):
    """
    entries: list of dicts with seo_url, datetime (unix int).
  static_config: from load_sitemap_static_config() or None.
    """
    base, _host = _site_base(site_url)
    if not base:
        raise ValueError("LIREATE_PUBLIC_SITE_URL required for sitemap")

    cfg = static_config if static_config is not None else load_sitemap_static_config()
    exclude = cfg.get("exclude_article_slugs") or set()
    dedupe_once = cfg.get("dedupe_article_slugs") or set()
    seen_dedupe = set()
    url_nodes = []
    seen_urls = set()
    max_ts = 0

    for row in entries or []:
        seo = (row.get("seo_url") or "").strip().strip("/")
        if not seo or seo in exclude:
            continue
        if seo in dedupe_once:
            if seo in seen_dedupe:
                continue
            seen_dedupe.add(seo)
        ts = row.get("datetime") or 0
        try:
            ts = int(ts)
        except (TypeError, ValueError):
            ts = 0
        if ts > max_ts:
            max_ts = ts
        loc_raw = "{0}/{1}/".format(base, seo)
        if loc_raw in seen_urls:
            continue
        seen_urls.add(loc_raw)
        loc = escape(loc_raw)
        lastmod = datetime_to_lastmod(ts)
        if lastmod:
            url_nodes.append(
                "  <url>\n    <loc>{0}</loc>\n    <lastmod>{1}</lastmod>\n  </url>".format(
                    loc, lastmod
                )
            )
        else:
            url_nodes.append("  <url>\n    <loc>{0}</loc>\n  </url>".format(loc))

    site_lastmod = datetime_to_lastmod(max_ts) if max_ts else None
    static_nodes = []
    news_in_static = False
    for item in cfg.get("paths") or []:
        p = item.get("path") if isinstance(item, dict) else item
        if not p:
            continue
        if p.rstrip("/") == "/news" or p == "/news/":
            news_in_static = True
        raw_loc = _static_loc(base, p)
        if raw_loc in seen_urls:
            continue
        seen_urls.add(raw_loc)
        loc = escape(raw_loc)
        src = item.get("lastmod_source") if isinstance(item, dict) else "site"
        # A new article does not change every service, case and MKTU page.
        lm = site_lastmod if src == "articles_max" else None
        if lm:
            static_nodes.append("  <url>\n    <loc>{0}</loc>\n    <lastmod>{1}</lastmod>\n  </url>".format(loc, lm))
        else:
            static_nodes.append("  <url>\n    <loc>{0}</loc>\n  </url>".format(loc))

    if not news_in_static:
        news_path = news_list_path if news_list_path.startswith("/") else "/" + news_list_path
        static_nodes.insert(
            0,
            ("  <url>\n    <loc>{0}</loc>\n".format(escape(_static_loc(base, news_path)))
             + ("    <lastmod>{0}</lastmod>\n".format(site_lastmod) if site_lastmod else "") + "  </url>"),
        )

    body = "\n".join(static_nodes + url_nodes)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body
        + "\n</urlset>\n"
    )


def write_sitemap_atomic(docroot, xml_text):
    docroot = Path(docroot)
    target = docroot / "sitemap.xml"
    fd, tmp_name = tempfile.mkstemp(prefix="sitemap.", suffix=".xml", dir=str(docroot))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(xml_text)
        os.replace(tmp_name, str(target))
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return str(target)


def write_sitemap_bundle_atomic(docroot, bundle):
    """bundle: filename -> xml str (includes sitemap.xml index)."""
    docroot = Path(docroot)
    written = []
    for fname, xml_text in sorted(bundle.items()):
        target = docroot / fname
        fd, tmp_name = tempfile.mkstemp(
            prefix="sitemap.", suffix=".xml", dir=str(docroot)
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(xml_text)
            os.replace(tmp_name, str(target))
            written.append(str(target))
        except Exception:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise
    return written


def _sitemap_index_enabled(static_config):
    block = static_config.get("sitemap_index") if isinstance(static_config, dict) else None
    return bool(isinstance(block, dict) and block.get("enabled"))


def deploy_indexnow_key_file(docroot, key):
    key = (key or "").strip()
    if not key or not re.match(r"^[a-fA-F0-9]{32,128}$", key):
        return False, "INDEXNOW_KEY missing or invalid (expected hex key)"
    docroot = Path(docroot)
    path = docroot / "{0}.txt".format(key)
    path.write_text(key + "\n", encoding="utf-8")
    return True, str(path)


def post_indexnow_yandex(host, key, url_list, timeout=30):
    host = (host or "").strip()
    key = (key or "").strip()
    urls = [u for u in (url_list or []) if u]
    if not host or not key or not urls:
        return {"ok": False, "skipped": True, "reason": "missing host, key, or urlList"}

    key_location = "https://{0}/{1}.txt".format(host, key)
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "lireate_fast_indexing/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")[:500]
            return {"ok": code in (200, 202), "http_status": code, "body": body}
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            body = ""
        return {"ok": e.code in (200, 202), "http_status": e.code, "body": body}
    except Exception as e:
        return {"ok": False, "error": "{0}: {1}".format(type(e).__name__, e)}


def fetch_news_rows_for_sitemap(docroot):
    from lireate_db_invoke import run_sitemap_urls

    return run_sitemap_urls(docroot)


def run_after_publish(docroot, site_url, article_url, log=None):
    """
    Regenerate sitemap.xml and POST IndexNow. Never raises; returns summary dict.
    """
    log = log or (lambda msg: logging.info("%s", msg))
    summary = {"sitemap": None, "indexnow": None}

    docroot_path = Path(docroot) if docroot else None
    if not docroot_path or not docroot_path.is_dir():
        summary["sitemap"] = {"ok": False, "skipped": True, "reason": "missing docroot"}
        summary["indexnow"] = {"ok": False, "skipped": True, "reason": "missing docroot"}
        return summary

    base, host = _site_base(site_url)
    if not base:
        summary["sitemap"] = {"ok": False, "skipped": True, "reason": "missing site URL"}
        summary["indexnow"] = {"ok": False, "skipped": True, "reason": "missing site URL"}
        return summary

    try:
        db_res = fetch_news_rows_for_sitemap(docroot_path)
        if not db_res.get("ok"):
            summary["sitemap"] = {
                "ok": False,
                "error": db_res.get("error") or "sitemap_urls query failed",
            }
        else:
            rows = db_res.get("rows") or []
            static_cfg = load_sitemap_static_config()
            if _sitemap_index_enabled(static_cfg):
                try:
                    from lireate_sitemap_index_lib import build_sitemap_bundle, url_count

                    bundle = build_sitemap_bundle(site_url, rows, static_cfg)
                    paths = write_sitemap_bundle_atomic(docroot_path, bundle)
                    summary["sitemap"] = {
                        "ok": True,
                        "path": str(docroot_path / "sitemap.xml"),
                        "mode": "index",
                        "paths": paths,
                        "url_count": url_count(bundle),
                    }
                    log(
                        "fast_indexing: sitemap index written ({0} URLs, {1} files)".format(
                            url_count(bundle), len(paths)
                        )
                    )
                except Exception as index_exc:
                    summary["sitemap"] = {
                        "ok": False,
                        "error": "{0}: {1}".format(type(index_exc).__name__, index_exc),
                    }
                    log("fast_indexing: sitemap index error: {0}".format(summary["sitemap"]["error"]))
            else:
                xml = build_sitemap_xml(site_url, rows)
                path = write_sitemap_atomic(docroot_path, xml)
                summary["sitemap"] = {
                    "ok": True,
                    "path": path,
                    "mode": "urlset",
                    "url_count": len(rows) + 1,
                }
                log("fast_indexing: sitemap written {0} ({1} article URLs + /news/)".format(path, len(rows)))
    except Exception as e:
        summary["sitemap"] = {"ok": False, "error": "{0}: {1}".format(type(e).__name__, e)}
        log("fast_indexing: sitemap error (non-fatal): {0}".format(summary["sitemap"]["error"]))

    sitemap_public = "{0}/sitemap.xml".format(base)
    article_norm = normalize_article_url(site_url, article_url)
    index_key = (os.environ.get("INDEXNOW_KEY") or "").strip()

    if not index_key:
        summary["indexnow"] = {"ok": False, "skipped": True, "reason": "INDEXNOW_KEY not set"}
        log("fast_indexing: IndexNow skipped (INDEXNOW_KEY not set)")
        return summary

    url_list = []
    if article_norm:
        url_list.append(article_norm)
    url_list.append(sitemap_public)

    try:
        in_res = post_indexnow_yandex(host, index_key, url_list)
        summary["indexnow"] = in_res
        status = in_res.get("http_status")
        if status is not None:
            log("fast_indexing: IndexNow HTTP {0}".format(status))
        elif in_res.get("skipped"):
            log("fast_indexing: IndexNow skipped: {0}".format(in_res.get("reason")))
        else:
            log("fast_indexing: IndexNow failed: {0}".format(in_res.get("error") or in_res))
    except Exception as e:
        summary["indexnow"] = {"ok": False, "error": "{0}: {1}".format(type(e).__name__, e)}
        log("fast_indexing: IndexNow error (non-fatal): {0}".format(summary["indexnow"]["error"]))

    return summary


def run_deploy_indexnow_key(docroot):
    key = (os.environ.get("INDEXNOW_KEY") or "").strip()
    if not key:
        return False, "INDEXNOW_KEY not set in environment"
    return deploy_indexnow_key_file(docroot, key)
