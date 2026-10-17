#!/usr/bin/env bash
# Install Lireate autopublish outside public docroot on REG.RU ISPmanager.
# Usage: curl -fsSL .../lireate_hosting_install.sh | bash
set -euo pipefail

SCRIPT_DIR="$(pwd)"
if [[ -n "${BASH_SOURCE:-}" ]]; then
  _src="${BASH_SOURCE[0]}"
  if [[ -n "${_src}" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${_src}")" && pwd)"
  fi
fi

PICK_PY="${SCRIPT_DIR}/lireate_pick_python.sh"
PICK_PHP="${SCRIPT_DIR}/lireate_pick_php.sh"

LIREATE_AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
REPO_URL="${LIREATE_REPO_URL:-https://github.com/devham13/lireate-news.git}"
REPO_BRANCH="${LIREATE_REPO_BRANCH:-main}"

if [[ -x "${PICK_PY}" ]]; then
  LIREATE_PYTHON="$(bash "${PICK_PY}")"
else
  LIREATE_PYTHON="${LIREATE_PYTHON:-$(command -v python3.8 || command -v python3.6 || command -v python3)}"
fi

if [[ -x "${PICK_PHP}" ]]; then
  LIREATE_PHP="$(bash "${PICK_PHP}")"
else
  LIREATE_PHP="${LIREATE_PHP:-$(command -v php || echo php)}"
fi

echo "==> Lireate autopublish install into ${LIREATE_AUTOPUB_HOME}"
echo "==> Python: ${LIREATE_PYTHON}"
"${LIREATE_PYTHON}" -c 'import sys; print("==> Python version:", sys.version.replace("\n"," "))'
echo "==> PHP: ${LIREATE_PHP}"
"${LIREATE_PHP}" -v | head -1 || true

mkdir -p "${LIREATE_AUTOPUB_HOME}/logs" "${LIREATE_AUTOPUB_HOME}/var" "${LIREATE_AUTOPUB_HOME}/state"
echo "${LIREATE_PYTHON}" > "${LIREATE_AUTOPUB_HOME}/.python-interpreter"
echo "${LIREATE_PHP}" > "${LIREATE_AUTOPUB_HOME}/.php-interpreter"
chmod 600 "${LIREATE_AUTOPUB_HOME}/.python-interpreter" "${LIREATE_AUTOPUB_HOME}/.php-interpreter"

if [[ ! -d "${LIREATE_AUTOPUB_HOME}/repo/.git" ]]; then
  git clone --depth 1 --branch "${REPO_BRANCH}" "${REPO_URL}" "${LIREATE_AUTOPUB_HOME}/repo"
else
  echo "==> repo exists, git pull"
  git -C "${LIREATE_AUTOPUB_HOME}/repo" pull --ff-only || true
fi

ENV_FILE="${LIREATE_AUTOPUB_HOME}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
  cat >"${ENV_FILE}" <<'EOF'
# Lireate autopublish — заполните и сохраните (chmod 600).
LIREATE_PUBLIC_SITE_URL=
# $HOME/www/public_html на REG.RU (пример: /var/www/uXXXX/data/www/public_html)
LIREATE_DOCROOT=
LIREATE_ALLOW_PUBLISH=no

# Публикация через PHP+MySQL (пароль БД только в public_html/data/db.php на сервере)
# LIREATE_PHP=

LIREATE_ARTICLE_DIR=
LIREATE_LOG_FILE=
LIREATE_LOCK_FILE=
LIREATE_STATE_FILE=
LIREATE_ENV_FILE=
EOF
  chmod 600 "${ENV_FILE}"
  echo "==> Created template ${ENV_FILE}"
else
  echo "==> .env already exists, not overwritten"
fi

chmod +x "${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_publish.py" 2>/dev/null || true
chmod +x "${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_selfcheck.py" 2>/dev/null || true
chmod +x "${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_db_diagnostic.py" 2>/dev/null || true

export LIREATE_AUTOPUB_HOME
export LIREATE_ENV_FILE="${ENV_FILE}"
export LIREATE_PYTHON="${LIREATE_PYTHON}"
export LIREATE_PHP="${LIREATE_PHP}"
"${LIREATE_PYTHON}" "${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_selfcheck.py" || true

echo ""
echo "Next steps:"
echo "  1. Edit ${ENV_FILE} (LIREATE_PUBLIC_SITE_URL, LIREATE_DOCROOT)"
echo "  2. Diagnostic: ${LIREATE_PYTHON} ${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_db_diagnostic.py"
echo "  3. Dry-run L01: ${LIREATE_PYTHON} ${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_publish.py --dry-run"
echo "Cron: \$(cat ${LIREATE_AUTOPUB_HOME}/.python-interpreter) .../lireate_hosting_publish.py"
echo "See docs/lireate-autopub-hosting.ru.md"
