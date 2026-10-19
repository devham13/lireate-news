#!/usr/bin/env python3
"""Unit tests for lireate collage-v1 (no Chromium required)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_collage.derive import category_badge, derive_cover_spec, split_headline  # noqa: E402
from lireate_collage.eligibility import collage_allowed  # noqa: E402
from lireate_collage.validate import validate_cover_spec, validate_inline_item  # noqa: E402


class TestCollage(unittest.TestCase):
    def test_frozen_l01(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "article.meta.json").write_text('{"topic_id":"L01"}\n', encoding="utf-8")
            ok, reason = collage_allowed(p)
            self.assertFalse(ok)
            self.assertIn("L01", reason)

    def test_new_l06(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "article.meta.json").write_text('{"topic_id":"L06"}\n', encoding="utf-8")
            ok, _ = collage_allowed(p)
            self.assertTrue(ok)

    def test_split_headline(self):
        lines, hl = split_headline("Проверка товарного знака перед подачей в Роспатент")
        self.assertTrue(lines)
        self.assertTrue(hl)

    def test_derive_cover(self):
        meta = {
            "h1": "Патент или ноу-хау",
            "lireate_category_name": "Патент",
            "keywords": ["патент", "ноу-хау"],
        }
        spec = derive_cover_spec(meta)
        self.assertEqual(spec["badge_label"], "ПАТЕНТ")
        self.assertFalse(validate_cover_spec(spec))
        self.assertIn("Патентная заявка", spec["ui_card_title"])
        self.assertNotIn("МКТУ", " ".join(spec["ui_card_rows"]))

    def test_derive_copyright_ui(self):
        meta = {"lireate_category_name": "Авторское право", "cover_headline": "Права на текст"}
        spec = derive_cover_spec(meta)
        self.assertIn("Права на контент", spec["ui_card_title"])

    def test_inline_bad_good(self):
        item = {
            "template": "bad_good",
            "headline": "Тест",
            "bad": {"header": "a", "lines": ["x"]},
            "good": {"header": "b", "lines": ["y"]},
            "conclusion": {"box_lines": ["итог"]},
        }
        self.assertFalse(validate_inline_item(item))


if __name__ == "__main__":
    unittest.main()
