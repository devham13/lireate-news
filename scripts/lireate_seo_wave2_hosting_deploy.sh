#!/usr/bin/env bash
# Wave 2 hosting deploy (run on REG.RU after git pull). Backs up *.bak-2026-11-10-seo3
set -euo pipefail

REPO="${LIREATE_REPO_DIR:-$HOME/lireate-autopub/repo}"
ENV_FILE="${LIREATE_ENV_FILE:-$HOME/lireate-autopub/.env}"
# shellcheck disable=SC1090
source "$ENV_FILE"
DOCROOT="${LIREATE_DOCROOT:?}"
SITE="${LIREATE_PUBLIC_SITE_URL:?LIREATE_PUBLIC_SITE_URL required}"
BAK_SUFFIX="bak-2026-11-10-seo3"
PY="$(cat "${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}/.python-interpreter")"

bak() {
  local f="$1"
  [[ -f "$f" ]] && cp -a "$f" "${f}.${BAK_SUFFIX}"
}

cd "$REPO"

# SEO PHP + htaccess fragments
for pair in "hosting-seo/data/lireate-seo-runtime.php:data/lireate-seo-runtime.php" \
            "hosting-seo/data/lireate-seo-head.inc.php:data/lireate-seo-head.inc.php"; do
  src="$REPO/${pair%%:*}"
  dst="$DOCROOT/${pair##*:}"
  bak "$dst"
  cp -a "$src" "$dst"
done

HT="$DOCROOT/.htaccess"
bak "$HT"
grep -q "LIREATE cache headers" "$HT" || cat "$REPO/hosting-seo/lireate-cache.htaccess.inc" >>"$HT"
grep -q "LIREATE SEO 2026-11-10" "$HT" || cat "$REPO/hosting-seo/lireate-seo.htaccess.inc" >>"$HT"

# robots.txt
bak "$DOCROOT/robots.txt"
sed "s|https://example.invalid|${SITE%/}|g" "$REPO/docs/proposals/robots.lireate-site.txt" >"$DOCROOT/robots.txt"

# Empty page CSS (stop 404 in logs)
for sub in 404 home news; do
  d="$DOCROOT/template/page/$sub"
  mkdir -p "$d"
  css="$d/style.css"
  [[ -f "$css" ]] || echo "/* lireate placeholder */" >"$css"
done

# Regenerate sitemap
"$PY" -c "
import os
from pathlib import Path
import sys
sys.path.insert(0, '$REPO/scripts')
from lireate_fast_indexing import build_sitemap_xml, load_sitemap_static_config, write_sitemap_atomic
from lireate_db_invoke import run_sitemap_urls
doc = Path('$DOCROOT')
rows = run_sitemap_urls(doc)['rows']
xml = build_sitemap_xml(os.environ.get('LIREATE_PUBLIC_SITE_URL',''), rows, load_sitemap_static_config())
write_sitemap_atomic(doc, xml)
print('sitemap ok', len(rows))
"

# llms.txt
"$PY" "$REPO/scripts/lireate_llms_site_generate.py" --docroot "$DOCROOT" --out "$REPO/memory/blog/lireate-site/llms.txt"
cp -a "$REPO/memory/blog/lireate-site/llms.txt" "$DOCROOT/llms.txt"

# Legacy title shorten
php "$REPO/scripts/lireate_db_shorten_seo_titles.php" "$DOCROOT"

# Messenger shim
bash "$REPO/scripts/lireate_hosting_messenger_shim.sh"

echo "WAVE2_HOSTING_DEPLOY_OK"
