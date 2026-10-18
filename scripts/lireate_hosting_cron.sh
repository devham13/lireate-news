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
  SYNC="$REPO_DIR/scripts/lireate_hosting_git_sync.sh"
  if [[ -x "$SYNC" ]]; then
    bash "$SYNC" >>"$LOG_DIR/cron-git.log" 2>&1 || true
  else
    # Fallback until repo synced to a commit that contains git_sync.sh
    cd "$REPO_DIR"
    git fetch origin "$BRANCH" 2>>"$LOG_DIR/cron-git.log" || true
    git checkout -B "$BRANCH" "origin/$BRANCH" 2>>"$LOG_DIR/cron-git.log" || true
    git pull --ff-only origin "$BRANCH" 2>>"$LOG_DIR/cron-git.log" || true
  fi
fi

# Publish only the newest not-yet-published article; prints NO_NEW_ARTICLE and exits 0 otherwise.
# Never --update here: old articles are not rewritten by CRON.
exec "$PY" "$REPO_DIR/scripts/lireate_hosting_publish.py" "$@"
