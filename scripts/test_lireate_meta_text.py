#!/usr/bin/env python3
"""Tests for lireate_meta_text."""

import unittest

from lireate_meta_text import normalize_seo_description, normalize_seo_title, truncate_utf8


class TestTruncateUtf8(unittest.TestCase):
    def test_short_unchanged(self):
        self.assertEqual(truncate_utf8("короткий", 50), "короткий")

    def test_word_boundary_cyrillic(self):
        text = "Компенсация за нарушение товарного знака: расчёт и доказательства для суда"
        out = truncate_utf8(text, 40)
        self.assertLessEqual(len(out), 40)
        self.assertFalse(out.endswith("расч"))
        self.assertTrue(out.endswith("расчёт") or "расчёт" not in text[: len(out) + 1])

    def test_description_ellipsis(self):
        base = "А" * 250
        out = normalize_seo_description(base, max_len=200)
        self.assertLessEqual(len(out), 200)
        self.assertTrue(out.endswith("…"))

    def test_seo_title_no_mid_word_cut(self):
        title = (
            "Реальные сроки регистрации товарного знака и «ускоренный порядок»: "
            "когда имеет смысл платить"
        )
        out = normalize_seo_title(title, max_len=70)
        self.assertLessEqual(len(out), 70)
        self.assertNotIn("ко", out[-3:])


if __name__ == "__main__":
    unittest.main()