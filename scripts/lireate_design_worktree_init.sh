#!/usr/bin/env bash
# Отдельный worktree для дизайн-деплоя — основной ~/lireate-autopub/repo остаётся на main (CRON).
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
MAIN_REPO="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"
DESIGN_WT="${LIREATE_DESIGN_WORKTREE:-$AUTOPUB_HOME/design-wt}"
BRANCH="${LIREATE_DESIGN_BRANCH:-main}"

[[ -d "$MAIN_REPO/.git" ]] || { echo "missing git repo: $MAIN_REPO" >&2; exit 1; }

git -C "$MAIN_REPO" fetch origin main "$BRANCH"

if [[ -d "$DESIGN_WT/.git" ]] || [[ -f "$DESIGN_WT/.git" ]]; then
  git -C "$DESIGN_WT" fetch origin "$BRANCH"
  git -C "$DESIGN_WT" checkout "$BRANCH"
  git -C "$DESIGN_WT" pull --ff-only origin "$BRANCH" 2>/dev/null || true
else
  mkdir -p "$(dirname "$DESIGN_WT")"
  git -C "$MAIN_REPO" worktree add -f "$DESIGN_WT" "origin/$BRANCH"
fi

echo "DESIGN_WORKTREE_OK path=$DESIGN_WT branch=$BRANCH"
echo "Use: LIREATE_DESIGN_WORKTREE=$DESIGN_WT bash scripts/lireate_design_hosting_apply.sh"
