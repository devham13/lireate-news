#!/usr/bin/env python3
"""Smoke + screenshots for /avtor/ on the public Lireate site."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

import os

_base = os.environ.get("LIREATE_PUBLIC_SITE_URL", "").rstrip("/")
if not _base:
    raise SystemExit("LIREATE_PUBLIC_SITE_URL is required for verify script")
SITE = _base + "/avtor/"
ART = Path("/opt/cursor/artifacts")
ART.mkdir(parents=True, exist_ok=True)

EXPECTED_TITLE = "Горбачев Юрий Александрович — директор бюро «Лирейт»"
EXPECTED_DESC = (
    "Юрий Горбачев — директор и управляющий партнёр ООО «ЛИРЕЙТ»: товарные знаки, "
    "патенты, авторское право и споры. Статьи на vc.ru, в Т—Ж, на Клерке и Хабре."
)


def main() -> int:
    results: dict = {"url": SITE, "checks": [], "ok": True}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, name in ((375, "avtor-375"), (1366, "avtor-1366")):
            page = browser.new_page(viewport={"width": width, "height": 900})
            resp = page.goto(SITE, wait_until="networkidle", timeout=120000)
            status = resp.status if resp else 0
            results["checks"].append({"viewport": width, "http_status": status})
            if status != 200:
                results["ok"] = False
            page.screenshot(path=str(ART / f"{name}.png"), full_page=True)
            page.close()
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        page.goto(SITE, wait_until="domcontentloaded", timeout=120000)
        title = page.title()
        desc = page.locator('meta[name="description"]').get_attribute("content") or ""
        h1s = page.locator("h1").all_text_contents()
        robots = page.locator('meta[name="robots"]').count()
        ld = page.locator('script[type="application/ld+json"]').all_text_contents()
        person_blocks = sum(1 for block in ld if '"@type":"Person"' in block.replace(" ", "") or '"@type": "Person"' in block)
        img_ok = page.locator('img[alt="Горбачев Юрий Александрович"]').count() >= 1
        results["title"] = title
        results["description"] = desc
        results["h1_count"] = len(h1s)
        results["h1_texts"] = h1s
        results["robots_meta_count"] = robots
        results["person_jsonld_blocks"] = person_blocks
        results["photo_ok"] = img_ok
        if title != EXPECTED_TITLE:
            results["ok"] = False
        if desc != EXPECTED_DESC:
            results["ok"] = False
        if len(h1s) != 1 or h1s[0].strip() != "Горбачев Юрий Александрович":
            results["ok"] = False
        if person_blocks != 1:
            results["ok"] = False
        if robots > 0:
            content = page.locator('meta[name="robots"]').first.get_attribute("content") or ""
            if "noindex" in content.lower():
                results["ok"] = False
        browser.close()
    out = ART / "avtor-verify.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if results["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
