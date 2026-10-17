#!/usr/bin/env bash
# Install Lireate autopublish outside public docroot on REG.RU ISPmanager.
# Usage (in ISPmanager Shell): curl -fsSL .../lireate_hosting_install.sh | bash
# Or: bash scripts/lireate_hosting_install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PICK_PY="${SCRIPT_DIR}/lireate_pick_python.sh"

LIREATE_AUTOPUB_HOME="${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}"
REPO_URL="${LIREATE_REPO_URL:-https://github.com/devham13/lireate-news.git}"
REPO_BRANCH="${LIREATE_REPO_BRANCH:-main}"

if [[ -x "${PICK_PY}" ]]; then
  LIREATE_PYTHON="$(bash "${PICK_PY}")"
else
  LIREATE_PYTHON="${LIREATE_PYTHON:-$(command -v python3.8 || command -v python3.6 || command -v python3)}"
fi

echo "==> Lireate autopublish install into ${LIREATE_AUTOPUB_HOME}"
echo "==> Python: ${LIREATE_PYTHON}"
"${LIREATE_PYTHON}" -c 'import sys; print("==> Python version:", sys.version.replace("\n"," "))'

mkdir -p "${LIREATE_AUTOPUB_HOME}/logs" "${LIREATE_AUTOPUB_HOME}/var" "${LIREATE_AUTOPUB_HOME}/state" "${LIREATE_AUTOPUB_HOME}/cms-config"
echo "${LIREATE_PYTHON}" > "${LIREATE_AUTOPUB_HOME}/.python-interpreter"
chmod 600 "${LIREATE_AUTOPUB_HOME}/.python-interpreter"

if [[ ! -d "${LIREATE_AUTOPUB_HOME}/repo/.git" ]]; then
  git clone --depth 1 --branch "${REPO_BRANCH}" "${REPO_URL}" "${LIREATE_AUTOPUB_HOME}/repo"
else
  echo "==> repo exists, git pull"
  git -C "${LIREATE_AUTOPUB_HOME}/repo" pull --ff-only || true
fi

ENV_FILE="${LIREATE_AUTOPUB_HOME}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
  cat >"${ENV_FILE}" <<'EOF'
# Lireate autopublish — заполните значения и сохраните. chmod 600 уже выставлен установщиком.
# Публичный URL сайта (https://…)
LIREATE_PUBLIC_SITE_URL=
# Абсолютный путь к public_html (ISPmanager → файловый менеджер)
LIREATE_DOCROOT=
LIREATE_ALLOW_PUBLISH=no

# HTTP к админке с того же сервера (обходит RCPC с внешних IP). Обычно:
LIREATE_CMS_HTTP_BASE=http://127.0.0.1
# LIREATE_ADMIN_URL=http://127.0.0.1/admin/

LIREATE_ADMIN_USER=
LIREATE_ADMIN_PASSWORD=

# Первая статья для теста (после merge PR — путь внутри клона):
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

EXAMPLE_CFG="${LIREATE_AUTOPUB_HOME}/repo/shared/lireate-cms-http-config.json.example"
DEST_CFG="${LIREATE_AUTOPUB_HOME}/cms-config/lireate-cms-http-config.json"
if [[ -f "${EXAMPLE_CFG}" && ! -f "${DEST_CFG}" ]]; then
  cp "${EXAMPLE_CFG}" "${DEST_CFG}"
  echo "==> Copied CMS config example to ${DEST_CFG} (edit after probe)"
fi

chmod +x "${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_publish.py" 2>/dev/null || true
chmod +x "${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_selfcheck.py" 2>/dev/null || true

export LIREATE_AUTOPUB_HOME
export LIREATE_ENV_FILE="${ENV_FILE}"
export LIREATE_PYTHON="${LIREATE_PYTHON}"
"${LIREATE_PYTHON}" "${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_selfcheck.py" || true

echo ""
echo "Next steps:"
echo "  1. Edit ${ENV_FILE} (set DOCROOT, admin login, LIREATE_ALLOW_PUBLISH=yes when ready)"
echo "  2. Dry-run: ${LIREATE_PYTHON} ${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_hosting_publish.py --dry-run"
echo "  3. Probe CMS once: ${LIREATE_PYTHON} ${LIREATE_AUTOPUB_HOME}/repo/scripts/lireate_cms_probe.py"
echo "  4. Copy probe config to ${DEST_CFG}"
echo "Cron: use interpreter from ${LIREATE_AUTOPUB_HOME}/.python-interpreter"
echo "See docs/lireate-autopub-hosting.ru.md"
