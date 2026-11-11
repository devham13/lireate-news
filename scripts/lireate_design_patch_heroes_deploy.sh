#!/usr/bin/env bash
# Step 3: hero main_back patches — guard + verify + rollback.
set -euo pipefail

REPO="${LIREATE_REPO_DIR:-$HOME/lireate-autopub/repo}"
DOCROOT="${LIREATE_DOCROOT:-$HOME/www/public_html}"
MAIN="$DOCROOT/template/main.php"
PY="$(command -v python3)"
LIREATE_MAIN_MIN_LINES="${LIREATE_MAIN_MIN_LINES:-6000}"
BAK="bak-2026-11-11-design"

source "$REPO/scripts/lireate_main_php_guard.sh"
# shellcheck source=scripts/lireate_design_main_php_patch_lib.sh
source "$REPO/scripts/lireate_design_main_php_patch_lib.sh"
export LIREATE_DESIGN_BAK_SUFFIX="$BAK"
export LIREATE_DESIGN_PYTHON="$PY"

lireate_design_patch_main_php "$MAIN" "$REPO/scripts/lireate_design_patch_heroes.py" "heroes" || exit 1

bash "$REPO/scripts/lireate_design_post_deploy_verify.sh"
echo "HERO_PATCH_OK lines=$(wc -l <"$MAIN")"
