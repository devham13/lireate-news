#!/usr/bin/env bash
# After design deploy: HTTP 200, one <h1>, body LU markers (with opcache-aware retry).
set -euo pipefail

SITE="${LIREATE_PUBLIC_SITE_URL:?}"
SITE="${SITE%/}"

REPO="${REPO:-$(cd "$(dirname "$0")/.." && pwd)}"
BODY_RETRIES="${LIREATE_VERIFY_BODY_RETRIES:-10}"
BODY_SLEEP="${LIREATE_VERIFY_BODY_SLEEP:-15}"
DOCROOT="${LIREATE_DOCROOT:-}"

if [[ -n "$DOCROOT" && -f "$DOCROOT/template/main.php" ]]; then
  PY="$(command -v python3)"
  INV="$REPO/scripts/lireate_design_opcache_invalidate_cli.py"
  if [[ -n "${REPO:-}" && -f "$INV" ]]; then
  "$PY" "$INV" "$DOCROOT/template/main.php" 2>/dev/null || true
  fi
fi

curl_fetch() {
  local url="$1"
  curl -sL -m 45 -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' "$url" || true
}

curl_code() {
  local url="$1"
  curl -sL -m 45 -o /dev/null -w '%{http_code}' -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' "$url" || echo "000"
}

verify_page() {
  local path="$1"
  local need_body_grep="${2:-}"
  local url="${SITE}${path}"
  local tries=1
  local sleep_s=0
  if [[ -n "$need_body_grep" ]]; then
    tries="$BODY_RETRIES"
    sleep_s="$BODY_SLEEP"
  fi
  local attempt html code h1c
  for ((attempt = 1; attempt <= tries; attempt++)); do
    html="$(curl_fetch "$url")"
    code="$(curl_code "$url")"
    if [[ "$code" != "200" ]]; then
      if [[ "$attempt" -lt "$tries" ]]; then
        echo "VERIFY_RETRY http=$code attempt=$attempt/$tries url=$url" >&2
        sleep "$sleep_s"
        continue
      fi
      echo "VERIFY_FAIL http=$code url=$url" >&2
      return 1
    fi
    h1c=$(printf '%s' "$html" | grep -oi '<h1[^>]*>' | wc -l | tr -d ' ')
    if [[ "$h1c" -ne 1 ]]; then
      if [[ "$attempt" -lt "$tries" ]]; then
        echo "VERIFY_RETRY h1_count=$h1c attempt=$attempt/$tries url=$url" >&2
        sleep "$sleep_s"
        continue
      fi
      echo "VERIFY_FAIL h1_count=$h1c url=$url" >&2
      return 1
    fi
    if [[ -n "$need_body_grep" ]]; then
      if ! printf '%s' "$html" | grep -qi "$need_body_grep"; then
        if [[ "$attempt" -lt "$tries" ]]; then
          echo "VERIFY_RETRY body_marker missing ($need_body_grep) attempt=$attempt/$tries url=$url" >&2
          sleep "$sleep_s"
          continue
        fi
        echo "VERIFY_FAIL body missing pattern=$need_body_grep url=$url" >&2
        return 1
      fi
      echo "VERIFY_OK h1=1 body=$need_body_grep url=$url (attempt $attempt)"
      return 0
    fi
    echo "VERIFY_OK h1=1 url=$url"
    return 0
  done
  return 1
}

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

ARTICLE_PATH="${LIREATE_VERIFY_ARTICLE_PATH:-/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/}"
urls+=("$ARTICLE_PATH")

fail=0
for path in "${urls[@]}"; do
  case "$path" in
    /) marker="lireate-home-dark" ;;
    /reviews/) marker="lireate-static-lu" ;;
    /poisk_tovarnyh_znakov/) marker="lireate-legacy-cms-lu" ;;
    *) marker="" ;;
  esac
  if ! verify_page "$path" "$marker"; then
    fail=1
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "POST_DEPLOY_VERIFY_FAILED" >&2
  exit 1
fi
echo "POST_DEPLOY_VERIFY_OK"
