#!/usr/bin/env bash
# Отдельный worktree для дизайн-деплоя — основной ~/lireate-autopub/repo остаётся на main (CRON).
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
MAIN_REPO="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"
DESIGN_WT="${LIREATE_DESIGN_WORKTREE:-$AUTOPUB_HOME/design-wt}"
TRACK_BRANCH="${LIREATE_DESIGN_TRACK:-main}"
DEPLOY_BRANCH="${LIREATE_DESIGN_BRANCH:-design-deploy}"

[[ -d "$MAIN_REPO/.git" ]] || { echo "missing git repo: $MAIN_REPO" >&2; exit 1; }

git -C "$MAIN_REPO" fetch origin "$TRACK_BRANCH"

if [[ -d "$DESIGN_WT" ]]; then
  git -C "$MAIN_REPO" worktree remove -f "$DESIGN_WT" 2>/dev/null || rm -rf "$DESIGN_WT"
fi

if ! git -C "$MAIN_REPO" show-ref --verify --quiet "refs/heads/$DEPLOY_BRANCH"; then
  git -C "$MAIN_REPO" branch -f "$DEPLOY_BRANCH" "origin/$TRACK_BRANCH"
fi

git -C "$MAIN_REPO" worktree add -f "$DESIGN_WT" "$DEPLOY_BRANCH"
git -C "$DESIGN_WT" merge --ff-only "origin/$TRACK_BRANCH" 2>/dev/null || \
  git -C "$DESIGN_WT" reset --hard "origin/$TRACK_BRANCH"

echo "DESIGN_WORKTREE_OK path=$DESIGN_WT branch=$DEPLOY_BRANCH tracks=origin/$TRACK_BRANCH"
echo "Use: LIREATE_DESIGN_WORKTREE=$DESIGN_WT bash $MAIN_REPO/scripts/lireate_design_hosting_apply.sh"
