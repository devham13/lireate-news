#!/usr/bin/env bash
# Simulate #132 deploy main.php patch chain on live-shaped fixture.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=scripts/lireate_design_resolve_python.sh
source "$REPO/scripts/lireate_design_resolve_python.sh"
PY="${PYTHON:-$(lireate_design_resolve_python)}"
if ! "$PY" -c 'import sys; assert sys.version_info >= (3, 8)' 2>/dev/null; then
  PY=python3
fi

export LIREATE_DESIGN_PYTHON="$PY"
export REPO
export LIREATE_DESIGN_BAK_SUFFIX="bak-selftest"
# shellcheck source=scripts/lireate_design_main_php_patch_lib.sh
source "$REPO/scripts/lireate_design_main_php_patch_lib.sh"
# shellcheck source=scripts/lireate_main_php_guard.sh
source "$REPO/scripts/lireate_main_php_guard.sh"

"$PY" "$REPO/scripts/lireate_design_dock_main_fixture.py" 2>/dev/null || true
BASE="$REPO/tests/fixtures/main-php-v120-dock-v2-body-drift.php"
if [[ ! -f "$BASE" ]]; then
  BASE="$REPO/tests/fixtures/main-php-v117-service-dock-v1.php"
fi
WORK="${BASE}.deploy-chain"
cp -a "$BASE" "$WORK"

run_patch() {
  local py="$1" label="$2"
  lireate_design_patch_main_php "$WORK" "$py" "$label"
}

run_patch "$REPO/scripts/lireate_design_patch_news_lu.py" "news_lu"
run_patch "$REPO/scripts/lireate_design_patch_legacy_cms_services.py" "legacy_cms"
run_patch "$REPO/scripts/lireate_design_patch_global_ux.py" "global_ux"
run_patch "$REPO/scripts/lireate_design_patch_static_lu.py" "static_lu"
if ! grep -q 'lireate_design_service_mobile_dock_v2 body' "$WORK"; then
  run_patch "$REPO/scripts/lireate_design_patch_service_mobile_dock.py" "service_dock"
fi
if grep -q 'var lurl = \[\[' "$WORK"; then
  run_patch "$REPO/scripts/lireate_design_patch_home_service_urls.py" "home_svc_urls"
  grep -q 'lireate_design_home_service_urls_v1' "$WORK"
fi

grep -q 'lireate_design_legacy_cms_services_v1 body' "$WORK"
grep -q 'lireate-legacy-cms-lu' "$WORK"
php -l "$WORK" >/dev/null

"$PY" - <<PY
from pathlib import Path
import re
t = Path("$WORK").read_text(encoding="utf-8")
assert "lireate-legacy-cms-lu" in t
assert re.search(r"preg_match\(.+poisk_tovarnyh_znakov", t), "poisk URI regex missing"
print("POISK_LEGACY_SNIPPET_OK")
PY

echo "FULL_DEPLOY_MAIN_SELFTEST_OK"
