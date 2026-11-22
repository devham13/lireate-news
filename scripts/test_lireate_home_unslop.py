#!/usr/bin/env python3
"""Exercise real file deployment, conflict handling, rollback and SEO preservation."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import lireate_home_unslop as home

FIXTURE = b'''<?php $temp = array('page' => getenv('TEST_PAGE') ?: 'home'); ?>
<html><head><title>Lireate original title</title>
<meta name="description" content="Original description">
<link rel="canonical" href="https://lireate.ru/">
<link rel="stylesheet" href="/template/css/lireate-home-hero.css?v=original">
<script type="application/ld+json">{"@type":"Organization","name":"Lireate"}</script>
</head><body class="lireate-home-dark"><h1>Original H1</h1>
<a href="/contacts/">Contacts</a><form action="/original"><input name="tel"></form>
</body></html>'''


class HomePolishTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docroot = self.root / 'public'
        (self.docroot / 'template/css').mkdir(parents=True)
        self.main = self.docroot / home.MAIN
        self.main.write_bytes(FIXTURE)
        self.main.chmod(0o640)
        self.backups = self.root / 'backups'
        self.backups.mkdir(mode=0o700)

    def apply(self):
        plan, before = home.build_plan(self.docroot)
        return home.apply_plan(self.docroot, plan, before, self.backups)

    def test_only_adds_conditional_style_and_preserves_every_original_byte(self):
        patched = home.patch_main(FIXTURE)
        self.assertEqual(patched.replace(home.LINK.encode(), b'', 1), FIXTURE)
        self.assertEqual(home.patch_main(patched), patched)

    def test_link_renders_only_for_home_in_php(self):
        self.main.write_bytes(home.patch_main(FIXTURE))
        for page in ('home', 'contacts', 'news', 'patent'):
            output = subprocess.check_output([home.pick_php_executable(), str(self.main)],
                                              env=dict(os.environ, TEST_PAGE=page))
            self.assertEqual(home.ASSET.encode() in output, page == 'home')

    def test_apply_repeat_and_restore_original_files(self):
        backup = self.apply()
        self.assertEqual(self.main.stat().st_mode & 0o777, 0o640)
        self.assertEqual((backup / 'main.php').stat().st_mode & 0o777, 0o600)
        self.assertEqual(home.build_plan(self.docroot)[0], {})
        home.restore(self.docroot, backup)
        self.assertEqual(self.main.read_bytes(), FIXTURE)
        self.assertFalse((self.docroot / home.ASSET).exists())

    def test_concurrent_template_edit_is_preserved(self):
        plan, before = home.build_plan(self.docroot)
        changed = FIXTURE + b'<!-- owner edit -->'
        self.main.write_bytes(changed)
        with self.assertRaises(ValueError):
            home.apply_plan(self.docroot, plan, before, self.backups)
        self.assertEqual(self.main.read_bytes(), changed)
        self.assertFalse((self.docroot / home.ASSET).exists())

    def test_asset_is_removed_if_template_replace_fails(self):
        replace = os.replace
        def fail_template(source, destination):
            if Path(destination) == self.main:
                raise OSError('simulated template write failure')
            return replace(source, destination)
        with mock.patch.object(home.os, 'replace', side_effect=fail_template):
            with self.assertRaises(OSError):
                self.apply()
        self.assertEqual(self.main.read_bytes(), FIXTURE)
        self.assertFalse((self.docroot / home.ASSET).exists())

    def test_restore_refuses_to_overwrite_owner_edit(self):
        backup = self.apply()
        self.main.write_bytes(self.main.read_bytes() + b'<!-- owner edit -->')
        with self.assertRaises(ValueError):
            home.restore(self.docroot, backup)
        self.assertTrue((self.docroot / home.ASSET).is_file())
        self.assertIn(b'owner edit', self.main.read_bytes())

    def test_unknown_css_is_not_overwritten(self):
        asset = self.docroot / home.ASSET
        asset.write_bytes(b'/* owner stylesheet */')
        with self.assertRaises(ValueError):
            home.build_plan(self.docroot)
        self.assertEqual(asset.read_bytes(), b'/* owner stylesheet */')

    def test_bad_head_or_edited_marker_is_rejected(self):
        for data in (FIXTURE.replace(b'</head>', b''), FIXTURE + b'</head>',
                     FIXTURE + home.MARKER.encode(), b'<?php echo "</head>"; ?>'):
            with self.assertRaises(ValueError):
                home.patch_main(data)

    def test_symlink_is_rejected(self):
        self.main.unlink()
        target = self.root / 'outside.php'
        target.write_bytes(FIXTURE)
        self.main.symlink_to(target)
        with self.assertRaises(ValueError):
            home.build_plan(self.docroot)
        self.assertEqual(target.read_bytes(), FIXTURE)


if __name__ == '__main__':
    unittest.main()
