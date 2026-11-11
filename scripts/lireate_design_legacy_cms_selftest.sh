#!/usr/bin/env bash
# dock v2 fixture → legacy_cms patch: body class + pagekey hide, idempotent.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-python3}"
FIXTURE="$REPO/tests/fixtures/main-php-v117-service-dock-v1.php"

"$PY" "$REPO/scripts/lireate_design_dock_main_fixture.py"
export LIREATE_MAIN_MIN_LINES=6000
# shellcheck source=scripts/lireate_main_php_guard.sh
source "$REPO/scripts/lireate_main_php_guard.sh"

WORK="${FIXTURE}.legacy-work"
cp -a "$FIXTURE" "$WORK"
"$PY" "$REPO/scripts/lireate_design_patch_service_mobile_dock.py" "$WORK"

# Simulate live leak after <body>
if ! grep -q pagekey "$WORK"; then
  sed -i "s|<main>Fixture|<?php echo \$temp['pagekey']; ?>\\n<main>Fixture|" "$WORK"
fi

"$PY" "$REPO/scripts/lireate_design_patch_legacy_cms_services.py" "$WORK"
lireate_main_php_guard "$WORK"
php -l "$WORK" >/dev/null
grep -q 'lireate_design_legacy_cms_services_v1 body' "$WORK"
grep -q 'lireate-legacy-cms-lu' "$WORK"
grep -q 'lireate_hide_pagekey_v1' "$WORK"
! grep -qE "echo[[:space:]]+\\\$temp\\['pagekey'\\]" "$WORK" || {
  echo "FAIL: pagekey still echoed" >&2
  exit 1
}

cp -a "$WORK" "${WORK}.once"
"$PY" "$REPO/scripts/lireate_design_patch_legacy_cms_services.py" "$WORK"
diff -q "${WORK}.once" "$WORK" || {
  echo "FAIL: second legacy patch run not idempotent" >&2
  exit 1
}

echo "LEGACY_CMS_SELFTEST_OK"
