#!/usr/bin/env bash
# Step 3: hero main_back patches — guard + verify + rollback.
set -euo pipefail

REPO="${LIREATE_REPO_DIR:-$HOME/lireate-autopub/repo}"
DOCROOT="${LIREATE_DOCROOT:?}"
MAIN="$DOCROOT/template/main.php"
PY="$(command -v python3)"
LIREATE_MAIN_MIN_LINES="${LIREATE_MAIN_MIN_LINES:-6000}"

source "$REPO/scripts/lireate_main_php_guard.sh"

rollback_main() {
  local pre="${MAIN}.pre-heroes-patch"
  if [[ -f "$pre" ]]; then
    cp -a "$pre" "$MAIN"
    lireate_main_php_touch "$MAIN"
  fi
}

lireate_main_php_guard "$MAIN" || exit 1
cp -a "$MAIN" "${MAIN}.pre-heroes-patch"

if ! "$PY" "$REPO/scripts/lireate_design_patch_heroes.py" "$MAIN"; then
  rollback_main
  exit 1
fi

lireate_main_php_guard "$MAIN" || { rollback_main; exit 1; }
lireate_main_php_touch "$MAIN"

bash "$REPO/scripts/lireate_design_post_deploy_verify.sh"
echo "HERO_PATCH_OK lines=$(wc -l <"$MAIN")"
