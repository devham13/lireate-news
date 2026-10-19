#!/usr/bin/env python3
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_collage_publish_gate import (  # noqa: E402
    requires_collage_v1_gate,
    validate_collage_publish,
)


def _minimal_collage_dir(base, topic_id="L07"):
    d = base / "article"
    cov = d / "cover"
    cov.mkdir(parents=True)
    (d / "article.html").write_text(
        '<p>x</p>\n<figure class="lx-article-cover" data-cover-style="collage-v1">'
        '<img src="cover/cover.png"></figure>\n'
        '<figure class="inline-collage" data-inline-style="collage-v1" data-slot="inline_1"></figure>\n'
        '<figure class="inline-collage" data-inline-style="collage-v1" data-slot="inline_2"></figure>\n',
        encoding="utf-8",
    )
    (d / "article.meta.json").write_text(
        json.dumps({"topic_id": topic_id, "cover_style": "collage-v1"}), encoding="utf-8"
    )
    (cov / "cover.png").write_bytes(b"x")
    (cov / "inline-01.png").write_bytes(b"x")
    (cov / "inline-02.png").write_bytes(b"x")
    (cov / "cover-collage-qa.md").write_text("# QA\n- PASS: cover.png\n", encoding="utf-8")
    (cov / "inline-specs.json").write_text(
        json.dumps(
            {
                "style": "collage-v1",
                "illustrations": [
                    {"slot": "inline_1", "template": "bad_good"},
                    {"slot": "inline_2", "template": "process"},
                ],
            }
        ),
        encoding="utf-8",
    )
    return d


class TestCollagePublishGate(unittest.TestCase):
    def test_requires_gate(self):
        self.assertFalse(requires_collage_v1_gate("L06"))
        self.assertTrue(requires_collage_v1_gate("L07"))
        self.assertTrue(requires_collage_v1_gate("l10"))

    def test_l06_legacy_ok_without_collage(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "L06-x"
            d.mkdir()
            (d / "article.meta.json").write_text('{"topic_id":"L06"}\n', encoding="utf-8")
            (d / "article.html").write_text("<p>legacy</p>", encoding="utf-8")
            self.assertEqual(validate_collage_publish(d), [])

    def test_l07_pass_minimal(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _minimal_collage_dir(Path(tmp))
            self.assertEqual(validate_collage_publish(d), [])

    def test_l07_fail_missing_meta(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _minimal_collage_dir(Path(tmp))
            meta = json.loads((d / "article.meta.json").read_text(encoding="utf-8"))
            meta.pop("cover_style")
            (d / "article.meta.json").write_text(json.dumps(meta), encoding="utf-8")
            errs = validate_collage_publish(d)
            self.assertTrue(any("cover_style" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
