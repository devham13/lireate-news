#!/usr/bin/env bash
# Sync autopub repo to origin/<branch> without fetching into the checked-out branch ref.
# Preserves local publish artifacts (ledger edits, lireate-publish-result.json, publish-bundle/).
set -euo pipefail

AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
REPO_DIR="${LIREATE_REPO_DIR:-$AUTOPUB_HOME/repo}"
BRANCH="${LIREATE_REPO_BRANCH:-main}"
REMOTE="${LIREATE_REPO_REMOTE:-origin}"
LEDGER_REL="shared/published-articles-lireate.md"
LOG_DIR="${AUTOPUB_HOME}/logs"

sync_error() {
  echo "SYNC_ERROR: $*" >&2
  exit 1
}

resolve_stash_pop_conflict() {
  local ts
  ts="$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$LOG_DIR"
  if git rev-parse --verify stash@{0} >/dev/null 2>&1; then
    git show "stash@{0}:${LEDGER_REL}" >"$LOG_DIR/published-articles-local-${ts}.md" 2>/dev/null \
      || true
  fi
  # During stash apply, "ours" is current HEAD (upstream); keep it in the working tree.
  git checkout --ours -- "$LEDGER_REL" 2>/dev/null || git checkout HEAD -- "$LEDGER_REL"
  git add -- "$LEDGER_REL" 2>/dev/null || true
  git reset HEAD -- "$LEDGER_REL" 2>/dev/null || true
  git checkout -- "$LEDGER_REL"
  git stash drop -q 2>/dev/null || git stash drop 2>/dev/null || true
}

ensure_clean_merge_state() {
  if git ls-files -u | grep -q .; then
    if [[ -f "$LEDGER_REL" ]]; then
      git checkout --ours -- "$LEDGER_REL" 2>/dev/null || git checkout HEAD -- "$LEDGER_REL"
      git add -- "$LEDGER_REL" 2>/dev/null || true
      git reset HEAD -- "$LEDGER_REL" 2>/dev/null || true
      git checkout -- "$LEDGER_REL"
    fi
  fi
  if git ls-files -u | grep -q .; then
    sync_error "unmerged paths remain after sync (manual fix required)"
  fi
}

if [[ ! -d "$REPO_DIR/.git" ]]; then
  sync_error "not a git repo: $REPO_DIR"
fi

mkdir -p "$LOG_DIR"
cd "$REPO_DIR"

STASHED=0
trap 'ensure_clean_merge_state' EXIT

if ! git fetch "$REMOTE" "+refs/heads/${BRANCH}:refs/remotes/${REMOTE}/${BRANCH}"; then
  sync_error "git fetch failed for ${REMOTE}/${BRANCH}"
fi

if ! git rev-parse --verify "${REMOTE}/${BRANCH}^{commit}" >/dev/null 2>&1; then
  sync_error "missing ${REMOTE}/${BRANCH} after fetch (shallow clone? fetch ${BRANCH} once manually)"
fi

if [[ -f "$LEDGER_REL" ]]; then
  if ! git diff --quiet HEAD -- "$LEDGER_REL" 2>/dev/null \
    || ! git diff --cached --quiet -- "$LEDGER_REL" 2>/dev/null; then
    if git stash push -q -m "lireate-autopub: local ledger before sync" -- "$LEDGER_REL"; then
      STASHED=1
    fi
  fi
fi

if ! git checkout -B "$BRANCH" "${REMOTE}/${BRANCH}"; then
  if [[ "$STASHED" -eq 1 ]]; then
    git stash pop -q 2>/dev/null || true
  fi
  sync_error "git checkout -B ${BRANCH} ${REMOTE}/${BRANCH} failed"
fi

if [[ "$STASHED" -eq 1 ]]; then
  if ! git stash pop -q; then
    resolve_stash_pop_conflict
  fi
fi

ensure_clean_merge_state
trap - EXIT

echo "OK synced to ${REMOTE}/${BRANCH} at $(git rev-parse --short HEAD)"
