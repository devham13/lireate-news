#!/usr/bin/env python3
"""Unit tests for sitemap / URL helpers (no DB)."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_fast_indexing import (  # noqa: E402
    build_sitemap_xml,
    normalize_article_url,
)


class TestFastIndexing(unittest.TestCase):
    def test_normalize_trailing_slash(self):
        site = "https://example.test"
        self.assertEqual(
            normalize_article_url(site, "https://example.test/foo"),
            "https://example.test/foo/",
        )
        self.assertEqual(
            normalize_article_url(site, "/bar"),
            "https://example.test/bar/",
        )

    def test_sitemap_xml_shape(self):
        xml = build_sitemap_xml(
            "https://example.test",
            [{"seo_url": "test_slug", "datetime": 1700000000}],
        )
        self.assertIn('<?xml version="1.0"', xml)
        self.assertIn("<loc>https://example.test/news/</loc>", xml)
        self.assertIn("<loc>https://example.test/test_slug/</loc>", xml)
        self.assertIn("<lastmod>", xml)
        self.assertNotIn("librend.ru", xml)


if __name__ == "__main__":
    unittest.main()
