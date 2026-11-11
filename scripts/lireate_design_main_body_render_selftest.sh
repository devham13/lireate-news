#!/usr/bin/env bash
# After full deploy patch chain: body class PHP must echo expected LU markers.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
RENDER="$REPO/scripts/lireate_design_main_body_class_render.php"
WORK="$REPO/tests/fixtures/main-php-v120-dock-v2-body-drift.php.deploy-chain"
[[ -f "$WORK" ]] || bash "$REPO/scripts/lireate_design_full_deploy_main_selftest.sh" >/dev/null

run_render() {
  local page="$1" uri="$2"
  php "$RENDER" "$WORK" "$page" "$uri"
}

home_plain="$(run_render home /)"
home_q="$(run_render home '/?lireate_verify=1')"
echo "$home_plain" | grep -q 'lireate-home-dark' || { echo "FAIL home plain: $home_plain" >&2; exit 1; }
echo "$home_q" | grep -q 'lireate-home-dark' || { echo "FAIL home query: $home_q" >&2; exit 1; }

reviews="$(run_render reviews '/reviews?lireate_verify=1')"
echo "$reviews" | grep -q 'lireate-static-lu' || { echo "FAIL reviews query: $reviews" >&2; exit 1; }

poisk="$(run_render poisk_tovarnyh_znakov '/poisk_tovarnyh_znakov/?lireate_verify=1')"
echo "$poisk" | grep -q 'lireate-legacy-cms-lu' || { echo "FAIL poisk query: $poisk" >&2; exit 1; }

echo "MAIN_BODY_RENDER_SELFTEST_OK"
