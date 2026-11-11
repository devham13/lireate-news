#!/usr/bin/env bash
# Деплой страницы /avtor/ и SEO-meta на REG.RU. Бэкап: *.bak-2026-11-11-avtor
set -euo pipefail

REPO="${LIREATE_REPO_DIR:-$HOME/lireate-autopub/repo}"
ENV_FILE="${LIREATE_ENV_FILE:-$HOME/lireate-autopub/.env}"
set -a
# shellcheck source=/dev/null
source "$ENV_FILE" 2>/dev/null || true
set +a
DOCROOT="${LIREATE_DOCROOT:?}"
BAK_SUFFIX="bak-2026-11-11-avtor"

bak() {
  local f="$1"
  if [[ -f "$f" ]]; then
    cp -a "$f" "${f}.${BAK_SUFFIX}"
  fi
}

cd "$REPO"

mkdir -p "$DOCROOT/template/page/avtor" "$DOCROOT/pages"

for pair in \
  "hosting-seo/data/lireate-seo-page-meta.inc.php:data/lireate-seo-page-meta.inc.php" \
  "hosting-seo/data/lireate-seo-schema.inc.php:data/lireate-seo-schema.inc.php" \
  "hosting-seo/index.lireate-seo-pre-template.inc.php:data/lireate-seo-pre-template.inc.php" \
  "hosting-seo/pages/avtor-page.inc.php:pages/avtor-page.inc.php" \
  "hosting-seo/template/page/avtor.php:template/page/avtor.php" \
  "hosting-seo/template/page/avtor/lireate-avtor.css:template/page/avtor/lireate-avtor.css"; do
  src="$REPO/${pair%%:*}"
  dst="$DOCROOT/${pair##*:}"
  bak "$dst"
  cp -a "$src" "$dst"
done

php -r "
require '$DOCROOT/data/db.php';
\$m = new mysqli(DB_SERVER, DB_USER, DB_PASS, DB_NAME);
if (\$m->connect_errno) { fwrite(STDERR, 'db connect failed\n'); exit(1); }
\$title = 'Горбачев Юрий Александрович — директор бюро «Лирейт»';
\$desc = 'Юрий Горбачев — директор и управляющий партнёр ООО «ЛИРЕЙТ»: товарные знаки, патенты, авторское право и споры. Статьи на vc.ru, в Т—Ж, на Клерке и Хабре.';
\$st = \$m->prepare('UPDATE pages SET seo_title=?, seo_description=? WHERE seo_url=? LIMIT 1');
\$slug = 'avtor';
\$st->bind_param('sss', \$title, \$desc, \$slug);
\$st->execute();
echo 'pages_updated=' . \$st->affected_rows . PHP_EOL;
"

echo "AVTOR_HOSTING_DEPLOY_OK docroot=$DOCROOT"
