#!/usr/bin/env python3
import unittest

from lireate_publish_meta_validate import validate_article_meta


class TestPublishMetaValidate(unittest.TestCase):
    def test_ok_meta(self):
        meta = {
            "h1": "Как подать иск",
            "seo_title": "Иск о нарушении прав на товарный знак",
            "description": "А" * 120,
            "lireate_seo_url": "isk_o_narushenii",
            "lireate_category_id": 9,
        }
        self.assertEqual(validate_article_meta(meta), [])

    def test_missing_description(self):
        meta = {"h1": "X", "seo_title": "X", "lireate_seo_url": "x"}
        errs = validate_article_meta(meta)
        self.assertTrue(any("description" in e for e in errs))


if __name__ == "__main__":
    unittest.main()