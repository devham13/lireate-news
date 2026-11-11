#!/usr/bin/env bash
# Home dark design deploy — backups *.bak-2026-11-11-design
set -euo pipefail

REPO="${LIREATE_REPO_DIR:-$HOME/lireate-autopub/repo}"
DOCROOT="${LIREATE_DOCROOT:?}"
BAK="bak-2026-11-11-design"
PY="$(command -v python3)"

bak() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  cp -a "$f" "${f}.${BAK}"
}

cd "$REPO"
git fetch origin main
git merge --ff-only origin/main

CSS_DST="$DOCROOT/template/css"
mkdir -p "$CSS_DST"
for f in lireate-cms-page-dark.css lireate-home-dark.css lireate-ux-fixes.css; do
  src="$REPO/hosting-design/template/css/$f"
  [[ -f "$src" ]] || { echo "missing $src" >&2; exit 1; }
  bak "$CSS_DST/$f"
  cp -a "$src" "$CSS_DST/$f"
done

JS_DST="$DOCROOT/template/js/lireate-floating-widget-ux.js"
src_js="$REPO/hosting-design/template/js/lireate-floating-widget-ux.js"
if [[ -f "$src_js" ]]; then
  bak "$JS_DST"
  cp -a "$src_js" "$JS_DST"
fi

MAIN="$DOCROOT/template/main.php"
[[ -f "$MAIN" ]] || { echo "main.php missing" >&2; exit 1; }
bak "$MAIN"
cp -a "$MAIN" "${MAIN}.pre-design-patch"
"$PY" "$REPO/scripts/lireate_design_patch_main.py" "$MAIN"
php -l "$MAIN" >/dev/null

# Bump ux-fixes query on main.php if present
if grep -q 'lireate-ux-fixes.css?v=' "$MAIN"; then
  sed -i 's|lireate-ux-fixes.css?v=[^"]*|lireate-ux-fixes.css?v=20261111design2|g' "$MAIN"
  php -l "$MAIN" >/dev/null
fi
sed -i 's|lireate-home-dark.css?v=[^"]*|lireate-home-dark.css?v=20261111design2|g' "$MAIN" 2>/dev/null || true
sed -i 's|lireate-floating-widget-ux.js?v=[^"]*|lireate-floating-widget-ux.js?v=20261111design2|g' "$MAIN" 2>/dev/null || true
php -l "$MAIN" >/dev/null

echo "DESIGN_APPLY_OK docroot=$DOCROOT"
