#!/usr/bin/env bash
# Syntax-check deployed webmaster.php with the hosting PHP CLI (safe: no secrets printed).
set -euo pipefail

AUTOPUB="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
ENV_FILE="${LIREATE_ENV_FILE:-$AUTOPUB/.env}"

docroot="${LIREATE_DOCROOT:-}"
if [[ -z "${docroot}" && -f "${ENV_FILE}" ]]; then
  line="$(grep -E '^LIREATE_DOCROOT=' "${ENV_FILE}" | head -1 || true)"
  if [[ -n "${line}" ]]; then
    docroot="${line#LIREATE_DOCROOT=}"
    docroot="${docroot//$'\r'/}"
    docroot="${docroot#\"}"
    docroot="${docroot%\"}"
    docroot="${docroot#\'}"
    docroot="${docroot%\'}"
  fi
fi

if [[ -z "${docroot}" ]]; then
  echo "FAIL: set LIREATE_DOCROOT or add it to ${ENV_FILE}" >&2
  exit 2
fi

target="${docroot}/lireate-analytics/webmaster.php"
if [[ ! -f "${target}" ]]; then
  echo "FAIL: missing ${target} (run --deploy-php-only after git pull)" >&2
  exit 2
fi

PHP_BIN="${LIREATE_PHP:-}"
if [[ -z "${PHP_BIN}" && -f "${AUTOPUB}/.php-interpreter" ]]; then
  PHP_BIN="$(cat "${AUTOPUB}/.php-interpreter")"
fi
PHP_BIN="${PHP_BIN:-php}"

echo "==> ${PHP_BIN} -l ${target}"
"${PHP_BIN}" -v | head -1
"${PHP_BIN}" -l "${target}"

if grep -q 'declare(strict_types=1)' "${target}"; then
  echo "FAIL: deployed file is old PHP 7+ template — git pull repo and --deploy-php-only" >&2
  exit 1
fi

mode="$(stat -c '%a' "${target}" 2>/dev/null || stat -f '%OLp' "${target}")"
if [[ "${mode}" != "644" && "${mode}" != "600" ]]; then
  echo "WARN: ${target} mode is ${mode} (644 recommended for CGI/FPM; redeploy fixes)"
fi

echo "OK: PHP 5.4+ template, parse check passed"
