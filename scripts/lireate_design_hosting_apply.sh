#!/usr/bin/env bash
# Design deploy — CSS/JS + OPTIONAL safe main.php patch. Backups *.bak-2026-11-11-design
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
MAIN_REPO="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"
DESIGN_WT="${LIREATE_DESIGN_WORKTREE:-$AUTOPUB_HOME/design-wt}"
# Источник файлов design — worktree, не основной repo (CRON держит main).
REPO="$DESIGN_WT"
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

if [[ ! -d "$REPO" ]]; then
  echo "Design worktree missing; run: bash $MAIN_REPO/scripts/lireate_design_worktree_init.sh" >&2
  exit 1
fi
cd "$REPO"
BRANCH="${LIREATE_DESIGN_BRANCH:-cursor/home-v3-layout-fix-181e}"
if [[ "${LIREATE_SKIP_GIT_FETCH:-0}" != "1" ]]; then
  git fetch origin "$BRANCH"
  git checkout "$BRANCH" 2>/dev/null || true
  git pull --ff-only origin "$BRANCH" 2>/dev/null || {
    echo "WARN: could not ff-only pull $BRANCH (deploying current worktree HEAD)" >&2
  }
fi

CSS_DST="$DOCROOT/template/css"
mkdir -p "$CSS_DST"
for f in lireate-cms-page-dark.css lireate-cms-lu.css lireate-mktu-lu.css lireate-home-dark.css lireate-home-hero.css lireate-ux-fixes.css lireate-lu-viewport.css lireate-home-modal-lu.css lireate-legacy-article-lu.css lireate-legacy-cms-lu.css; do
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

HOME_DIR_DST="$DOCROOT/template/page/home"
HOME_DIR_SRC="$REPO/hosting-design/template/page/home"
mkdir -p "$HOME_DIR_DST"
for inc in lireate-home-blog-teaser.inc.php lireate-home-hero.inc.php lireate-home-url.inc.php lireate-home-lu.css; do
  if [[ -f "$HOME_DIR_SRC/$inc" ]]; then
    bak "$HOME_DIR_DST/$inc"
    cp -a "$HOME_DIR_SRC/$inc" "$HOME_DIR_DST/$inc"
  fi
done

JS_HERO_DST="$DOCROOT/template/js/lireate-home-hero.js"
JS_HERO_SRC="$REPO/hosting-design/template/js/lireate-home-hero.js"
if [[ -f "$JS_HERO_SRC" ]]; then
  bak "$JS_HERO_DST"
  cp -a "$JS_HERO_SRC" "$JS_HERO_DST"
fi

JS_MODAL_DST="$DOCROOT/template/js/lireate-home-modal-lu.js"
JS_MODAL_SRC="$REPO/hosting-design/template/js/lireate-home-modal-lu.js"
if [[ -f "$JS_MODAL_SRC" ]]; then
  bak "$JS_MODAL_DST"
  mkdir -p "$(dirname "$JS_MODAL_DST")"
  cp -a "$JS_MODAL_SRC" "$JS_MODAL_DST"
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
  sed -i 's|lireate-home-dark.css?v=[^"]*|lireate-home-dark.css?v=20261111design6b|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-home-hero.css?v=[^"]*|lireate-home-hero.css?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-home-hero.js?v=[^"]*|lireate-home-hero.js?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
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
    sed -i 's|lireate-home-dark.css?v=[^"]*|lireate-home-dark.css?v=20261111design6b|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-home-hero.css?v=[^"]*|lireate-home-hero.css?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-home-hero.js?v=[^"]*|lireate-home-hero.js?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-floating-widget-ux.js?v=[^"]*|lireate-floating-widget-ux.js?v=20261111design4|g' "$MAIN" 2>/dev/null || true
    lireate_main_php_guard "$MAIN" || exit 1
    lireate_main_php_touch "$MAIN"
  fi
fi

CMS_DIR_DST="$DOCROOT/template/page/cms"
CMS_DIR_SRC="$REPO/hosting-design/template/page/cms"
if [[ -d "$CMS_DIR_SRC" ]]; then
  mkdir -p "$CMS_DIR_DST"
  for inc in lireate-cms-hero-facts.inc.php lireate-cms-hero-patent.inc.php lireate-cms-hero-patent-prom.inc.php; do
  if [[ -f "$CMS_DIR_SRC/$inc" ]]; then
    bak "$CMS_DIR_DST/$inc"
    cp -a "$CMS_DIR_SRC/$inc" "$CMS_DIR_DST/$inc"
  fi
  done
fi

if [[ "${LIREATE_DESIGN_PATCH_CMS:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_main_php_guard "$MAIN" || exit 1
  bak "$MAIN"
  if ! "$PY" "$REPO/scripts/lireate_design_patch_cms_pages.py" "$MAIN"; then
    echo "CMS_PATCH_FAIL" >&2
    exit 1
  fi
  lireate_main_php_guard "$MAIN" || exit 1
  lireate_main_php_touch "$MAIN"
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
