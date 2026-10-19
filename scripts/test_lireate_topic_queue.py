#!/usr/bin/env python3
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_topic_queue import is_auto_publish_article, next_unpublished_article  # noqa: E402


class TestTopicQueue(unittest.TestCase):
    def test_sample_and_high_l_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            art = root / "memory/blog/articles"
            l99 = art / "L99-test"
            l99.mkdir(parents=True)
            (l99 / "article.html").write_text("<p>x</p>", encoding="utf-8")
            (l99 / "article.meta.json").write_text(
                json.dumps({"topic_id": "L99", "sample": True}), encoding="utf-8"
            )
            self.assertFalse(is_auto_publish_article("L99", l99))
            state = root / "state.json"
            state.write_text("{}", encoding="utf-8")
            self.assertIsNone(next_unpublished_article(root, state))

    def test_l06_ok(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            l06 = root / "memory/blog/articles/L06-x"
            l06.mkdir(parents=True)
            (l06 / "article.html").write_text("<p>x</p>", encoding="utf-8")
            (l06 / "article.meta.json").write_text(
                json.dumps({"topic_id": "L06"}), encoding="utf-8"
            )
            self.assertTrue(is_auto_publish_article("L06", l06))


if __name__ == "__main__":
    unittest.main()
