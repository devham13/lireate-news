#!/usr/bin/env bash
# REG.RU CRON entry: pull latest article from git, then publish or update CMS row.
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
ENV_FILE="${LIREATE_ENV_FILE:-$AUTOPUB_HOME/.env}"
REPO_DIR="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"
BRANCH="${LIREATE_REPO_BRANCH:-main}"
PY="$(cat "$AUTOPUB_HOME/.python-interpreter")"
LOG_DIR="$AUTOPUB_HOME/logs"
mkdir -p "$LOG_DIR"

export LIREATE_AUTOPUB_HOME="$AUTOPUB_HOME"
export LIREATE_ENV_FILE="$ENV_FILE"

if [[ -d "$REPO_DIR/.git" ]]; then
  cd "$REPO_DIR"
  git fetch origin "$BRANCH" 2>>"$LOG_DIR/cron-git.log" || true
  git checkout "$BRANCH" 2>>"$LOG_DIR/cron-git.log" || true
  git pull --ff-only origin "$BRANCH" 2>>"$LOG_DIR/cron-git.log" || true
fi

# After first publish the URL is 200 — refresh text/images from git (--update bumps datetime).
exec "$PY" "$REPO_DIR/scripts/lireate_hosting_publish.py" --update "$@"
