#!/usr/bin/env python3
"""Verify sitemap.xml: each loc returns 200, no redirect, canonical matches loc."""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "lireate_sitemap_verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            final = resp.geturl()
            body = resp.read(500_000).decode("utf-8", errors="replace")
            return resp.status, final, body
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:
        return -1, url, str(e)


def canonical_from_html(html):
    m = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        html,
        re.I,
    )
    if not m:
        m = re.search(
            r'href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
            html,
            re.I,
        )
    return m.group(1).strip() if m else ""


def norm(url):
    p = urllib.parse.urlparse(url)
    path = p.path or "/"
    if path != "/" and not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    return urllib.parse.urlunparse((p.scheme, p.netloc, path, "", "", ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sitemap_url")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    code, _, xml = fetch(args.sitemap_url)
    if code != 200:
        print("FAIL sitemap fetch", code)
        return 2
    root = ET.fromstring(xml)
    locs = [el.text.strip() for el in root.findall(".//sm:loc", NS) if el.text]
    if args.limit:
        locs = locs[: args.limit]
    bad = []
    for loc in locs:
        c, final, html = fetch(loc)
        if c != 200:
            bad.append((loc, "http", c))
            continue
        if norm(final) != norm(loc):
            bad.append((loc, "redirect", final))
            continue
        can = canonical_from_html(html)
        if can and norm(can) != norm(loc):
            bad.append((loc, "canonical", can))
    print("checked", len(locs), "bad", len(bad))
    for row in bad[:50]:
        print(row)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
