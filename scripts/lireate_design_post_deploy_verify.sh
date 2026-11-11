#!/usr/bin/env bash
# After design deploy: HTTP 200, one <h1>, body LU markers (with opcache-aware retry).
set -euo pipefail

SITE="${LIREATE_PUBLIC_SITE_URL:?}"
SITE="${SITE%/}"

REPO="${REPO:-$(cd "$(dirname "$0")/.." && pwd)}"
BODY_RETRIES="${LIREATE_VERIFY_BODY_RETRIES:-10}"
BODY_SLEEP="${LIREATE_VERIFY_BODY_SLEEP:-15}"
DOCROOT="${LIREATE_DOCROOT:-}"
VERIFY_LOG="${LIREATE_VERIFY_BODY_LOG:-}"

VERIFY_PY="${LIREATE_DESIGN_PYTHON:-}"
if [[ -z "$VERIFY_PY" && -f "$REPO/scripts/lireate_design_resolve_python.sh" ]]; then
  # shellcheck source=scripts/lireate_design_resolve_python.sh
  source "$REPO/scripts/lireate_design_resolve_python.sh"
  VERIFY_PY="$(lireate_design_resolve_python)"
fi
VERIFY_PY="${VERIFY_PY:-$(command -v python3)}"
INV="$REPO/scripts/lireate_design_opcache_invalidate_cli.py"

lireate_verify_invalidate_opcache() {
  if [[ -n "$DOCROOT" && -f "$DOCROOT/template/main.php" && -f "$INV" ]]; then
    "$VERIFY_PY" "$INV" "$DOCROOT/template/main.php" 2>/dev/null || true
  fi
}
lireate_verify_invalidate_opcache

lireate_verify_body_open_tag() {
  local html="$1"
  printf '%s' "$html" | tr '\n' ' ' | grep -oiE '<body[^>]+>' | head -1
}

lireate_verify_log_body_fail() {
  local url="$1" pattern="$2" body_tag="$3"
  local line="VERIFY_BODY_TAG url=$url pattern=$pattern tag=${body_tag:-EMPTY}"
  echo "$line" >&2
  if [[ -n "$VERIFY_LOG" ]]; then
    printf '%s\n' "$line" >>"$VERIFY_LOG"
  fi
}

curl_common_headers=(-H 'Cache-Control: no-cache' -H 'Pragma: no-cache')

curl_fetch() {
  local url="$1"
  local attempt="${2:-1}"
  curl -sL -m 45 "${curl_common_headers[@]}" \
    -H "X-Lireate-Deploy-Verify: ${attempt}-$RANDOM" \
    "$url" || true
}

curl_code() {
  local url="$1"
  local attempt="${2:-1}"
  curl -sL -m 45 -o /dev/null -w '%{http_code}' "${curl_common_headers[@]}" \
    -H "X-Lireate-Deploy-Verify: ${attempt}-$RANDOM" \
    "$url" || echo "000"
}

verify_page() {
  local path="$1"
  local need_body_grep="${2:-}"
  local alt_body_grep="${3:-}"
  local url="${SITE}${path}"
  local tries=1
  local sleep_s=0
  if [[ -n "$need_body_grep" ]]; then
    tries="$BODY_RETRIES"
    sleep_s="$BODY_SLEEP"
  fi
  local attempt html code h1c body_tag
  for ((attempt = 1; attempt <= tries; attempt++)); do
  if [[ -n "$need_body_grep" && $((attempt % 3)) -eq 1 ]]; then
      lireate_verify_invalidate_opcache
    fi
    url="${SITE}${path}"
    html="$(curl_fetch "$url" "$attempt")"
    code="$(curl_code "$url" "$attempt")"
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
      body_tag="$(lireate_verify_body_open_tag "$html")"
      local found=0
      if printf '%s' "$body_tag" | grep -qi "$need_body_grep"; then
        found=1
      elif [[ -n "$alt_body_grep" ]] && printf '%s' "$body_tag" | grep -qi "$alt_body_grep"; then
        found=1
      fi
      if [[ "$found" -ne 1 ]]; then
        if [[ "$attempt" -lt "$tries" ]]; then
          echo "VERIFY_RETRY body_marker missing ($need_body_grep) attempt=$attempt/$tries url=$url" >&2
          sleep "$sleep_s"
          continue
        fi
        lireate_verify_log_body_fail "$url" "$need_body_grep" "$body_tag"
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
  "/reviews"
  "/poisk_tovarnyh_znakov/"
)

ARTICLE_PATH="${LIREATE_VERIFY_ARTICLE_PATH:-/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/}"
urls+=("$ARTICLE_PATH")

fail=0
for path in "${urls[@]}"; do
  marker=""
  alt_marker=""
  case "$path" in
    /) marker="lireate-home-dark"; alt_marker="lireate-home-lu-body" ;;
    /reviews) marker="lireate-static-lu"; alt_marker="lireate-reviews-body" ;;
    /poisk_tovarnyh_znakov/)
      marker="lireate-legacy-cms-lu"
      alt_marker="lireate_design_legacy_cms_services_v1"
      ;;
  esac
  if ! verify_page "$path" "$marker" "$alt_marker"; then
    fail=1
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "POST_DEPLOY_VERIFY_FAILED" >&2
  exit 1
fi
echo "POST_DEPLOY_VERIFY_OK"
