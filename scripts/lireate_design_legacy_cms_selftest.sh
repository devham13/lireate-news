#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-python3}"
SNIP="$REPO/tests/fixtures/main-php-hosting-pagekey-inline.snippet.php"
LIVE_FIXTURE="$REPO/tests/fixtures/main-php-hosting-live-body-v1.php"

export LIREATE_MAIN_MIN_LINES=6000
# shellcheck source=scripts/lireate_main_php_guard.sh
source "$REPO/scripts/lireate_main_php_guard.sh"

"$PY" "$REPO/scripts/lireate_design_legacy_cms_live_fixture.py"

# Hosting fragment: echo inside open <?php (lines ~382–386)
SNIP_WORK="${SNIP}.work"
cp -a "$SNIP" "$SNIP_WORK"
"$PY" "$REPO/scripts/lireate_design_legacy_cms_pagekey_snippet_test.py" "$SNIP_WORK"

# Live-shaped main.php (body class block + inline pagekey)
LIVE_WORK="${LIVE_FIXTURE}.work"
cp -a "$LIVE_FIXTURE" "$LIVE_WORK"
"$PY" "$REPO/scripts/lireate_design_patch_legacy_cms_services.py" "$LIVE_WORK"
php -l "$LIVE_WORK" >/dev/null
grep -q 'lireate_design_legacy_cms_services_v1 body' "$LIVE_WORK"
grep -q 'lireate-home-dark' "$LIVE_WORK"
if grep -qE "echo[[:space:]]+\\\$temp\\['pagekey'\\]" "$LIVE_WORK"; then
  echo "FAIL: pagekey echo in live fixture" >&2
  exit 1
fi

# dock v2 chain (regression)
FIXTURE="$REPO/tests/fixtures/main-php-v117-service-dock-v1.php"
"$PY" "$REPO/scripts/lireate_design_dock_main_fixture.py"
WORK="${FIXTURE}.legacy-work"
cp -a "$FIXTURE" "$WORK"
"$PY" "$REPO/scripts/lireate_design_patch_service_mobile_dock.py" "$WORK"
"$PY" -c "
from pathlib import Path
block = \"\"\"    <?php 
    
        echo \$temp['pagekey'];
        include ('./template/parts/online.php');
    ?>
\"\"\"
p = Path('$WORK')
t = p.read_text(encoding='utf-8')
if 'online.php' not in t:
    t = t.replace('<main>Fixture', block + '<main>Fixture', 1)
    p.write_text(t, encoding='utf-8')
"
"$PY" "$REPO/scripts/lireate_design_patch_legacy_cms_services.py" "$WORK"
lireate_main_php_guard "$WORK"
php -l "$WORK" >/dev/null

cp -a "$LIVE_WORK" "${LIVE_WORK}.once"
"$PY" "$REPO/scripts/lireate_design_patch_legacy_cms_services.py" "$LIVE_WORK"
diff -q "${LIVE_WORK}.once" "$LIVE_WORK" || {
  echo "FAIL: legacy patch not idempotent on live fixture" >&2
  exit 1
}

echo "LEGACY_CMS_SELFTEST_OK"
