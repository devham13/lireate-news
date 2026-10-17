#!/usr/bin/env bash
# Pick Python 3.6+ for Lireate hosting. Prints absolute path to stdout.
set -euo pipefail

_candidates() {
  if [[ -n "${LIREATE_PYTHON:-}" ]]; then
    echo "${LIREATE_PYTHON}"
  fi
  echo python3.8 python3.6 python3
}

for c in $(_candidates); do
  if ! command -v "${c}" >/dev/null 2>&1; then
    continue
  fi
  py="$(command -v "${c}")"
  if "${py}" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 6) else 1)' 2>/dev/null; then
    echo "${py}"
    exit 0
  fi
done

echo "ERROR: no Python 3.6+ found (tried: LIREATE_PYTHON, python3.8, python3.6, python3)" >&2
exit 1
