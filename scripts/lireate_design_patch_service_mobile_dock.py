#!/usr/bin/env python3
"""Inject mobile service dock (4-button bar) on CMS / legacy service routes via main.php."""
import re
import sys
from pathlib import Path

MARK = "lireate_design_service_mobile_dock_v1"
MIN_LINES = 6000

CMS_PAGES_PHP = (
    "array('patent','patent_prom_obr','mktu','mktu1','uslugi',"
    "'poisk_tovarnyh_znakov','ekspertiza_tovarnogo_znaka',"
    "'mezhdunarodnaja_registracija_tovarnogo_znaka',"
    "'registracija_torgovyh_marok_i_logotipov')"
)

URI_REGEX = (
    "#^/(?:findtz|registraciya_tovarnogo_znaka(?:_s_oplatoy_za_rezultat)?|"
    "prodlenie_tovarnogo_znaka|vozrazhenie_protiv_registracii_tovarnogo_znaka|"
    "registraciya_tovarnogo_znaka_v_kitae|zashchita_avtorskih_prav|"
    "poisk_tovarnyh_znakov|ekspertiza_tovarnogo_znaka|"
    "mezhdunarodnaja_registracija_tovarnogo_znaka|"
    "registracija_torgovyh_marok_i_logotipov|patent_prom_obr|patent|mktu|uslugi)"
    "(?:/|$)#"
)

HEAD_BLOCK = f"""\t<?php /* {MARK} head */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};
\t$_lx_svc_dock = in_array($temp['page'], $_lx_svc_dock_pg, true);
\tif (!$_lx_svc_dock) {{
\t  $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\t  $_lx_svc_dock = (bool) preg_match('{URI_REGEX}', $_lx_svc_ru);
\t}}
\tif ($_lx_svc_dock): ?>
\t<link rel="stylesheet" href="/template/css/lireate-service-mobile-bar.css?v=20261111svc1" />
\t<script defer src="/template/js/lireate-service-mobile-bar.js?v=20261111svc1"></script>
\t<script defer src="/template/js/lireate-service-metrika-goals.js?v=20261111svc1"></script>
\t<?php endif; ?>
"""

BODY_SNIP = f""" /* {MARK} body */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};
 if (in_array($temp['page'], $_lx_svc_dock_pg, true)) echo ' lireate-svc-body lireate-service-mobile-dock';
 else {{
   $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
   if (preg_match('{URI_REGEX}', $_lx_svc_ru)) echo ' lireate-svc-body lireate-service-mobile-dock';
 }}"""

FOOTER_BLOCK = f"""\t<?php /* {MARK} footer */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};
\t$_lx_svc_dock = in_array($temp['page'], $_lx_svc_dock_pg, true);
\tif (!$_lx_svc_dock) {{
\t  $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\t  $_lx_svc_dock = (bool) preg_match('{URI_REGEX}', $_lx_svc_ru);
\t}}
\tif ($_lx_svc_dock) {{
\t  include __DIR__ . '/lireate/lireate-service-mobile-bar.inc.php';
\t}}
?>
"""

FOOTER_ANCHOR = "\t<?php /* lireate_site_footer_v1"


def patch(text: str) -> str:
    if text.count("\n") < MIN_LINES:
        raise SystemExit("main.php too short")

    if MARK not in text:
        if "</head>" in text and f"{MARK} head" not in text:
            text = text.replace("</head>", HEAD_BLOCK + "</head>", 1)

        if "lireate_cms_dark_body_v1" in text or "lireate-home-dark" in text:
            anchor = " if ($temp['page']==='home') echo ' lireate-home-dark';"
            if anchor in text and MARK not in text:
                text = text.replace(anchor, anchor + BODY_SNIP, 1)
            elif "lireate-uslugi-body" in text:
                idx = text.find("lireate-uslugi-body")
                semi = text.find(";", idx)
                text = text[: semi + 1] + BODY_SNIP + text[semi + 1 :]

        if FOOTER_ANCHOR in text:
            text = text.replace(FOOTER_ANCHOR, FOOTER_BLOCK + FOOTER_ANCHOR, 1)
        elif "</body>" in text and f"{MARK} footer" not in text:
            text = text.replace("</body>", FOOTER_BLOCK + "</body>", 1)

    return text


def main() -> None:
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw)
    path.write_text(out, encoding="utf-8")
    print("SERVICE_MOBILE_DOCK_PATCH_OK" if MARK in out else "SERVICE_MOBILE_DOCK_PATCH_PARTIAL")


if __name__ == "__main__":
    main()
