"""Exercise CMS updates against the disposable localhost database in CI only."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT/'shared/lireate-visibility-fixes-2026-11-22.json'
PHP = ROOT/'scripts/lireate_visibility_db.php'


@unittest.skipUnless(os.environ.get('LIREATE_RUN_DB_TESTS') == '1', 'Disposable CI MariaDB only')
class CmsIntegration(unittest.TestCase):
    def php(self, code, *args, data=None):
        return subprocess.run(['php','-r',code]+list(args),input=data,text=True,capture_output=True,check=True).stdout

    def initialize(self, root, engine):
        # This helper can address only the CI service on localhost and a named test DB.
        config = json.loads(CONFIG.read_text())
        fixtures = []
        for i, fix in enumerate(config['titles']+config['links']):
            row = {'id':i+1,'seo_url':fix['slug'],'name':fix.get('expected_old','Тестовая статья'),
                   'seo_title':fix.get('expected_old','Тестовая статья'),'full_story':'<p>Кириллица, emoji 😀 и кавычки \'".</p>\n'}
            if 'old' in fix: row['full_story'] += '<a href="'+fix['old']+'">Ссылка</a>\n'
            fixtures.append(row)
        code = r'''
        $m=new mysqli('127.0.0.1','root',getenv('LIREATE_TEST_DB_PASSWORD'));
        $m->set_charset('utf8mb4');
        $m->query('DROP DATABASE IF EXISTS lireate_visibility_test');
        $m->query('CREATE DATABASE lireate_visibility_test CHARACTER SET utf8mb4');
        $m->select_db('lireate_visibility_test');
        $engine=$argv[1]; if(!in_array($engine,array('InnoDB','MyISAM'),true)) exit(2);
        $m->query('CREATE TABLE news (id INT PRIMARY KEY,seo_url VARCHAR(255),name VARCHAR(255),seo_title VARCHAR(255),full_story MEDIUMTEXT,active INT DEFAULT 1,datetime INT DEFAULT 12345) ENGINE='.$engine.' CHARACTER SET utf8mb4');
        foreach(json_decode(stream_get_contents(STDIN),true) as $r) {
          $st=$m->prepare('INSERT INTO news(id,seo_url,name,seo_title,full_story) VALUES (?,?,?,?,?)');
          $st->bind_param('issss',$r['id'],$r['seo_url'],$r['name'],$r['seo_title'],$r['full_story']);
          $st->execute();
        }
        '''
        self.php(code,engine,data=json.dumps(fixtures,ensure_ascii=False))
        doc=root/'public'; (doc/'data').mkdir(parents=True)
        (doc/'data/db.php').write_text("<?php define('DB_SERVER','127.0.0.1'); define('DB_USER','root'); define('DB_PASS',getenv('LIREATE_TEST_DB_PASSWORD')); define('DB_NAME','lireate_visibility_test');")
        return doc

    def rows(self):
        return json.loads(self.php("$m=new mysqli('127.0.0.1','root',getenv('LIREATE_TEST_DB_PASSWORD'),'lireate_visibility_test');$m->set_charset('utf8mb4');$r=$m->query('SELECT * FROM news ORDER BY id');$out=array();while($x=$r->fetch_assoc())$out[]=$x;echo json_encode($out);"))

    def invoke(self, mode, doc, backup=None):
        command=['php',str(PHP),mode,str(doc),str(CONFIG)]
        if backup is not None: command.append(str(backup))
        return subprocess.run(command,text=True,capture_output=True)

    def test_apply_repeat_restore_and_error_recovery_for_both_engines(self):
        for engine in ('InnoDB','MyISAM'):
            with self.subTest(engine=engine), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); doc=self.initialize(root,engine); before=self.rows()
                dry=self.invoke('plan',doc)
                self.assertEqual(dry.returncode,0,dry.stderr)
                self.assertEqual(len(json.loads(dry.stdout)['changed_slugs']),6)
                self.assertEqual(self.rows(),before)
                backup=root/'news.json'
                result=self.invoke('apply',doc,backup)
                self.assertEqual(result.returncode,0,result.stderr)
                after=self.rows()
                self.assertNotEqual(after,before)
                self.assertTrue(all(r['datetime']=='12345' for r in after))
                self.assertEqual(backup.stat().st_mode & 0o777,0o600)
                again=self.invoke('apply',doc,root/'unused.json')
                self.assertEqual(again.returncode,0,again.stderr)
                self.assertEqual(json.loads(again.stdout)['changed_slugs'],[])
                restored=self.invoke('restore',doc,backup)
                self.assertEqual(restored.returncode,0,restored.stderr)
                self.assertEqual(self.rows(),before)
                # Fail the sixth UPDATE after earlier statements succeeded. MyISAM
                # requires compensating writes; InnoDB uses the transaction rollback.
                slug=json.loads(CONFIG.read_text())['links'][-1]['slug']
                self.php("$m=new mysqli('127.0.0.1','root',getenv('LIREATE_TEST_DB_PASSWORD'),'lireate_visibility_test');$q=\"CREATE TRIGGER fail_visibility BEFORE UPDATE ON news FOR EACH ROW BEGIN IF NEW.seo_url='\".$argv[1].\"' AND NEW.full_story<>OLD.full_story THEN SIGNAL SQLSTATE '45000'; END IF; END\";if(!$m->query($q)){fwrite(STDERR,$m->error);exit(2);}",slug)
                failed=self.invoke('apply',doc,root/'failure.json')
                self.assertNotEqual(failed.returncode,0)
                self.assertEqual(self.rows(),before)


if __name__ == '__main__': unittest.main()
