#!/usr/bin/env bash
# Design deploy — CSS/JS + OPTIONAL safe main.php patch. Backups *.bak-2026-11-11-design
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
MAIN_REPO="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"
DESIGN_WT="${LIREATE_DESIGN_WORKTREE:-$AUTOPUB_HOME/design-wt}"
# Источник файлов design — worktree, не основной repo (CRON держит main).
REPO="$DESIGN_WT"
DOCROOT="${LIREATE_DOCROOT:-$HOME/www/public_html}"
_LIREATE_DEFAULT_SITE_URL="https://lireate.ru" # pragma: allowlist secret
export LIREATE_PUBLIC_SITE_URL="${LIREATE_PUBLIC_SITE_URL:-$_LIREATE_DEFAULT_SITE_URL}"
BAK="bak-2026-11-11-design"
PY="$(command -v python3)"
APPLY_MAIN_PATCH="${LIREATE_DESIGN_PATCH_MAIN:-0}"
APPLY_HOME_PATCH="${LIREATE_DESIGN_PATCH_HOME:-0}"

# shellcheck source=scripts/lireate_main_php_guard.sh
source "$REPO/scripts/lireate_main_php_guard.sh"
# shellcheck source=scripts/lireate_design_main_php_patch_lib.sh
source "$REPO/scripts/lireate_design_main_php_patch_lib.sh"
export LIREATE_DESIGN_BAK_SUFFIX="$BAK"
export LIREATE_DESIGN_PYTHON="$PY"

bak() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  cp -a "$f" "${f}.${BAK}"
}

rollback_main() {
  lireate_design_rollback_main "$1" "$BAK" || true
}

if [[ ! -d "$REPO" ]]; then
  echo "Design worktree missing; run: bash $MAIN_REPO/scripts/lireate_design_worktree_init.sh" >&2
  exit 1
fi
cd "$REPO"
TRACK="${LIREATE_DESIGN_TRACK:-main}"
DEPLOY_BRANCH="${LIREATE_DESIGN_BRANCH:-design-deploy}"
if [[ "${LIREATE_SKIP_GIT_FETCH:-0}" != "1" ]]; then
  git fetch origin "+$TRACK:refs/remotes/origin/$TRACK"
  git checkout "$DEPLOY_BRANCH" 2>/dev/null || true
  git merge --ff-only "origin/$TRACK" 2>/dev/null || git reset --hard "origin/$TRACK"
fi

CSS_DST="$DOCROOT/template/css"
mkdir -p "$CSS_DST"
for f in lireate-cms-page-dark.css lireate-cms-lu.css lireate-mktu-lu.css lireate-home-dark.css lireate-home-hero.css lireate-ux-fixes.css lireate-lu-viewport.css lireate-home-modal-lu.css lireate-legacy-article-lu.css lireate-legacy-cms-lu.css lireate-static-pages-lu.css lireate-service-mobile-bar.css; do
  src="$REPO/hosting-design/template/css/$f"
  [[ -f "$src" ]] || { echo "missing $src" >&2; exit 1; }
  bak "$CSS_DST/$f"
  cp -a "$src" "$CSS_DST/$f"
done

for js_f in lireate-floating-widget-ux.js lireate-static-hero-lu.js lireate-service-mobile-bar.js lireate-service-metrika-goals.js; do
  JS_DST="$DOCROOT/template/js/$js_f"
  src_js="$REPO/hosting-design/template/js/$js_f"
  if [[ -f "$src_js" ]]; then
    bak "$JS_DST"
    mkdir -p "$(dirname "$JS_DST")"
    cp -a "$src_js" "$JS_DST"
  fi
done

LIREATE_INC_DST="$DOCROOT/template/lireate/lireate-service-mobile-bar.inc.php"
LIREATE_INC_SRC="$REPO/hosting-design/template/lireate/lireate-service-mobile-bar.inc.php"
if [[ -f "$LIREATE_INC_SRC" ]]; then
  mkdir -p "$(dirname "$LIREATE_INC_DST")"
  bak "$LIREATE_INC_DST"
  cp -a "$LIREATE_INC_SRC" "$LIREATE_INC_DST"
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
MAIN_PRE_APPLY="${MAIN}.${BAK}-pre-apply"
main_php_will_patch() {
  [[ "${LIREATE_DESIGN_PATCH_MAIN:-0}" == "1" ]] && return 0
  [[ "${LIREATE_DESIGN_PATCH_NEWS_LU:-0}" == "1" ]] && return 0
  [[ "${LIREATE_DESIGN_PATCH_LEGACY_CMS:-0}" == "1" ]] && return 0
  [[ "${LIREATE_DESIGN_PATCH_GLOBAL_UX:-0}" == "1" ]] && return 0
  [[ "${LIREATE_DESIGN_PATCH_STATIC:-0}" == "1" ]] && return 0
  [[ "${LIREATE_DESIGN_PATCH_SERVICE_DOCK:-0}" == "1" ]] && return 0
  [[ "${LIREATE_DESIGN_PATCH_HOME_SERVICE_URLS:-0}" == "1" ]] && return 0
  [[ "${LIREATE_DESIGN_PATCH_CMS:-0}" == "1" ]] && return 0
  [[ "$APPLY_HOME_PATCH" == "1" ]] && return 0
  return 1
}

if main_php_will_patch && [[ -f "$MAIN" ]]; then
  cp -a "$MAIN" "$MAIN_PRE_APPLY"
  echo "MAIN_PRE_APPLY_SNAPSHOT $MAIN_PRE_APPLY" >&2
fi

if [[ "$APPLY_MAIN_PATCH" == "1" ]]; then
  [[ -f "$MAIN" ]] || { echo "main.php missing" >&2; exit 1; }
  if ! lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_main.py" "design_main"; then
    exit 1
  fi

  if grep -q 'lireate-ux-fixes.css?v=' "$MAIN"; then
    sed -i 's|lireate-ux-fixes.css?v=[^"]*|lireate-ux-fixes.css?v=20261111design4|g' "$MAIN"
  fi
  sed -i 's|lireate-home-dark.css?v=[^"]*|lireate-home-dark.css?v=20261111design6b|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-home-hero.css?v=[^"]*|lireate-home-hero.css?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-home-hero.js?v=[^"]*|lireate-home-hero.js?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-cms-page-dark.css?v=[^"]*|lireate-cms-page-dark.css?v=20261111design3|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-floating-widget-ux.js?v=[^"]*|lireate-floating-widget-ux.js?v=20261111design4|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-static-pages-lu.css?v=[^"]*|lireate-static-pages-lu.css?v=20261111static3|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-lu-viewport.css?v=[^"]*|lireate-lu-viewport.css?v=20261111vp5|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-static-hero-lu.js?v=[^"]*|lireate-static-hero-lu.js?v=20261111static3|g' "$MAIN" 2>/dev/null || true

else
  echo "SKIP_MAIN_PATCH (set LIREATE_DESIGN_PATCH_MAIN=1 to patch main.php)"
  if [[ -f "$MAIN" ]]; then
    lireate_main_php_guard "$MAIN" || exit 1
    sed -i 's|lireate-ux-fixes.css?v=[^"]*|lireate-ux-fixes.css?v=20261111design4|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-home-dark.css?v=[^"]*|lireate-home-dark.css?v=20261111design6b|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-home-hero.css?v=[^"]*|lireate-home-hero.css?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-home-hero.js?v=[^"]*|lireate-home-hero.js?v=20261111hero2|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-floating-widget-ux.js?v=[^"]*|lireate-floating-widget-ux.js?v=20261111design4|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-static-pages-lu.css?v=[^"]*|lireate-static-pages-lu.css?v=20261111static3|g' "$MAIN" 2>/dev/null || true
  sed -i 's|lireate-lu-viewport.css?v=[^"]*|lireate-lu-viewport.css?v=20261111vp5|g' "$MAIN" 2>/dev/null || true
    sed -i 's|lireate-static-hero-lu.js?v=[^"]*|lireate-static-hero-lu.js?v=20261111static3|g' "$MAIN" 2>/dev/null || true
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

if [[ "${LIREATE_DESIGN_PATCH_NEWS_LU:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_news_lu.py" "news_lu" || exit 1
fi

if [[ "${LIREATE_DESIGN_PATCH_LEGACY_CMS:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_legacy_cms_services.py" "legacy_cms" || exit 1
fi

if [[ "${LIREATE_DESIGN_PATCH_GLOBAL_UX:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_global_ux.py" "global_ux" || exit 1
fi

if [[ "${LIREATE_DESIGN_PATCH_STATIC:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_static_lu.py" "static_lu" || exit 1
fi

if [[ "${LIREATE_DESIGN_PATCH_SERVICE_DOCK:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_service_mobile_dock.py" "service_dock" || exit 1
fi

if [[ "${LIREATE_DESIGN_DEPLOY_NEW_SERVICES:-0}" == "1" ]]; then
  if ! "$PY" "$REPO/scripts/lireate_design_deploy_service_landings.py" "$DOCROOT" "$REPO"; then
    echo "DEPLOY_NEW_SERVICES_FAIL" >&2
    exit 1
  fi
  if [[ -f "$DOCROOT/.htaccess" ]]; then
    "$PY" "$REPO/scripts/lireate_design_patch_root_htaccess_services.py" "$DOCROOT/.htaccess" \
      || echo "ROOT_HTACCESS_PATCH_WARN" >&2
  fi
fi

if [[ "${LIREATE_DESIGN_PATCH_SERVICE_LANDINGS:-0}" == "1" ]]; then
  if ! "$PY" "$REPO/scripts/lireate_design_patch_service_landings.py" "$DOCROOT" "$REPO"; then
    echo "SERVICE_LANDINGS_PATCH_FAIL" >&2
    exit 1
  fi
fi

if [[ "${LIREATE_DESIGN_PATCH_HOME_SERVICE_URLS:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_home_service_urls.py" "home_svc_urls" || exit 1
fi

if [[ "${LIREATE_DESIGN_PATCH_USLUGI_CARDS:-0}" == "1" ]]; then
  "$PY" "$REPO/scripts/lireate_design_patch_uslugi_cards.py" "$DOCROOT" || echo "USLUGI_CARDS_PATCH_WARN" >&2
fi

if [[ "${LIREATE_DESIGN_PATCH_ROOT_HTACCESS:-0}" == "1" && -f "$DOCROOT/.htaccess" ]]; then
  "$PY" "$REPO/scripts/lireate_design_patch_root_htaccess_services.py" "$DOCROOT/.htaccess" \
    || echo "ROOT_HTACCESS_PATCH_WARN" >&2
fi

if [[ "${LIREATE_DESIGN_PATCH_CMS:-0}" == "1" && -f "$MAIN" ]]; then
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_cms_pages.py" "cms_pages" || exit 1
fi

if [[ "$APPLY_HOME_PATCH" == "1" ]]; then
  [[ -f "$MAIN" ]] || { echo "main.php missing for home patch" >&2; exit 1; }
  lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_home.py" "home" || exit 1
else
  echo "SKIP_HOME_PATCH (set LIREATE_DESIGN_PATCH_HOME=1 for blog/footer on home)"
fi

if [[ -x "$REPO/scripts/lireate_design_post_deploy_verify.sh" ]]; then
  export REPO LIREATE_DOCROOT
  if ! bash "$REPO/scripts/lireate_design_post_deploy_verify.sh"; then
    if [[ -f "$MAIN_PRE_APPLY" ]]; then
      cp -a "$MAIN_PRE_APPLY" "$MAIN"
      lireate_main_php_touch "$MAIN"
      echo "MAIN_ROLLBACK_PRE_APPLY_OK from $MAIN_PRE_APPLY" >&2
    elif [[ -f "$MAIN" ]]; then
      rollback_main "$MAIN"
    fi
    exit 1
  fi
fi

echo "DESIGN_APPLY_OK docroot=$DOCROOT"
