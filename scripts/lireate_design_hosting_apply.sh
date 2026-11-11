#!/usr/bin/env bash
# Design deploy — CSS/JS + OPTIONAL safe main.php patch. Backups *.bak-2026-11-11-design
set -euo pipefail

REPO="${LIREATE_REPO_DIR:-$HOME/lireate-autopub/repo}"
DOCROOT="${LIREATE_DOCROOT:?}"
BAK="bak-2026-11-11-design"
PY="$(command -v python3)"
APPLY_MAIN_PATCH="${LIREATE_DESIGN_PATCH_MAIN:-0}"
APPLY_HOME_PATCH="${LIREATE_DESIGN_PATCH_HOME:-0}"

# shellcheck source=scripts/lireate_main_php_guard.sh
source "$REPO/scripts/lireate_main_php_guard.sh"

bak() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  cp -a "$f" "${f}.${BAK}"
}

rollback_main() {
  local main="$1"
  local pre="${main}.pre-design-patch"
  if [[ -f "$pre" ]]; then
    cp -a "$pre" "$main"
    lireate_main_php_touch "$main"
    echo "MAIN_ROLLBACK_OK" >&2
  fi
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

HOME_INC_DST="$DOCROOT/template/page/home/lireate-home-blog-teaser.inc.php"
HOME_INC_SRC="$REPO/hosting-design/template/page/home/lireate-home-blog-teaser.inc.php"
if [[ -f "$HOME_INC_SRC" ]]; then
  mkdir -p "$(dirname "$HOME_INC_DST")"
  bak "$HOME_INC_DST"
  cp -a "$HOME_INC_SRC" "$HOME_INC_DST"
fi

MAIN="$DOCROOT/template/main.php"
if [[ "$APPLY_MAIN_PATCH" == "1" ]]; then
  [[ -f "$MAIN" ]] || { echo "main.php missing" >&2; exit 1; }
  lireate_main_php_guard "$MAIN" || { echo "MAIN_GUARD_PRE_FAIL" >&2; exit 1; }

  bak "$MAIN"
  cp -a "$MAIN" "${MAIN}.pre-design-patch"

  if ! "$PY" "$REPO/scripts/lireate_design_patch_main.py" "$MAIN"; then
    rollback_main "$MAIN"
    exit 1
  fi

  lireate_main_php_guard "$MAIN" || {
    rollback_main "$MAIN"
    echo "MAIN_GUARD_POST_FAIL" >&2
    exit 1
  }

  lireate_main_php_touch "$MAIN"

  if grep -q 'lireate-ux-fixes.css?v=' "$MAIN"; then
    sed -i 's|lireate-ux-fixes.css?v=[^"]*|lireate-ux-fixes.css?v=20261111design4|g' "$MAIN"
  fi
  sed -i 's|lireate-home-dark.css?v=[^"]*|lireate-home-dark.css?v=20261111design5|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-cms-page-dark.css?v=[^"]*|lireate-cms-page-dark.css?v=20261111design3|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-floating-widget-ux.js?v=[^"]*|lireate-floating-widget-ux.js?v=20261111design4|g' "$MAIN" 2>/dev/null || true

  lireate_main_php_guard "$MAIN" || {
    rollback_main "$MAIN"
    exit 1
  }
  lireate_main_php_touch "$MAIN"
else
  echo "SKIP_MAIN_PATCH (set LIREATE_DESIGN_PATCH_MAIN=1 to patch main.php)"
  if [[ -f "$MAIN" ]]; then
    lireate_main_php_guard "$MAIN" || exit 1
    sed -i 's|lireate-ux-fixes.css?v=[^"]*|lireate-ux-fixes.css?v=20261111design4|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-home-dark.css?v=[^"]*|lireate-home-dark.css?v=20261111design5|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-floating-widget-ux.js?v=[^"]*|lireate-floating-widget-ux.js?v=20261111design4|g' "$MAIN" 2>/dev/null || true
    lireate_main_php_guard "$MAIN" || exit 1
    lireate_main_php_touch "$MAIN"
  fi
fi

if [[ "$APPLY_HOME_PATCH" == "1" ]]; then
  [[ -f "$MAIN" ]] || { echo "main.php missing for home patch" >&2; exit 1; }
  lireate_main_php_guard "$MAIN" || exit 1
  bak "$MAIN"
  if ! "$PY" "$REPO/scripts/lireate_design_patch_home.py" "$MAIN"; then
    echo "HOME_PATCH_FAIL" >&2
    exit 1
  fi
  lireate_main_php_guard "$MAIN" || exit 1
  lireate_main_php_touch "$MAIN"
else
  echo "SKIP_HOME_PATCH (set LIREATE_DESIGN_PATCH_HOME=1 for blog/footer on home)"
fi

if [[ -x "$REPO/scripts/lireate_design_post_deploy_verify.sh" ]]; then
  if ! bash "$REPO/scripts/lireate_design_post_deploy_verify.sh"; then
    if [[ "$APPLY_MAIN_PATCH" == "1" ]]; then
      rollback_main "$MAIN"
    fi
    exit 1
  fi
fi

echo "DESIGN_APPLY_OK docroot=$DOCROOT"
