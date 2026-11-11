#!/usr/bin/env bash
# CI: v1 main fixture → dock v2 patch → php -l, line count, idempotent 2nd run.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-python3}"
FIXTURE="$REPO/tests/fixtures/main-php-v117-service-dock-v1.php"

"$PY" "$REPO/scripts/lireate_design_dock_main_fixture.py"
cp -a "$FIXTURE" "${FIXTURE}.orig"

export LIREATE_MAIN_MIN_LINES=6000
# shellcheck source=scripts/lireate_main_php_guard.sh
source "$REPO/scripts/lireate_main_php_guard.sh"

WORK="${FIXTURE}.work"
cp -a "$FIXTURE" "$WORK"
"$PY" "$REPO/scripts/lireate_design_patch_service_mobile_dock.py" "$WORK"
lireate_main_php_guard "$WORK"
php -l "$WORK" >/dev/null
grep -q 'lireate_design_service_mobile_dock_v2 body' "$WORK"
! grep -q 'lireate_design_service_mobile_dock_v1 body' "$WORK" || {
  echo "FAIL: v1 body marker still present" >&2
  exit 1
}

cp -a "$WORK" "${WORK}.once"
"$PY" "$REPO/scripts/lireate_design_patch_service_mobile_dock.py" "$WORK"
diff -q "${WORK}.once" "$WORK" || {
  echo "FAIL: second patch run changed file (not idempotent)" >&2
  exit 1
}
lireate_main_php_guard "$WORK"

echo "SERVICE_MOBILE_DOCK_SELFTEST_OK"
