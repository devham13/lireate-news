#!/usr/bin/env bash
# Run on self-hosted worker (pool lireate). Requires LIREATE_* in env / Cloud Secrets.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
ARTICLE_DIR="${1:-memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent}"
python3 scripts/lireate_reg_ru_check.py
python3 scripts/lireate_news_publish.py --article-dir "$ARTICLE_DIR"
