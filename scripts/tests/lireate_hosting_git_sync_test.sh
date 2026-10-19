#!/usr/bin/env bash
# Integration test for lireate_hosting_git_sync.sh (bash 4+, git 2.x).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SYNC="$ROOT/scripts/lireate_hosting_git_sync.sh"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

pass() {
  echo "PASS: $*"
}

BARE="$WORKDIR/remote.git"
CLONE="$WORKDIR/clone"
AUTOPUB="$WORKDIR/autopub"
mkdir -p "$AUTOPUB/logs"

git init --bare -q "$BARE"
git -C "$BARE" symbolic-ref HEAD refs/heads/main

git init -q "$WORKDIR/seed"
cd "$WORKDIR/seed"
git config user.email "test@lireate.local"
git config user.name "Test"
mkdir -p shared memory/blog/articles/L01-test
echo "# ledger" > shared/published-articles-lireate.md
echo "base" > memory/blog/articles/L01-test/article.html
git add .
git commit -q -m "initial"
git branch -M main
git remote add origin "$BARE"
git push -q -u origin main

git clone -q "$BARE" "$CLONE"
cd "$CLONE"
git config user.email "test@lireate.local"
git config user.name "Test"

echo "| local | row |" >> shared/published-articles-lireate.md
mkdir -p memory/blog/articles/L01-test/publish-bundle
echo '{"verdict":"published"}' > memory/blog/articles/L01-test/lireate-publish-result.json
echo "bundle" > memory/blog/articles/L01-test/publish-bundle/x.txt

LOCAL_HEAD_BEFORE="$(git rev-parse HEAD)"

UPSTREAM_W="$WORKDIR/upstream"
git clone -q "$BARE" "$UPSTREAM_W"
cd "$UPSTREAM_W"
git config user.email "test@lireate.local"
git config user.name "Test"
echo "| upstream | row |" >> shared/published-articles-lireate.md
git add shared/published-articles-lireate.md
git commit -q -m "upstream ledger"
git push -q origin main
UPSTREAM_SHA="$(git rev-parse HEAD)"

export LIREATE_AUTOPUB_HOME="$AUTOPUB"
export LIREATE_REPO_DIR="$CLONE"
export LIREATE_REPO_BRANCH=main
export LIREATE_REPO_REMOTE=origin

SYNC_LOG="$WORKDIR/sync.log"
if ! bash "$SYNC" >"$SYNC_LOG" 2>&1; then
  cat "$SYNC_LOG" >&2
  fail "sync script exited non-zero"
fi

if grep -q "refusing to fetch" "$SYNC_LOG"; then
  cat "$SYNC_LOG" >&2
  fail "git refused to fetch into checked-out branch"
fi

if ! grep -q "OK synced to origin/main at" "$SYNC_LOG"; then
  cat "$SYNC_LOG" >&2
  fail "missing success line"
fi

cd "$CLONE"
LOCAL_HEAD_AFTER="$(git rev-parse HEAD)"
if [[ "$LOCAL_HEAD_AFTER" != "$UPSTREAM_SHA" ]]; then
  fail "HEAD $LOCAL_HEAD_AFTER != upstream $UPSTREAM_SHA (was $LOCAL_HEAD_BEFORE)"
fi

if [[ ! -f memory/blog/articles/L01-test/lireate-publish-result.json ]]; then
  fail "untracked lireate-publish-result.json was lost"
fi

if [[ ! -f memory/blog/articles/L01-test/publish-bundle/x.txt ]]; then
  fail "untracked publish-bundle was lost"
fi

if git ls-files -u | grep -q .; then
  fail "repo left in unmerged/conflict state"
fi

if [[ -f shared/published-articles-lireate.md ]] && grep -q '<<<<<<<' shared/published-articles-lireate.md; then
  fail "conflict markers in ledger"
fi

if ! grep -q 'upstream' shared/published-articles-lireate.md; then
  fail "ledger should keep upstream version after stash conflict"
fi

if ! compgen -G "$AUTOPUB/logs/published-articles-local-*.md" >/dev/null; then
  fail "expected published-articles-local backup in logs after ledger conflict"
fi

pass "no refusing-to-fetch; HEAD at upstream; untracked publish artifacts preserved; clean merge state"
echo "--- sync output ---"
cat "$SYNC_LOG"
