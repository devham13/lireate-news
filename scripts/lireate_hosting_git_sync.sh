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
# Shallow/feature clone: после `git fetch origin main` часто есть только FETCH_HEAD, без refs/remotes/origin/main
git fetch "$REMOTE" "+refs/heads/${BRANCH}:refs/heads/${BRANCH}"
git fetch "$REMOTE" "+refs/heads/${BRANCH}:refs/remotes/${REMOTE}/${BRANCH}" 2>/dev/null || true
git checkout -B "$BRANCH" "$BRANCH"
git pull --ff-only "$REMOTE" "$BRANCH" 2>/dev/null || true
echo "OK synced to $REMOTE/$BRANCH at $(git rev-parse --short HEAD)"
