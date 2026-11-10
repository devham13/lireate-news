#!/usr/bin/env bash
# Wave 3 SEO hosting deploy — backups *.bak-2026-11-10-seo4
set -euo pipefail

REPO="${LIREATE_REPO_DIR:-$HOME/lireate-autopub/repo}"
ENV_FILE="${LIREATE_ENV_FILE:-$HOME/lireate-autopub/.env}"
set -a
# shellcheck source=/dev/null
source "$ENV_FILE" 2>/dev/null || true
set +a
DOCROOT="${LIREATE_DOCROOT:?}"
SITE="${LIREATE_PUBLIC_SITE_URL:?}"
export LIREATE_PUBLIC_SITE_URL="$SITE"
BAK_SUFFIX="bak-2026-11-10-seo4"
PY="$(cat "${LIREATE_AUTOPUB_HOME:-$HOME/lireate-autopub}/.python-interpreter")"

bak() {
  local f="$1"
  if [[ -f "$f" ]]; then
    cp -a "$f" "${f}.${BAK_SUFFIX}"
  fi
}

cd "$REPO"

for pair in \
  "hosting-seo/data/lireate-seo-runtime.php:data/lireate-seo-runtime.php" \
  "hosting-seo/data/lireate-seo-head.inc.php:data/lireate-seo-head.inc.php" \
  "hosting-seo/data/lireate-seo-schema.inc.php:data/lireate-seo-schema.inc.php"; do
  src="$REPO/${pair%%:*}"
  dst="$DOCROOT/${pair##*:}"
  bak "$dst"
  cp -a "$src" "$dst"
done

BLOG_LAYOUT="$DOCROOT/pages/blog/_shared/lireate-blog-layout.inc.php"
if [[ -f "$BLOG_LAYOUT" ]]; then
  bak "$BLOG_LAYOUT"
  cp -a "$REPO/hosting-seo/patches/pages/blog/_shared/lireate-blog-layout.inc.php" "$BLOG_LAYOUT"
fi
TPL_LAYOUT="$DOCROOT/template/page/news/lireate-blog-layout.inc.php"
if [[ -f "$TPL_LAYOUT" ]]; then
  bak "$TPL_LAYOUT"
  cp -a "$REPO/hosting-seo/patches/pages/blog/_shared/lireate-blog-layout.inc.php" "$TPL_LAYOUT"
fi
CMS_INC="$DOCROOT/template/page/news/lireate-blog-cms.inc.php"
bak "$CMS_INC"
cp -a "$REPO/hosting-seo/patches/template/page/news/lireate-blog-cms.inc.php" "$CMS_INC"

mkdir -p "$DOCROOT/pages" "$DOCROOT/template/page"
bak "$DOCROOT/pages/avtor-page.inc.php"
cp -a "$REPO/hosting-seo/pages/avtor-page.inc.php" "$DOCROOT/pages/avtor-page.inc.php"
bak "$DOCROOT/template/page/avtor.php"
cp -a "$REPO/hosting-seo/template/page/avtor.php" "$DOCROOT/template/page/avtor.php"

PRE_DST="$DOCROOT/data/lireate-seo-pre-template.inc.php"
bak "$PRE_DST"
cp -a "$REPO/hosting-seo/index.lireate-seo-pre-template.inc.php" "$PRE_DST"

INDEX="$DOCROOT/index.php"
bak "$INDEX"
if ! grep -q "lireate-seo-pre-template" "$INDEX"; then
  sed -i '/\$template = template(\$db, \$temp);/i require __DIR__ . '"'"'/data/lireate-seo-pre-template.inc.php'"'"';' "$INDEX"
fi

# main.php og guard: apply manually if needed (hosting-seo/template/main.php.og-guard.patch).

bak "$DOCROOT/robots.txt"
sed "s|https://example.invalid|${SITE%/}|g" "$REPO/docs/proposals/robots.lireate-site.txt" >"$DOCROOT/robots.txt"

HT="$DOCROOT/.htaccess"
if ! grep -q "chto_delat_esli_tovarnyy_znak_zanyat" "$HT" 2>/dev/null; then
  bak "$HT"
  cat >>"$HT" <<'HTINC'

# L19 duplicate → legacy (SEO wave 3)
RewriteRule ^chto_delat_esli_tovarnyy_znak_zanyat/?$ /chto_delat_esli_tovarnyiy_znak_zanyat/ [R=301,L]
HTINC
fi

BACKUP_DIR="$DOCROOT/data/backups-seo4-$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
php "$REPO/scripts/lireate_seo_mktu_descriptions.php" "$DOCROOT" --apply | tee "$BACKUP_DIR/mktu-descriptions.json"
LANDING_BAK="$BACKUP_DIR/pages-registracija_torgovyh_marok_i_logotipov.sql"
php -r "require '$DOCROOT/data/db.php'; \$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME); \$r=\$m->query('SELECT * FROM pages WHERE id=105'); \$row=\$r->fetch_assoc(); file_put_contents('$LANDING_BAK', json_encode(\$row, JSON_UNESCAPED_UNICODE));"
php "$REPO/scripts/lireate_seo_fee_update.php" "$DOCROOT" --apply | tee "$BACKUP_DIR/fee-update.json"

NEWS_BAK="$BACKUP_DIR/news-table.json"
php -r "require '$DOCROOT/data/db.php'; \$m=new mysqli(DB_SERVER,DB_USER,DB_PASS,DB_NAME); \$r=\$m->query('SELECT id,seo_url,full_story FROM news'); \$rows=[]; while(\$x=\$r->fetch_assoc())\$rows[]=\$x; file_put_contents('$NEWS_BAK', json_encode(\$rows, JSON_UNESCAPED_UNICODE));"

"$PY" "$REPO/scripts/lireate_seo_internal_links.py" --docroot "$DOCROOT" --apply --backup "$NEWS_BAK" | tee "$BACKUP_DIR/internal-links.json"

"$PY" -c "
import os, sys
from pathlib import Path
sys.path.insert(0, '$REPO/scripts')
from lireate_fast_indexing import build_sitemap_xml, load_sitemap_static_config, write_sitemap_atomic
from lireate_db_invoke import run_sitemap_urls
doc = Path('$DOCROOT')
rows = run_sitemap_urls(doc)['rows']
xml = build_sitemap_xml(os.environ.get('LIREATE_PUBLIC_SITE_URL',''), rows, load_sitemap_static_config())
write_sitemap_atomic(doc, xml)
print('sitemap ok', len(rows))
"

"$PY" -c "
import os, sys
sys.path.insert(0, '$REPO/scripts')
from lireate_fast_indexing import post_indexnow_yandex
from urllib.parse import urlparse
site=os.environ.get('LIREATE_PUBLIC_SITE_URL','').rstrip('/')
key=os.environ.get('INDEXNOW_KEY','')
host=urlparse(site).netloc
urls=[site+'/avtor/', site+'/registracija_torgovyh_marok_i_logotipov/', site+'/news']
if key:
    print(post_indexnow_yandex(host, key, urls))
else:
    print({'skipped': True, 'reason': 'INDEXNOW_KEY'})
"

echo "WAVE3_HOSTING_DEPLOY_OK"
