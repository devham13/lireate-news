#!/usr/bin/env python3
"""Build padded main.php fixture with live-like <body class=…> + inline pagekey block."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "fixtures" / "main-php-hosting-live-body-v1.php"
MIN_LINES = 6100

# Mirrors hosting main.php ~381–386: pagekey echo inside multi-line <?php, not a new tag.
PAGEKEY_BLOCK = """    <?php 
    
        echo $temp['pagekey'];
        include ('./template/parts/online.php');
    ?>
"""


def main() -> None:
    body = (
        "<?php\n"
        "// page_container\n"
        "$temp = array('page' => 'poisk_tovarnyh_znakov');\n"
        "?>\n"
        "<html><head></head>\n"
        '<body class="cms-default<?php '
        "/* lireate_cms_dark_body_v1 */ "
        "if (in_array($temp['page'], array('home','patent','patent_prom_obr','mktu','mktu1'), true)) "
        "echo ' lireate-cms-page-dark'; "
        "if ($temp['page']==='home') echo ' lireate-home-dark';"
        " /* lireate_design_service_mobile_dock_v2 body */ "
        "$_lx_svc_dock_pg = array('patent','poisk_tovarnyh_znakov'); "
        "if (in_array($temp['page'], $_lx_svc_dock_pg, true)) "
        "echo ' lireate-svc-body lireate-service-mobile-dock';"
        '?>\">\n'
        f"{PAGEKEY_BLOCK}"
        "<main>Fixture</main>\n"
        "\t<?php /* lireate_site_footer_v1 */ ?>\n"
        "</body></html>\n"
    )
    lines = body.splitlines(keepends=True)
    pad = MIN_LINES - len(lines)
    if pad > 0:
        lines.extend(f"<!-- fixture-pad-{i} -->\n" for i in range(pad))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print("LIVE_BODY_FIXTURE_OK", OUT, len(lines))


if __name__ == "__main__":
    main()
