#!/usr/bin/env bash
# Sync autopub repo to origin/<branch> (creates local branch if missing — типично после clone feature-ветки).
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
REPO_DIR="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"
BRANCH="${LIREATE_REPO_BRANCH:-main}"
REMOTE="${LIREATE_REPO_REMOTE:-origin}"

if [[ ! -d "$REPO_DIR/.git" ]]; then
  echo "ERROR: not a git repo: $REPO_DIR" >&2
  exit 1
fi

cd "$REPO_DIR"
git fetch "$REMOTE" "$BRANCH"

if git show-ref --verify --quiet "refs/remotes/$REMOTE/$BRANCH"; then
  git checkout -B "$BRANCH" "$REMOTE/$BRANCH"
else
  echo "ERROR: remote ref $REMOTE/$BRANCH not found after fetch" >&2
  exit 1
fi

git pull --ff-only "$REMOTE" "$BRANCH" || true
echo "OK synced to $REMOTE/$BRANCH at $(git rev-parse --short HEAD)"
