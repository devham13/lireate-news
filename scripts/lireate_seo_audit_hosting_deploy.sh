#!/usr/bin/env bash
# SEO audit 2026-11-11 — hosting deploy (backups *.bak-2026-11-11-audit)
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
BAK="bak-2026-11-11-audit"
PY="$(command -v python3)"

bak() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  cp -a "$f" "${f}.${BAK}"
}

atomic_php() {
  local dst="$1"
  local src="$2"
  bak "$dst"
  cp -a "$src" "${dst}.new"
  php -l "${dst}.new" >/dev/null
  mv -f "${dst}.new" "$dst"
  php -l "$dst" >/dev/null
}

cd "$REPO"
git fetch origin main
git merge --ff-only origin/main

# SEO PHP layer
for pair in \
  "hosting-seo/data/lireate-seo-runtime.php:data/lireate-seo-runtime.php" \
  "hosting-seo/data/lireate-seo-head.inc.php:data/lireate-seo-head.inc.php" \
  "hosting-seo/data/lireate-seo-schema.inc.php:data/lireate-seo-schema.inc.php"; do
  atomic_php "$DOCROOT/${pair##*:}" "$REPO/${pair%%:*}"
done

bak "$DOCROOT/data/lireate-seo-audit-meta.json"
cp -a "$REPO/shared/lireate-seo-audit-meta.json" "$DOCROOT/data/lireate-seo-audit-meta.json"

PRE="$DOCROOT/data/lireate-seo-pre-template.inc.php"
atomic_php "$PRE" "$REPO/hosting-seo/index.lireate-seo-pre-template.inc.php"

MAIN="$DOCROOT/template/main.php"
if [[ -f "$MAIN" ]]; then
  bak "$MAIN"
  sed -i 's|href="./favicon.svg"|href="/favicon.svg"|g' "$MAIN"
  sed -i 's|/template/images/team/person/\([0-9][0-9]*\)\.jpg|/template/images/team/person/\1.webp|g' "$MAIN"
  sed -i 's|<div class="slidePhoto"><img src="/template/images/team/person/\([0-9][0-9]*\)\.webp">|<div class="slidePhoto"><img loading="lazy" width="120" height="120" src="/template/images/team/person/\1.webp" alt="Сотрудник LIREATE">|g' "$MAIN"
  sed -i 's|<div class="slidePhoto"><img src="/template/images/team/person/|<div class="slidePhoto"><img loading="lazy" width="120" height="120" src="/template/images/team/person/|g' "$MAIN"
  php -l "$MAIN" >/dev/null
fi

# Landing pages: broken service links
for f in "$DOCROOT/registraciya_tovarnogo_znaka/index.php" "$DOCROOT/findtz/index.php" "$DOCROOT/vozrazhenie_protiv_registracii_tovarnogo_znaka/index.php"; do
  [[ -f "$f" ]] || continue
  bak "$f"
  sed -i 's|/vozrazhenie-protiv-registracii-tovarnogo-znaka/|/vozrazhenie_protiv_registracii_tovarnogo_znaka/|g' "$f"
  php -l "$f" >/dev/null
done

# reviews/portfolio encoding: use shared db.php, utf8mb4
for f in "$DOCROOT/template/page/reviews.php" "$DOCROOT/template/page/portfolio.php"; do
  [[ -f "$f" ]] || continue
  bak "$f"
  sed -i "s/mysqli_set_charset (.'UTF8'.)/mysqli_set_charset(\$connect, 'utf8mb4');/g" "$f"
  sed -i "s/mysqli_set_charset ('UTF8')/mysqli_set_charset(\$connect, 'utf8mb4')/g" "$f"
  php -l "$f" >/dev/null
done

# Empty page style stubs (avoid 404 when link tag conditional fails on old caches)
for p in home 404 kontaktyi news; do
  d="$DOCROOT/template/page/$p"
  mkdir -p "$d"
  if [[ ! -f "$d/style.css" ]]; then
    touch "$d/style.css"
  fi
done

# CLS reserve for blog filters
CLS="$DOCROOT/template/css/lireate-audit-cls.css"
bak "$CLS" 2>/dev/null || true
cat >"$CLS" <<'CSS'
.lireate-blog-list-filters { min-height: 52px; }
.lireate-blog-list-filters-scroll { min-height: 44px; }
.lireate-blog-h1 { min-height: 1.2em; }
CSS
if [[ -f "$MAIN" ]] && ! grep -q lireate-audit-cls.css "$MAIN"; then
  sed -i 's|lireate-ux-fixes.css|lireate-ux-fixes.css?v=20261110ux" />\n    <link rel="stylesheet" href="/template/css/lireate-audit-cls.css?v=20261111audit|g' "$MAIN" || \
    echo '<link rel="stylesheet" href="/template/css/lireate-audit-cls.css?v=20261111audit" />' >>"$DOCROOT/template/page/news/lireate-blog-list.css" 2>/dev/null || true
fi

HT="$DOCROOT/.htaccess"
bak "$HT"
if ! grep -q "LIREATE audit 2026-11-11: single-hop" "$HT"; then
  {
    grep -v '^RewriteEngine On$' "$HT" | grep -v '^RewriteCond %{SERVER_PORT}' | grep -v '^RewriteRule .* https://%{SERVER_NAME}' || true
  } >"${HT}.body"
  {
    echo "RewriteEngine On"
    tail -n +3 "$REPO/hosting-seo/lireate-https-www.htaccess.inc"
    cat "${HT}.body"
  } >"${HT}.new"
  mv "${HT}.new" "$HT"
  rm -f "${HT}.body"
fi
for inc in lireate-audit-deny.htaccess.inc lireate-audit-redirects.htaccess.inc; do
  if ! grep -qF "$inc" "$HT"; then
    echo "" >>"$HT"
    cat "$REPO/hosting-seo/$inc" >>"$HT"
  fi
done

# WebP previews for blog + team (best effort)
if command -v cwebp >/dev/null; then
  while IFS= read -r -d '' img; do
    base="${img%.*}"
    [[ -f "${base}-preview480.webp" ]] && continue
    cwebp -quiet -q 82 -resize 480 0 "$img" -o "${base}-preview480.webp" || true
  done < <(find "$DOCROOT/template/images/blog" -type f \( -name '*.jpg' -o -name '*.png' \) -print0 2>/dev/null | head -z -n 300)
  while IFS= read -r -d '' img; do
    webp="${img%.*}.webp"
    [[ -f "$webp" ]] && continue
    cwebp -quiet -q 85 -resize 240 0 "$img" -o "$webp" || true
  done < <(find "$DOCROOT/template/images/team/person" -type f -name '*.jpg' -print0 2>/dev/null)
fi

BLOG_LAYOUT="$DOCROOT/pages/blog/_shared/lireate-blog-layout.inc.php"
if [[ -f "$BLOG_LAYOUT" ]]; then
  bak "$BLOG_LAYOUT"
  cp -a "$REPO/hosting-seo/patches/pages/blog/_shared/lireate-blog-layout.inc.php" "$BLOG_LAYOUT"
  php -l "$BLOG_LAYOUT" >/dev/null
fi

"$PY" "$REPO/scripts/lireate_seo_audit_apply.py" --docroot "$DOCROOT"

"$PY" -c "
import os, sys
from pathlib import Path
sys.path.insert(0, '$REPO/scripts')
from lireate_fast_indexing import build_sitemap_xml, load_sitemap_static_config, write_sitemap_atomic, post_indexnow_yandex
from lireate_db_invoke import run_sitemap_urls
from urllib.parse import urlparse
doc = Path('$DOCROOT')
rows = run_sitemap_urls(doc)['rows']
old = set()
old_path = doc / 'sitemap.xml'
if old_path.is_file():
    old = set(__import__('re').findall(r'<loc>([^<]+)</loc>', old_path.read_text(encoding='utf-8', errors='replace')))
xml = build_sitemap_xml(os.environ.get('LIREATE_PUBLIC_SITE_URL',''), rows, load_sitemap_static_config())
write_sitemap_atomic(doc, xml)
new = set(__import__('re').findall(r'<loc>([^<]+)</loc>', xml))
fresh = sorted(new - old)
print('sitemap_urls', len(new), 'new', len(fresh))
key=os.environ.get('INDEXNOW_KEY','')
host=urlparse(os.environ.get('LIREATE_PUBLIC_SITE_URL','')).netloc
if key and fresh:
    print(post_indexnow_yandex(host, key, fresh[:50]))
else:
    print({'indexnow':'skipped'})
"

curl -sf -o /dev/null -w "home:%{http_code}\n" "${SITE%/}/"
curl -sf -o /dev/null -w "poisk:%{http_code}\n" "${SITE%/}/poisk_tovarnyh_znakov/"
for s in PHP_errors.log cookie.txt everest.zip; do
  code=$(curl -sI -o /dev/null -w "%{http_code}" "${SITE%/}/$s")
  echo "deny $s:$code"
done

echo "AUDIT_HOSTING_DEPLOY_OK"
