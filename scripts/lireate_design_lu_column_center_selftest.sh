#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
grep -q 'lireate_wide_center_hotfix_v2' "$REPO/hosting-design/template/css/lireate-lu-viewport.css"
grep -q 'margin-left: auto !important' "$REPO/hosting-design/template/css/lireate-lu-viewport.css"
grep -q '@media (min-width: 1500px)' "$REPO/hosting-design/template/css/lireate-lu-viewport.css"
if [[ "${LIREATE_LU_COLUMN_CENTER_LIVE_CHECK:-0}" == "1" ]] && command -v node >/dev/null && node -e "require('playwright')" 2>/dev/null; then
  : "${LIREATE_PUBLIC_SITE_URL:?set LIREATE_PUBLIC_SITE_URL for live check}"
  node "$REPO/scripts/lireate_design_lu_column_center_check.mjs" || {
    echo "LU_COLUMN_CENTER_CHECK_FAIL (live+injected CSS)" >&2
    exit 1
  }
fi
echo "LU_COLUMN_CENTER_SELFTEST_OK"
