#!/usr/bin/env python3
"""Apply the reviewed visibility fixes once, with private backups and conflict guards."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from lireate_db_invoke import pick_php_executable
from lireate_dotenv import load_dotenv

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / 'shared/lireate-visibility-fixes-2026-11-22.json'
STATIC = REPO / 'shared/lireate-sitemap-static.json'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', NS)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def patch_robots(text):
    # Keep every unrelated directive, bot group and comment as supplied by the owner.
    return ''.join(line for line in text.splitlines(True) if not re.match(
        r'^\s*Disallow\s*:\s*/contacts/?\s*(?:#.*)?$', line.strip(), re.I))


def patch_sitemap(text, site_url, paths):
    root = ET.fromstring(text)
    if root.tag != '{' + NS + '}urlset':
        raise ValueError('Expected a sitemap urlset; no files changed')
    base = site_url.rstrip('/')
    seen = set()
    for node in list(root):
        loc = node.find('{' + NS + '}loc')
        if loc is None or not (loc.text or '').startswith(base + '/'):
            raise ValueError('Unexpected sitemap URL; review required')
        if loc.text in seen:
            root.remove(node)
        seen.add(loc.text)
    added = []
    for item in paths:
        path = item['path'] if isinstance(item, dict) else item
        if not path.startswith('/') or path.startswith('//') or '?' in path or '#' in path:
            raise ValueError('Invalid configured sitemap path')
        url = base + path
        if url not in seen:
            node = ET.SubElement(root, '{' + NS + '}url')
            ET.SubElement(node, '{' + NS + '}loc').text = url
            # The modification date of a page is unknown; do not invent one.
            seen.add(url)
            added.append(url)
    if not added and len(list(root)) == len(ET.fromstring(text)):
        return text, []
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n', added


def safe_file(docroot, relative):
    path = docroot / relative
    if path.is_symlink():
        raise ValueError('Refusing a symlink: ' + relative)
    path.resolve().relative_to(docroot.resolve())
    if not path.is_file():
        raise ValueError('Missing existing production file: ' + relative)
    return path


def build_plan(docroot, site_url):
    robots = safe_file(docroot, 'robots.txt')
    sitemap = safe_file(docroot, 'sitemap.xml')
    config = json.loads(STATIC.read_text(encoding='utf-8'))
    original = {'robots.txt': robots.read_bytes(), 'sitemap.xml': sitemap.read_bytes()}
    xml, added = patch_sitemap(original['sitemap.xml'].decode('utf-8'), site_url, config['paths'])
    changed = {
        'robots.txt': patch_robots(original['robots.txt'].decode('utf-8')).encode('utf-8'),
        'sitemap.xml': xml.encode('utf-8'),
    }
    plan = {k: v for k, v in changed.items() if original[k] != v}
    return plan, added, {k: digest(original[k]) for k in plan}


def stage(path, data, mode=0o644):
    fd, name = tempfile.mkstemp(prefix='.lireate-visibility-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        return Path(name)
    except Exception:
        if os.path.exists(name):
            os.unlink(name)
        raise


def apply_files(docroot, plan, backup, expected=None):
    before, staged, applied = {}, {}, []
    try:
        for relative, data in plan.items():
            path = safe_file(docroot, relative)
            before[relative] = path.read_bytes()
            if expected is not None and digest(before[relative]) != expected[relative]:
                raise ValueError('File changed since preflight: ' + relative)
            mode = path.stat().st_mode & 0o777
            staged[relative] = stage(path, data, mode)
            (backup / relative).write_bytes(before[relative])
            os.chmod(str(backup / relative), 0o600)
        (backup / 'files.json').write_text(json.dumps({
            k: {'before': digest(before[k]), 'after': digest(v)} for k, v in plan.items()
        }, indent=2), encoding='utf-8')
        for relative, prepared in staged.items():
            path = safe_file(docroot, relative)
            if path.read_bytes() != before[relative]:
                raise ValueError('Concurrent file edit; update refused: ' + relative)
            os.replace(str(prepared), str(path))
            applied.append(relative)
    except Exception:
        for relative in reversed(applied):
            path = safe_file(docroot, relative)
            if path.read_bytes() == plan[relative]:
                os.replace(str(stage(path, before[relative], path.stat().st_mode & 0o777)), str(path))
        raise
    finally:
        for prepared in staged.values():
            if prepared.exists():
                prepared.unlink()


def run_db(mode, docroot, backup=None):
    command = [pick_php_executable(), str(REPO / 'scripts/lireate_visibility_db.php'),
               mode, str(docroot), str(CONFIG)]
    if backup is not None:
        command.append(str(backup))
    proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if proc.returncode:
        # The PHP entry deliberately redacts SQL errors; never print DB configuration.
        raise RuntimeError(proc.stderr.strip() or 'CMS maintenance failed')
    result = json.loads(proc.stdout)
    if not result.get('ok'):
        raise RuntimeError('CMS maintenance did not confirm success')
    return result


@contextmanager
def lock(path):
    import fcntl
    with path.open('a') as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-file', type=Path)
    parser.add_argument('--docroot', type=Path)
    parser.add_argument('--backup-root', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    home = Path(os.environ.get('LIREATE_AUTOPUB_HOME') or str(Path.home() / 'lireate-autopub'))
    load_dotenv(args.env_file or os.environ.get('LIREATE_ENV_FILE') or home / '.env', override=False)
    if args.apply and os.environ.get('LIREATE_ALLOW_PUBLISH', '').lower() not in ('yes', 'true', '1', 'on'):
        print('STATUS: VISIBILITY_SKIPPED_PUBLISH_DISABLED')
        return 0
    docroot = (args.docroot or Path(os.environ.get('LIREATE_DOCROOT', ''))).resolve()
    site = os.environ.get('LIREATE_PUBLIC_SITE_URL', '').rstrip('/')
    if not re.match(r'^https://(?:www\.)?lireate\.ru$', site):
        raise ValueError('LIREATE_PUBLIC_SITE_URL must identify the public Lireate site')
    backup_root = (args.backup_root or home / 'backups/visibility').resolve()
    state_root = (home / 'state').resolve()
    for path in (backup_root, state_root):
        if path == docroot or docroot in path.parents:
            raise ValueError('Backups and state must be outside the public docroot')
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    fingerprint = digest(CONFIG.read_bytes() + STATIC.read_bytes())
    state = state_root / (config['version'] + '.json')
    with lock(state_root / 'visibility-maintenance.lock'):
        if args.apply and state.is_file() and json.loads(state.read_text()).get('fingerprint') == fingerprint:
            print('STATUS: VISIBILITY_ALREADY_APPLIED')
            return 0
        plan, added, expected = build_plan(docroot, site)
        db_plan = run_db('plan', docroot)
        print(json.dumps({'version': config['version'], 'files': sorted(plan),
                          'added_sitemap_urls': len(added), 'article_slugs': db_plan['changed_slugs'],
                          'apply': args.apply}, ensure_ascii=False))
        if not args.apply:
            print('STATUS: VISIBILITY_DRY_RUN')
            return 0
        # Validate and reserve private backup storage before any CMS update.
        backup = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'),
                                       dir=str(backup_root)))
        db_backup = backup / 'news.json'
        applied_db = run_db('apply', docroot, db_backup)
        try:
            apply_files(docroot, plan, backup, expected)
        except Exception:
            if applied_db['changed_slugs']:
                run_db('restore', docroot, db_backup)
            raise
        urls = sorted(set(added + [site + '/contacts/'] + [site + '/' + s + '/' for s in applied_db['changed_slugs']]))
        receipt = {'fingerprint': fingerprint, 'version': config['version'],
                   'applied_at': datetime.now(timezone.utc).isoformat(), 'backup': str(backup),
                   'files': sorted(plan), 'article_slugs': applied_db['changed_slugs'], 'changed_urls': urls}
        prepared = stage(state, json.dumps(receipt, ensure_ascii=False, indent=2).encode('utf-8'), 0o600)
        os.replace(str(prepared), str(state))
        print('STATUS: VISIBILITY_APPLIED; backup: ' + str(backup))
        # Reuse only an existing verified IndexNow setup. No account or key is created.
        key = os.environ.get('INDEXNOW_KEY', '')
        if re.match(r'^[a-fA-F0-9]{32,128}$', key) and (docroot / (key + '.txt')).is_file():
            if (docroot / (key + '.txt')).read_text().strip() == key:
                from lireate_fast_indexing import post_indexnow_yandex
                from urllib.parse import urlparse
                result = post_indexnow_yandex(urlparse(site).netloc, key, urls)
                print(json.dumps({'indexnow_accepted': result.get('ok', False),
                                  'http_status': result.get('http_status')}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError) as exc:
        print('STATUS: VISIBILITY_FAILED: ' + str(exc))
        raise SystemExit(1)
