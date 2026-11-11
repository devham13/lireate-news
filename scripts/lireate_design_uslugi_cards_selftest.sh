#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-python3}"
TMP="$(mktemp -d)"
mkdir -p "$TMP/template/page/uslugi"
cp -a "$REPO/tests/fixtures/lireate-uslugi-lib-contact-anchor.php" \
  "$TMP/template/page/uslugi/lireate-uslugi-lib.php"
"$PY" "$REPO/scripts/lireate_design_patch_uslugi_cards.py" "$TMP"
grep -q 'lireate_design_uslugi_dogovory_evm_v1' "$TMP/template/page/uslugi/lireate-uslugi-lib.php"
grep -q 'href="/dogovory/"' "$TMP/template/page/uslugi/lireate-uslugi-lib.php"
grep -q 'href="/registraciya_programm_evm/"' "$TMP/template/page/uslugi/lireate-uslugi-lib.php"
rm -rf "$TMP"
echo "USLUGI_CARDS_SELFTEST_OK"
