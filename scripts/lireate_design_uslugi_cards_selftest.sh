#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-python3}"
TMP="$(mktemp -d)"
mkdir -p "$TMP/template/page/uslugi"

cp -a "$REPO/tests/fixtures/lireate-uslugi-cms-contact-anchor.inc.php" \
  "$TMP/template/page/uslugi/lireate-uslugi-cms.inc.php"
"$PY" "$REPO/scripts/lireate_design_patch_uslugi_cards.py" "$TMP"
grep -q 'lireate_design_uslugi_dogovory_evm_v1' "$TMP/template/page/uslugi/lireate-uslugi-cms.inc.php"
grep -q 'href="/dogovory/"' "$TMP/template/page/uslugi/lireate-uslugi-cms.inc.php"
grep -q 'href="/registraciya_programm_evm/"' "$TMP/template/page/uslugi/lireate-uslugi-cms.inc.php"
count="$(grep -c 'Договоры в сфере ИС' "$TMP/template/page/uslugi/lireate-uslugi-cms.inc.php" || true)"
[[ "$count" -eq 1 ]] || { echo "FAIL: duplicate dog card count=$count" >&2; exit 1; }
"$PY" "$REPO/scripts/lireate_design_patch_uslugi_cards.py" "$TMP" | grep -q 'already'

TMP2="$(mktemp -d)"
mkdir -p "$TMP2/template/page/uslugi"
cp -a "$REPO/tests/fixtures/lireate-uslugi-cms-cards-manual.inc.php" \
  "$TMP2/template/page/uslugi/lireate-uslugi-cms.inc.php"
out="$("$PY" "$REPO/scripts/lireate_design_patch_uslugi_cards.py" "$TMP2")"
echo "$out" | grep -q 'already'
count="$(grep -c 'Договоры в сфере ИС' "$TMP2/template/page/uslugi/lireate-uslugi-cms.inc.php" || true)"
[[ "$count" -eq 1 ]] || { echo "FAIL: manual fixture duplicated cards count=$count" >&2; exit 1; }

rm -rf "$TMP" "$TMP2"
echo "USLUGI_CARDS_SELFTEST_OK"
