"""Regression checks for the production maintenance and UTF-8 publishing boundaries."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lireate_visibility_maintenance as maintenance
from lireate_fast_indexing import build_sitemap_xml, load_sitemap_static_config
from lireate_news_format import build_news_row
from lireate_shorten_l_seo_titles import pick_title

BASE = 'https://lireate.ru'
NS = {'s': maintenance.NS}


class MaintenanceFilesTest(unittest.TestCase):
    def test_contacts_rule_only_and_no_word_cuts(self):
        original = 'User-agent: *\r\nDisallow: /contacts\r\nDisallow: /contacts/private\r\nDisallow: /admin/\r\n'
        self.assertEqual(maintenance.patch_robots(original),
                         original.replace('Disallow: /contacts\r\n', ''))
        text = 'Регистрация мобильного приложения в Роспатенте: программа для ЭВМ и товарный знак'
        result = pick_title({'title': text})
        self.assertLessEqual(len(result), 70)
        self.assertTrue(text.startswith(result))
        self.assertNotIn('…', result)
        self.assertIn(result.split()[-1], text.split())

    def test_h1_and_seo_title_have_independent_fields_and_stable_url(self):
        meta = {'title': 'Короткий заголовок', 'h1': 'Полный заголовок статьи без обрезанных слов',
                'seo_title': 'Заголовок для поисковой выдачи', 'lireate_category_id': 1}
        row = build_news_row(meta, '<p>Текст.</p>')
        old = build_news_row(dict(meta, h1=None), '<p>Текст.</p>')
        self.assertEqual(row['name'], meta['h1'])
        self.assertEqual(row['seo_title'], meta['seo_title'])
        self.assertEqual(row['seo_url'], old['seo_url'])
        self.assertIn(meta['h1'], row['full_story'])

    def test_sitemap_preserves_known_dates_deduplicates_and_is_repeatable(self):
        xml = '<?xml version="1.0"?><urlset xmlns="'+maintenance.NS+'"><url><loc>'+BASE+'/</loc><lastmod>2020-01-01</lastmod></url></urlset>'
        result, urls = maintenance.patch_sitemap(xml, BASE, [{'path': '/1/'}, {'path': '/1/'}])
        self.assertEqual(urls, [BASE+'/1/'])
        self.assertIn('2020-01-01', result)
        root = ET.fromstring(result)
        self.assertIsNone(root.findall('s:url', NS)[1].find('s:lastmod', NS))
        self.assertEqual(maintenance.patch_sitemap(result, BASE, ['/1/']), (result, []))
        with self.assertRaises(ValueError):
            maintenance.patch_sitemap(xml, BASE, ['//other.test/'])

    def test_future_generation_keeps_all_classes_and_excludes_known_article_aliases(self):
        config = load_sitemap_static_config()
        xml = build_sitemap_xml(BASE, [{'seo_url': 'test', 'datetime': 1700000000},
                                     {'seo_url': 'test', 'datetime': 1700000000},
                                     {'seo_url': 'kak_proverit_zaregistrirovan_li_tovarnyiy_znak2023'}], config)
        root = ET.fromstring(xml)
        nodes = root.findall('s:url', NS)
        urls = [n.find('s:loc', NS).text for n in nodes]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(all(BASE+'/'+str(n)+'/' in urls for n in range(1, 46)))
        self.assertNotIn(BASE+'/kak_proverit_zaregistrirovan_li_tovarnyiy_znak2023/', urls)
        static_home = next(n for n in nodes if n.find('s:loc', NS).text == BASE+'/')
        self.assertIsNone(static_home.find('s:lastmod', NS))

    def test_failed_second_file_rolls_back_first_and_preserves_private_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'public'; root.mkdir()
            backup = Path(tmp)/'backup'; backup.mkdir(mode=0o700)
            original = {'robots.txt': b'old robots', 'sitemap.xml': b'old sitemap'}
            for name, data in original.items(): (root/name).write_bytes(data)
            replace = os.replace
            def fail_second(source, target):
                if Path(target).name == 'sitemap.xml': raise OSError('simulated disk failure')
                return replace(source, target)
            with patch.object(maintenance.os, 'replace', side_effect=fail_second):
                with self.assertRaises(OSError):
                    maintenance.apply_files(root, {'robots.txt': b'new', 'sitemap.xml': b'new'}, backup)
            for name, data in original.items():
                self.assertEqual((root/name).read_bytes(), data)
                self.assertEqual((backup/name).read_bytes(), data)
                self.assertEqual((backup/name).stat().st_mode & 0o777, 0o600)
            (root/'robots.txt').unlink()
            (root/'robots.txt').symlink_to(backup/'robots.txt')
            with self.assertRaises(ValueError): maintenance.safe_file(root, 'robots.txt')

    def test_file_changed_after_preflight_is_never_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'public'; root.mkdir()
            backup=Path(tmp)/'backup'; backup.mkdir()
            target=root/'robots.txt'; target.write_bytes(b'employee edit')
            with self.assertRaises(ValueError):
                maintenance.apply_files(root, {'robots.txt':b'planned change'}, backup,
                                        {'robots.txt':maintenance.digest(b'original')})
            self.assertEqual(target.read_bytes(),b'employee edit')


@unittest.skipUnless(shutil.which('php'), 'PHP CLI is checked in CI for 5.6 and 8.3')
class MaintenancePhpTest(unittest.TestCase):
    def test_planner_repairs_only_anchor_urls_and_refuses_changed_titles(self):
        config = json.loads(maintenance.CONFIG.read_text())
        rows = {}
        for fix in config['titles']+config['links']:
            slug = fix['slug']
            rows[slug] = {'id': len(rows)+1, 'seo_url': slug,
                          'name': fix.get('expected_old', 'Статья'),
                          'seo_title': fix.get('expected_old', 'Статья'), 'full_story': '<p>Текст.</p>'}
            if 'old' in fix:
                rows[slug]['full_story'] += '<a href="'+fix['old']+'?a=1&amp;b=2#part">переход</a>'
                rows[slug]['full_story'] += '<a href="https://other.test'+fix['old']+'">другая компания</a>'
                rows[slug]['full_story'] += '<code>'+fix['old']+'</code>'
        code = "require $argv[1];$x=json_decode(stream_get_contents(STDIN),true);echo json_encode(lireate_visibility_plan($x['rows'],$x['config']));"
        command = ['php','-r',code,str(maintenance.REPO/'scripts/lireate_visibility_db.php')]
        result = subprocess.run(command,input=json.dumps({'rows':rows,'config':config}),text=True,capture_output=True,check=True)
        changes = json.loads(result.stdout)
        self.assertEqual(len(changes), 6)
        for fix in config['links']:
            body = changes[fix['slug']]['after']['full_story']
            self.assertIn('href="'+fix['new']+'?a=1&amp;b=2#part"', body)
            self.assertIn('https://other.test'+fix['old'], body)
            self.assertIn('<code>'+fix['old']+'</code>', body)
        rows[config['titles'][0]['slug']]['name'] = 'Новая редакция сотрудника'
        result = subprocess.run(command,input=json.dumps({'rows':rows,'config':config}),text=True,capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__': unittest.main()
