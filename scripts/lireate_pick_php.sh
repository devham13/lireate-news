#!/usr/bin/env bash
# Pick PHP CLI for Lireate DB publish. Prints absolute path to stdout.
set -euo pipefail

_candidates() {
  if [[ -n "${LIREATE_PHP:-}" ]]; then
    echo "${LIREATE_PHP}"
  fi
  for p in /opt/php/php-8.2/bin/php /opt/php/php-8.1/bin/php /opt/php/php-8.0/bin/php \
    /opt/php/php-7.4/bin/php php php-cli; do
    echo "${p}"
  done
}

for c in $(_candidates); do
  if command -v "${c}" >/dev/null 2>&1; then
    py="$(command -v "${c}")"
    if "${py}" -v >/dev/null 2>&1; then
      echo "${py}"
      exit 0
    fi
  fi
  if [[ -x "${c}" ]]; then
    if "${c}" -v >/dev/null 2>&1; then
      echo "${c}"
      exit 0
    fi
  fi
done

echo "ERROR: no PHP CLI found (set LIREATE_PHP)" >&2
exit 1
