#!/usr/bin/env bash
# Создаёт pages/services/_shared/lireate-messenger-urls.php → канон template/lireate/
# Запуск на REG.RU с LIREATE_DOCROOT в окружении или в ~/lireate-autopub/.env
set -euo pipefail

ENV_FILE="${LIREATE_ENV_FILE:-$HOME/lireate-autopub/.env}"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  set -a && source "$ENV_FILE" && set +a
fi
DOCROOT="${LIREATE_DOCROOT:?LIREATE_DOCROOT required}"
CANON="$DOCROOT/template/lireate/lireate-messenger-urls.php"
TARGET_DIR="$DOCROOT/pages/services/_shared"
TARGET="$TARGET_DIR/lireate-messenger-urls.php"
SUFFIX="${LIREATE_HOSTING_BAK_SUFFIX:-bak-2026-11-10-seo3}"

if [[ ! -f "$CANON" ]]; then
  echo "ERROR: canonical messenger file missing: $CANON" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"
if [[ -f "$TARGET" ]]; then
  cp -a "$TARGET" "$TARGET.$SUFFIX"
fi

cat >"$TARGET" <<PHP
<?php
/** Auto-generated shim — do not edit; see scripts/lireate_hosting_messenger_shim.sh */
require_once dirname(dirname(dirname(__DIR__))) . '/template/lireate/lireate-messenger-urls.php';
PHP

echo "OK: $TARGET -> template/lireate/lireate-messenger-urls.php"
