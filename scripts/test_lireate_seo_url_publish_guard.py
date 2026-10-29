#!/usr/bin/env python3
"""Unit tests for lireate_seo_url_publish_guard (offline)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_seo_url_publish_guard import (  # noqa: E402
    check_duplicate_seo_urls,
    collect_seo_urls,
)


class SeoUrlGuardTests(unittest.TestCase):
    def test_duplicate_seo_url_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / "memory/blog/articles"
            for tid, slug, seo in (
                ("L90", "a-one", "same_slug"),
                ("L91", "b-two", "same_slug"),
            ):
                ad = base / "{0}-{1}".format(tid, slug)
                ad.mkdir(parents=True)
                meta = {
                    "topic_id": tid,
                    "slug": slug,
                    "title": "T",
                    "lireate_category_id": 9,
                    "lireate_seo_url": seo,
                }
                (ad / "article.meta.json").write_text(
                    json.dumps(meta, ensure_ascii=False), encoding="utf-8"
                )
                (ad / "article.html").write_text("<p>x</p>", encoding="utf-8")
            rows = collect_seo_urls(root)
            errs = check_duplicate_seo_urls(rows)
            self.assertTrue(any("duplicate" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
