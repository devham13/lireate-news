#!/usr/bin/env bash
# Integrity checks for template/main.php before/after design deploy.
set -euo pipefail

LIREATE_MAIN_MIN_LINES="${LIREATE_MAIN_MIN_LINES:-5000}"

lireate_main_php_guard() {
  local f="${1:?main.php path}"
  [[ -f "$f" ]] || { echo "MAIN_GUARD: missing $f" >&2; return 1; }
  local lines
  lines=$(wc -l <"$f" | tr -d ' ')
  if [[ "$lines" -lt "$LIREATE_MAIN_MIN_LINES" ]]; then
    echo "MAIN_GUARD: too few lines ($lines < $LIREATE_MAIN_MIN_LINES)" >&2
    return 1
  fi
  if ! grep -q 'page_container' "$f"; then
    echo "MAIN_GUARD: page_container marker missing" >&2
    return 1
  fi
  if ! php -l "$f" >/dev/null 2>&1; then
    echo "MAIN_GUARD: php -l failed" >&2
    return 1
  fi
  return 0
}

lireate_main_php_touch() {
  local f="${1:?}"
  touch "$f"
}
