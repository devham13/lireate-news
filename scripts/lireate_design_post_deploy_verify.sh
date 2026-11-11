#!/usr/bin/env bash
# After main.php / design deploy: HTTP 200 + exactly one <h1> per URL.
set -euo pipefail

SITE="${LIREATE_PUBLIC_SITE_URL:?}"
SITE="${SITE%/}"

urls=(
  "/"
  "/uslugi/"
  "/news/"
  "/mktu"
  "/patent"
  "/team"
  "/kontaktyi"
  "/registraciya_tovarnogo_znaka/"
  "/avtor/"
  "/reviews/"
  "/poisk_tovarnyh_znakov/"
)

# One blog article (static fallback if env unset)
ARTICLE_PATH="${LIREATE_VERIFY_ARTICLE_PATH:-/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/}"
urls+=("$ARTICLE_PATH")

fail=0
for path in "${urls[@]}"; do
  url="${SITE}${path}"
  html=$(curl -sL -m 45 -H 'Cache-Control: no-cache' "$url" || true)
  code=$(curl -sL -m 45 -o /dev/null -w '%{http_code}' -H 'Cache-Control: no-cache' "$url" || echo "000")
  if [[ "$code" != "200" ]]; then
    echo "VERIFY_FAIL http=$code url=$url" >&2
    fail=1
    continue
  fi
  # Count h1 tags (case insensitive)
  h1c=$(printf '%s' "$html" | grep -oi '<h1[^>]*>' | wc -l | tr -d ' ')
  if [[ "$h1c" -ne 1 ]]; then
    echo "VERIFY_FAIL h1_count=$h1c url=$url" >&2
    fail=1
  else
    echo "VERIFY_OK h1=1 url=$url"
  fi
  case "$path" in
    /)
      if ! printf '%s' "$html" | grep -qi 'lireate-home-dark'; then
        echo "VERIFY_FAIL home missing lireate-home-dark in HTML" >&2
        fail=1
      else
        echo "VERIFY_OK body_class home=lireate-home-dark"
      fi
      ;;
    /reviews/)
      if ! printf '%s' "$html" | grep -qi 'lireate-static-lu'; then
        echo "VERIFY_FAIL reviews missing lireate-static-lu" >&2
        fail=1
      else
        echo "VERIFY_OK body_class reviews=lireate-static-lu"
      fi
      ;;
    /poisk_tovarnyh_znakov/)
      if ! printf '%s' "$html" | grep -qi 'lireate-legacy-cms-lu'; then
        echo "VERIFY_FAIL poisk missing lireate-legacy-cms-lu" >&2
        fail=1
      else
        echo "VERIFY_OK body_class poisk=lireate-legacy-cms-lu"
      fi
      ;;
  esac
done

if [[ "$fail" -ne 0 ]]; then
  echo "POST_DEPLOY_VERIFY_FAILED" >&2
  exit 1
fi
echo "POST_DEPLOY_VERIFY_OK"
