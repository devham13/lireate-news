#!/usr/bin/env python3
"""Ensure unpublished Lireate articles do not reuse live seo_url paths (Py3.6+)."""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_news_format import build_news_row  # noqa: E402
from lireate_publish_live import http_status  # noqa: E402
from lireate_topic_queue import (  # noqa: E402
    ALWAYS_PUBLISHED,
    article_dirs,
    published_ids,
    topic_cards,
)


def repo_root():
    return REPO_ROOT


def topic_status_map(root):
    out = {}
    for c in topic_cards(root):
        out[c["id"].upper()] = c.get("status") or "unknown"
    return out


ALWAYS_PUBLISHED = set(ALWAYS_PUBLISHED)
LEGACY_LIVE_ON_HOST_MAX = 17


def is_published_topic(topic_id, root, state_file):
    tid = (topic_id or "").upper()
    if tid in ALWAYS_PUBLISHED:
        return True
    if topic_status_map(root).get(tid) == "published":
        return True
    m = re.match(r"^L(\d+)$", tid)
    if m and int(m.group(1)) <= LEGACY_LIVE_ON_HOST_MAX:
        return True
    dirs = article_dirs(root)
    done = published_ids(state_file, dirs)
    return tid in done


def collect_seo_urls(root):
    rows = []
    for tid, adir in sorted(article_dirs(root).items(), key=lambda x: x[0]):
        meta_path = adir / "article.meta.json"
        html_path = adir / "article.html"
        if not meta_path.is_file() or not html_path.is_file():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (ValueError, TypeError):
            continue
        if meta.get("sample") is True:
            continue
        row = build_news_row(meta, html_path.read_text(encoding="utf-8"))
        seo = (row.get("seo_url") or "").strip()
        if not seo:
            rows.append((tid, adir, None, "missing seo_url"))
            continue
        rows.append((tid, adir, seo, None))
    return rows


def check_duplicate_seo_urls(rows):
    errors = []
    by_url = {}
    for tid, _adir, seo, err in rows:
        if err or not seo:
            errors.append("{0}: {1}".format(tid, err or "empty seo_url"))
            continue
        by_url.setdefault(seo, []).append(tid)
    for seo, tids in by_url.items():
        if len(tids) > 1:
            errors.append("duplicate seo_url {0!r}: {1}".format(seo, ", ".join(tids)))
    return errors


def check_live_unpublished(root, state_file, site_base, timeout=25):
    errors = []
    skipped = []
    site = (site_base or "").strip().rstrip("/")
    if not site:
        skipped.append("LIREATE_PUBLIC_SITE_URL unset — live HTTP checks skipped")
        return errors, skipped

    for tid, _adir, seo, err in collect_seo_urls(root):
        if err or not seo:
            continue
        if is_published_topic(tid, root, state_file):
            continue
        url = "{0}/{1}".format(site, seo)
        status = http_status(url, timeout=timeout)
        if status == 200:
            errors.append(
                "{0}: unpublished seo_url already live (HTTP 200): /{1}".format(tid, seo)
            )
        elif isinstance(status, int) and status not in (404, 403, 410):
            skipped.append(
                "{0}: /{1} returned HTTP {2} (expected 404 for free slug)".format(
                    tid, seo, status
                )
            )
    return errors, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=repo_root())
    ap.add_argument(
        "--state-file",
        type=Path,
        default=None,
        help="published.json path (default: state/published.json under root)",
    )
    ap.add_argument(
        "--site-base",
        default=os.environ.get("LIREATE_PUBLIC_SITE_URL", "").strip(),
        help="Public site URL for live checks",
    )
    ap.add_argument("--skip-live", action="store_true", help="Only duplicate/missing checks")
    args = ap.parse_args()

    root = args.root.resolve()
    state_file = args.state_file or (root / "state" / "published.json")

    errors = check_duplicate_seo_urls(collect_seo_urls(root))
    skipped = []
    if not args.skip_live:
        live_err, skipped = check_live_unpublished(root, state_file, args.site_base)
        errors.extend(live_err)

    if skipped:
        for line in skipped:
            print("WARN:", line)
    if errors:
        print("SEO_URL_PUBLISH_GUARD FAIL")
        for e in errors:
            print("  ERROR:", e)
        return 1
    print("OK SEO_URL_PUBLISH_GUARD PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
