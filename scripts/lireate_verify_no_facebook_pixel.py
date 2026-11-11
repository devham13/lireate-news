#!/usr/bin/env python3
"""Fetch sample live pages and assert no Facebook Pixel markers."""

import argparse
import random
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

PATTERNS = [
    re.compile(r"fbq\s*\(", re.I),
    re.compile(r"connect\.facebook\.net/en_US/fbevents\.js", re.I),
    re.compile(r"facebook\.com/tr\?", re.I),
]

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "lireate_verify_no_fb/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(800_000).decode("utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, help="Public site base URL (e.g. from LIREATE_PUBLIC_SITE_URL)")
    ap.add_argument("--sample", type=int, default=30)
    ap.add_argument("--seed", type=int, default=20261111)
    args = ap.parse_args()
    site = args.site.rstrip("/")
    xml = fetch(site + "/sitemap.xml")
    root = ET.fromstring(xml)
    locs = [el.text.strip() for el in root.findall(".//sm:loc", NS) if el.text]
    random.seed(args.seed)
    if len(locs) > args.sample:
        locs = random.sample(locs, args.sample)
    bad = []
    for url in locs:
        try:
            html = fetch(url)
        except Exception as exc:
            bad.append((url, "fetch", str(exc)))
            continue
        for pat in PATTERNS:
            if pat.search(html):
                bad.append((url, pat.pattern, "match"))
                break
    print("checked", len(locs), "bad", len(bad))
    for row in bad[:20]:
        print(row)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
