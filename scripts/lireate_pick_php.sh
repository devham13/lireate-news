#!/usr/bin/env bash
# Pick PHP CLI for Lireate DB publish. Prefers REG.RU alt PHP 8.2/8.3, then system php.
set -euo pipefail

_candidates() {
  if [[ -n "${LIREATE_PHP:-}" ]]; then
    echo "${LIREATE_PHP}"
  fi
  for p in \
    /opt/alt/php83/usr/bin/php \
    /opt/alt/php82/usr/bin/php \
    /opt/alt/php81/usr/bin/php \
    /opt/php83/bin/php \
    /opt/php82/bin/php \
    /opt/php81/bin/php \
    /opt/php/php-8.3/bin/php \
    /opt/php/php-8.2/bin/php \
    /opt/php/php-8.1/bin/php \
    /opt/php/php-8.0/bin/php \
    /opt/php/php-7.4/bin/php \
    /usr/bin/php \
    php php-cli; do
    echo "${p}"
  done
}

for c in $(_candidates); do
  if [[ -x "${c}" ]] && "${c}" -v >/dev/null 2>&1; then
    echo "${c}"
    exit 0
  fi
  if command -v "${c}" >/dev/null 2>&1; then
    py="$(command -v "${c}")"
    if "${py}" -v >/dev/null 2>&1; then
      echo "${py}"
      exit 0
    fi
  fi
done

echo "ERROR: no PHP CLI found (set LIREATE_PHP)" >&2
exit 1
