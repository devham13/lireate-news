#!/usr/bin/env bash
# Запуск с любого каталога (в т.ч. ~): sync git + publish --update.
# Usage: bash ~/lireate-autopub/repo/scripts/lireate_hosting_operator.sh
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
REPO_DIR="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"

if [[ ! -d "$REPO_DIR/.git" ]]; then
  echo "ERROR: git repo not found: $REPO_DIR" >&2
  echo "Install: curl -fsSL .../lireate_hosting_install.sh | bash" >&2
  exit 1
fi

export LIREATE_AUTOPUB_HOME="$AUTOPUB_HOME"
export LIREATE_ENV_FILE="${LIREATE_ENV_FILE:-$AUTOPUB_HOME/.env}"

SYNC="$REPO_DIR/scripts/lireate_hosting_git_sync.sh"
CRON="$REPO_DIR/scripts/lireate_hosting_cron.sh"

if [[ -x "$SYNC" ]]; then
  bash "$SYNC"
else
  cd "$REPO_DIR"
  git fetch origin main
  git checkout -B main origin/main
  git pull --ff-only origin main || true
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: missing $ENV_FILE" >&2
  exit 1
fi

if ! grep -qE '^LIREATE_ALLOW_PUBLISH=(yes|1|true|on)' "$ENV_FILE" 2>/dev/null; then
  echo "WARN: set LIREATE_ALLOW_PUBLISH=yes in $ENV_FILE before live publish" >&2
fi

exec bash "$CRON"
