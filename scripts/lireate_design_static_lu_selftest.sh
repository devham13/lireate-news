#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${LIREATE_DESIGN_PYTHON:-python3}"

"$PY" -c "
from pathlib import Path
import sys
sys.path.insert(0, '$REPO/scripts')
from lireate_design_main_php_sanitize import sanitize_main_php_head
from lireate_design_patch_static_lu import _upgrade_static_hero_js, HERO_JS

bad = '\t<script defer src=\"/template/js/lireate-static-hero-lu.js?v=20261111static3\"></script>\" />\\n'
assert '\" />' not in sanitize_main_php_head(bad)
print('SANITIZE_OK')

sample = (
    '\t<link rel=\"stylesheet\" href=\"/template/css/lireate-static-pages-lu.css?v=20261111static2\" />\\n'
)
out = sanitize_main_php_head(_upgrade_static_hero_js(sample))
assert HERO_JS in out
assert '</script>\" />' not in out
assert out.count('<link rel=\"stylesheet\" href=\"/template/css/lireate-static-pages-lu.css') == 1
print('UPGRADE_OK')
"

echo "STATIC_LU_SELFTEST_OK"
