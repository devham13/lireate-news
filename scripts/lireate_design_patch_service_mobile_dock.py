#!/usr/bin/env python3
"""Inject mobile service dock on CMS / legacy service routes via main.php (not LU index.php)."""
import re
import sys
from pathlib import Path

MARK = "lireate_design_service_mobile_dock_v1"
MARK2 = "lireate_design_service_mobile_dock_v2"
MIN_LINES = 6000

CMS_PAGES_PHP = (
    "array('patent','patent_prom_obr','mktu','mktu1','uslugi',"
    "'poisk_tovarnyh_znakov','ekspertiza_tovarnogo_znaka',"
    "'mezhdunarodnaja_registracija_tovarnogo_znaka',"
    "'registracija_torgovyh_marok_i_logotipov')"
)

# Legacy CMS slugs only — LU landings have their own index.php + embedded bar.
URI_LEGACY_REGEX = (
    "#^/(?:poisk_tovarnyh_znakov|ekspertiza_tovarnogo_znaka|"
    "mezhdunarodnaja_registracija_tovarnogo_znaka|"
    "registracija_torgovyh_marok_i_logotipov)"
    "(?:/|$)#"
)

STANDALONE_LU_REGEX = (
    "#^/(?:findtz|registraciya_tovarnogo_znaka(?:_s_oplatoy_za_rezultat|_v_kitae)?|"
    "prodlenie_tovarnogo_znaka|vozrazhenie_protiv_registracii_tovarnogo_znaka|"
    "zashchita_avtorskih_prav)(?:/|$)#"
)


def _dock_condition_php() -> str:
    return f"""$_lx_svc_dock_pg = {CMS_PAGES_PHP};
\t$_lx_svc_dock = in_array($temp['page'], $_lx_svc_dock_pg, true);
\tif (!$_lx_svc_dock) {{
\t  $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\t  $_lx_svc_dock = (bool) preg_match('{URI_LEGACY_REGEX}', $_lx_svc_ru);
\t}}
\tif ($_lx_svc_dock) {{
\t  $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\t  if (preg_match('{STANDALONE_LU_REGEX}', $_lx_svc_ru)) {{
\t    $_lx_svc_dock = false;
\t  }}
\t}}"""


HEAD_BLOCK = f"""\t<?php /* {MARK2} head */ {_dock_condition_php()}
\tif ($_lx_svc_dock): ?>
\t<link rel="stylesheet" href="/template/css/lireate-service-mobile-bar.css?v=20261111svc2" />
\t<script defer src="/template/js/lireate-service-mobile-bar.js?v=20261111svc2"></script>
\t<script defer src="/template/js/lireate-service-metrika-goals.js?v=20261111svc2"></script>
\t<?php endif; ?>
"""

BODY_SNIP = f""" /* {MARK2} body */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};
 if (in_array($temp['page'], $_lx_svc_dock_pg, true)) echo ' lireate-svc-body lireate-service-mobile-dock';
 else {{
   $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
   if (preg_match('{URI_LEGACY_REGEX}', $_lx_svc_ru) && !preg_match('{STANDALONE_LU_REGEX}', $_lx_svc_ru)) {{
     echo ' lireate-svc-body lireate-service-mobile-dock';
   }}
 }}"""

FOOTER_BLOCK = f"""\t<?php /* {MARK2} footer */ {_dock_condition_php()}
\tif ($_lx_svc_dock) {{
\t  include __DIR__ . '/lireate/lireate-service-mobile-bar.inc.php';
\t}}
?>
"""

FOOTER_ANCHOR = "\t<?php /* lireate_site_footer_v1"

V1_HEAD_RE = re.compile(
    r"\t<\?php /\* lireate_design_service_mobile_dock_v1 head \*/.*?"
    r"\t<\?php endif; \?>\s*\n",
    re.S,
)
V1_FOOTER_RE = re.compile(
    r"\t<\?php /\* lireate_design_service_mobile_dock_v1 footer \*/.*?"
    r"\?\>\s*\n",
    re.S,
)
V1_BODY_RE = re.compile(
    r" /\* lireate_design_service_mobile_dock_v1 body \*/[\s\S]*?\}\s*\}",
    re.M,
)
V2_HEAD_RE = re.compile(
    r"\t<\?php /\* lireate_design_service_mobile_dock_v2 head \*/.*?"
    r"\t<\?php endif; \?>\s*\n",
    re.S,
)
V2_FOOTER_RE = re.compile(
    r"\t<\?php /\* lireate_design_service_mobile_dock_v2 footer \*/.*?"
    r"\?\>\s*\n",
    re.S,
)


def _upgrade_dock_blocks(text: str) -> str:
    if V1_BODY_RE.search(text):
        text = V1_BODY_RE.sub(BODY_SNIP, text, count=1)
    if V2_HEAD_RE.search(text):
        text = V2_HEAD_RE.sub(HEAD_BLOCK, text, count=1)
    elif V1_HEAD_RE.search(text):
        text = V1_HEAD_RE.sub(HEAD_BLOCK, text, count=1)
    if V2_FOOTER_RE.search(text):
        text = V2_FOOTER_RE.sub(FOOTER_BLOCK, text, count=1)
    elif V1_FOOTER_RE.search(text):
        text = V1_FOOTER_RE.sub(FOOTER_BLOCK, text, count=1)
    return text


def patch(text: str) -> str:
    if text.count("\n") < MIN_LINES:
        raise SystemExit("main.php too short")

    text = _upgrade_dock_blocks(text)

    if f"{MARK2} head" not in text and "</head>" in text:
        text = text.replace("</head>", HEAD_BLOCK + "</head>", 1)

    if f"{MARK2} body" not in text and "lireate_design_service_mobile_dock_v1 body" not in text:
        anchor = " if ($temp['page']==='home') echo ' lireate-home-dark';"
        if anchor in text and BODY_SNIP not in text:
            text = text.replace(anchor, anchor + BODY_SNIP, 1)

    if f"{MARK2} footer" not in text and "lireate-service-mobile-bar.inc.php" not in text:
        if FOOTER_ANCHOR in text:
            text = text.replace(FOOTER_ANCHOR, FOOTER_BLOCK + FOOTER_ANCHOR, 1)
        elif "</body>" in text:
            text = text.replace("</body>", FOOTER_BLOCK + "</body>", 1)

    return text


def main() -> None:
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw)
    path.write_text(out, encoding="utf-8")
    print("SERVICE_MOBILE_DOCK_PATCH_OK", MARK2 in out)


if __name__ == "__main__":
    main()
