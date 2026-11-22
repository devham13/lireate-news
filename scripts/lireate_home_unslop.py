#!/usr/bin/env python3
"""Install the reviewed home-only stylesheet without replacing CMS templates."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from lireate_db_invoke import pick_php_executable
from lireate_dotenv import load_dotenv
from lireate_visibility_maintenance import digest, lock, stage

REPO = Path(__file__).resolve().parents[1]
ASSET = 'template/css/lireate-home-unslop.css'
MAIN = 'template/main.php'
VERSION = '20261122u1'
MARKER = 'lireate_home_unslop_' + VERSION
LINK = ('<?php /* ' + MARKER + ' */ '
        "if (isset($temp['page']) && $temp['page'] === 'home') { ?>\n"
        '<link rel="stylesheet" href="/' + ASSET + '?v=' + VERSION + '">\n'
        '<?php } ?>\n')


def patch_main(data):
    text = data.decode('utf-8')
    if MARKER in text:
        if text.count(LINK) != 1:
            raise ValueError('Existing home style marker was edited; update refused')
        return data
    if 'lireate-home-hero.css' not in text or 'lireate-home-dark' not in text:
        raise ValueError('Expected the existing Lireate home template')
    ends = list(re.finditer(r'</head\s*>', text, re.I))
    if len(ends) != 1:
        raise ValueError('Expected one closing head tag')
    pos = ends[0].start()
    prefix = text[:pos]
    if prefix.rfind('<?') > prefix.rfind('?>'):
        raise ValueError('Head closing tag is inside PHP; update refused')
    return (prefix + LINK + text[pos:]).encode('utf-8')


def target(docroot, relative):
    path = docroot / relative
    # No symlinked file or parent may redirect a write outside the chosen root.
    for item in [path] + list(path.parents):
        if item == docroot:
            break
        if item.is_symlink():
            raise ValueError('Symlink target refused: ' + relative)
    path.resolve().relative_to(docroot.resolve())
    if not path.parent.is_dir() or (path.exists() and not path.is_file()):
        raise ValueError('Unexpected hosting path: ' + relative)
    return path


def read(path):
    return path.read_bytes() if path.exists() else None


def build_plan(docroot):
    main = target(docroot, MAIN)
    original = read(main)
    if original is None:
        raise ValueError('CMS main template is missing')
    updated = patch_main(original)
    css = (REPO / 'hosting-design' / ASSET).read_bytes()
    existing = read(target(docroot, ASSET))
    if existing is not None and existing != css:
        raise ValueError('Existing home stylesheet differs; update refused')
    if updated == original and existing is None:
        raise ValueError('Installed home stylesheet is missing; review required')
    plan = {}
    if existing != css:
        plan[ASSET] = css
    if updated != original:
        plan[MAIN] = updated
    return plan, {rel: read(target(docroot, rel)) for rel in plan}


def lint_main(path):
    proc = subprocess.run([pick_php_executable(), '-l', str(path)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise ValueError('Patched CMS template did not pass PHP syntax validation')


def apply_plan(docroot, plan, before, backup_root):
    backup = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'),
                                   dir=str(backup_root)))
    prepared, applied = {}, []
    receipt = {'version': VERSION, 'files': {}}
    try:
        for rel, data in plan.items():
            path = target(docroot, rel)
            if read(path) != before[rel]:
                raise ValueError('Concurrent hosting edit; update refused: ' + rel)
            key = Path(rel).name
            old = before[rel]
            if old is not None:
                saved = backup / key
                saved.write_bytes(old)
                saved.chmod(0o600)
            receipt['files'][rel] = {'before': digest(old) if old is not None else None,
                                     'after': digest(data), 'backup': key}
            mode = path.stat().st_mode & 0o777 if old is not None else 0o644
            prepared[rel] = stage(path, data, mode)
        if MAIN in prepared:
            lint_main(prepared[MAIN])
        saved_receipt = backup / 'receipt.json'
        saved_receipt.write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        saved_receipt.chmod(0o600)
        for rel, staged in prepared.items():
            path = target(docroot, rel)
            if read(path) != before[rel]:
                raise ValueError('Concurrent hosting edit; update refused: ' + rel)
            os.replace(str(staged), str(path))
            applied.append(rel)
    except Exception:
        for rel in reversed(applied):
            path = target(docroot, rel)
            if read(path) == plan[rel]:
                if before[rel] is None:
                    path.unlink()
                else:
                    os.replace(str(stage(path, before[rel], path.stat().st_mode & 0o777)), str(path))
        raise
    finally:
        for staged in prepared.values():
            if staged.exists():
                staged.unlink()
    return backup


def restore(docroot, backup):
    receipt = json.loads((backup / 'receipt.json').read_text(encoding='utf-8'))
    if receipt.get('version') != VERSION or not set(receipt['files']).issubset({MAIN, ASSET}):
        raise ValueError('Unexpected home backup receipt')
    old = {}
    for rel, item in receipt['files'].items():
        current = read(target(docroot, rel))
        if current is None or digest(current) != item['after']:
            raise ValueError('Hosting changed after installation; restore refused: ' + rel)
        if item['backup'] != Path(rel).name:
            raise ValueError('Unexpected backup path')
        data = (backup / item['backup']).read_bytes() if item['before'] is not None else None
        if data is not None and digest(data) != item['before']:
            raise ValueError('Backup checksum mismatch')
        old[rel] = data
    # Remove the link before removing its new stylesheet.
    for rel in [MAIN, ASSET]:
        if rel not in old:
            continue
        path = target(docroot, rel)
        if digest(path.read_bytes()) != receipt['files'][rel]['after']:
            raise ValueError('Concurrent hosting edit during restore')
        if old[rel] is None:
            path.unlink()
        else:
            os.replace(str(stage(path, old[rel], path.stat().st_mode & 0o777)), str(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--docroot', type=Path)
    parser.add_argument('--env-file', type=Path)
    parser.add_argument('--restore-backup', type=Path)
    args = parser.parse_args()
    home = Path(os.environ.get('LIREATE_AUTOPUB_HOME') or str(Path.home() / 'lireate-autopub')).resolve()
    load_dotenv(args.env_file or os.environ.get('LIREATE_ENV_FILE') or home / '.env', override=False)
    if (args.apply or args.restore_backup) and os.environ.get('LIREATE_ALLOW_PUBLISH', '').lower() not in ('yes', 'true', '1', 'on'):
        print('STATUS: HOME_UNSLOP_PUBLISH_DISABLED')
        return 0
    if args.apply and os.environ.get('LIREATE_HOME_UNSLOP', '').lower() in ('no', 'false', '0', 'off'):
        print('STATUS: HOME_UNSLOP_DISABLED')
        return 0
    raw_root = args.docroot or os.environ.get('LIREATE_DOCROOT')
    if not raw_root:
        raise ValueError('LIREATE_DOCROOT is required')
    docroot = Path(raw_root).resolve()
    backup_root = home / 'backups/home-unslop'
    state_root = home / 'state'
    for path in (backup_root, state_root):
        if path == docroot or docroot in path.parents:
            raise ValueError('Backup and lock directories must be outside docroot')
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
    with lock(state_root / 'home-unslop.lock'):
        if args.restore_backup:
            backup = args.restore_backup.resolve()
            backup.relative_to(backup_root.resolve())
            restore(docroot, backup)
            print('STATUS: HOME_UNSLOP_RESTORED')
            return 0
        plan, before = build_plan(docroot)
        print(json.dumps({'version': VERSION, 'files': list(plan), 'apply': args.apply}))
        if not args.apply:
            print('STATUS: HOME_UNSLOP_DRY_RUN')
        elif plan:
            backup = apply_plan(docroot, plan, before, backup_root)
            print('STATUS: HOME_UNSLOP_APPLIED; backup: ' + str(backup))
        else:
            print('STATUS: HOME_UNSLOP_ALREADY_APPLIED')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError) as exc:
        print('STATUS: HOME_UNSLOP_FAILED: ' + str(exc))
        raise SystemExit(1)
