#!/usr/bin/env bash
# HOME_SERVICE_URLS on dock v2 drift fixture + marker guard via patch_lib.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-python3}"
export LIREATE_MAIN_MIN_LINES=6000
export REPO LIREATE_DESIGN_PYTHON="$PY"

# shellcheck source=scripts/lireate_main_php_guard.sh
source "$REPO/scripts/lireate_main_php_guard.sh"
# shellcheck source=scripts/lireate_design_main_php_patch_lib.sh
source "$REPO/scripts/lireate_design_main_php_patch_lib.sh"

"$PY" "$REPO/scripts/lireate_design_dock_main_fixture.py"
BASE="$REPO/tests/fixtures/main-php-v120-dock-v2-body-drift.php"
WORK="${BASE}.home-urls"
cp -a "$BASE" "$WORK"

"$PY" - "$WORK" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
t = path.read_text(encoding="utf-8")
snip = (
    'var lurl = [["/reg-tz-main","/findtz","#","#","#","#"],\n'
    '\t\t\t\t\t["#","#","#","#"],\n'
    '\t\t\t\t\t["/patent_prom_obr","#","/findtz"],\n'
    '\t\t\t\t\t["#","#","#"]]; // массив ссылок\n'
    '<div class="btn content-button red js-modal-form" data-toggle="modal" id="dog_but" '
    'style="margin-bottom:0px;" data-lx-home-modal-form="1">'
    '<!-- lireate_design_home_modal_form_btns_v1 -->Подробнее</div>\n'
    '<div class="btn content-button red js-modal-form" data-toggle="modal" id="pro_but" '
    'style="margin-bottom:0px;">Подробнее</div>\n'
)
if "var lurl" not in t:
    t = t.replace(
        "<main>Fixture v2 drift</main>",
        "<main>Fixture v2 drift\n" + snip + "</main>",
        1,
    )
    path.write_text(t, encoding="utf-8")
PY

cp -a "$WORK" "${WORK}.pre-design-patch"
lireate_design_patch_main_php "$WORK" "$REPO/scripts/lireate_design_patch_home_service_urls.py" "home_svc_urls_test"
grep -q 'lireate_design_home_service_urls_v1' "$WORK"
grep -q 'href="/dogovory/"' "$WORK"
grep -q '/registraciya_programm_evm/' "$WORK"
grep -q 'lireate-home-dark' "$WORK"
rm -f "$WORK" "${WORK}.pre-design-patch" "${WORK}."*
echo "HOME_SERVICE_URLS_SELFTEST_OK"
