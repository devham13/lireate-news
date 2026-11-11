#!/usr/bin/env python3
"""Mobile service dock in main.php — v2 (excludes standalone LU; safe v1→v2 body replace)."""
import os
import re
import subprocess
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

URI_REGEX_V1 = (
    "#^/(?:findtz|registraciya_tovarnogo_znaka(?:_s_oplatoy_za_rezultat)?|"
    "prodlenie_tovarnogo_znaka|vozrazhenie_protiv_registracii_tovarnogo_znaka|"
    "registraciya_tovarnogo_znaka_v_kitae|zashchita_avtorskih_prav|"
    "poisk_tovarnyh_znakov|ekspertiza_tovarnogo_znaka|"
    "mezhdunarodnaja_registracija_tovarnogo_znaka|"
    "registracija_torgovyh_marok_i_logotipov|patent_prom_obr|patent|mktu|uslugi)"
    "(?:/|$)#"
)

URI_LEGACY_REGEX = (
    "#^/(?:mktu1?|poisk_tovarnyh_znakov|ekspertiza_tovarnogo_znaka|"
    "mezhdunarodnaja_registracija_tovarnogo_znaka|"
    "registracija_torgovyh_marok_i_logotipov)"
    "(?:/|$)#"
)

URI_LEGACY_REGEX_OLD = (
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

V1_BODY_SNIP = (
    f" /* {MARK} body */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};\n"
    f" if (in_array($temp['page'], $_lx_svc_dock_pg, true)) echo ' lireate-svc-body lireate-service-mobile-dock';\n"
    f" else {{\n"
    f"   $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';\n"
    f"   if (preg_match('{URI_REGEX_V1}', $_lx_svc_ru)) echo ' lireate-svc-body lireate-service-mobile-dock';\n"
    f" }}"
)

V1_HEAD_BLOCK = f"""\t<?php /* {MARK} head */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};
\t$_lx_svc_dock = in_array($temp['page'], $_lx_svc_dock_pg, true);
\tif (!$_lx_svc_dock) {{
\t  $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\t  $_lx_svc_dock = (bool) preg_match('{URI_REGEX_V1}', $_lx_svc_ru);
\t}}
\tif ($_lx_svc_dock): ?>
\t<link rel="stylesheet" href="/template/css/lireate-service-mobile-bar.css?v=20261111svc1" />
\t<script defer src="/template/js/lireate-service-mobile-bar.js?v=20261111svc1"></script>
\t<script defer src="/template/js/lireate-service-metrika-goals.js?v=20261111svc1"></script>
\t<?php endif; ?>
"""

V1_FOOTER_BLOCK = f"""\t<?php /* {MARK} footer */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};
\t$_lx_svc_dock = in_array($temp['page'], $_lx_svc_dock_pg, true);
\tif (!$_lx_svc_dock) {{
\t  $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\t  $_lx_svc_dock = (bool) preg_match('{URI_REGEX_V1}', $_lx_svc_ru);
\t}}
\tif ($_lx_svc_dock) {{
\t  include __DIR__ . '/lireate/lireate-service-mobile-bar.inc.php';
\t}}
?>
"""


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


# URI_LEGACY_REGEX appears 3×: head/footer dock condition + body else-branch.
HEAD_BLOCK = f"""\t<?php /* {MARK2} head */ {_dock_condition_php()}
\tif ($_lx_svc_dock): ?>
\t<link rel="stylesheet" href="/template/css/lireate-service-mobile-bar.css?v=20261111svc3" />
\t<script defer src="/template/js/lireate-service-mobile-bar.js?v=20261111svc3"></script>
\t<script defer src="/template/js/lireate-service-metrika-goals.js?v=20261111svc3"></script>
\t<?php endif; ?>
"""

BODY_SNIP = (
    f" /* {MARK2} body */ $_lx_svc_dock_pg = {CMS_PAGES_PHP};\n"
    f" if (in_array($temp['page'], $_lx_svc_dock_pg, true)) echo ' lireate-svc-body lireate-service-mobile-dock';\n"
    f" else {{\n"
    f"   $_lx_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';\n"
    f"   if (preg_match('{URI_LEGACY_REGEX}', $_lx_svc_ru) && !preg_match('{STANDALONE_LU_REGEX}', $_lx_svc_ru)) {{\n"
    f"     echo ' lireate-svc-body lireate-service-mobile-dock';\n"
    f"   }}\n"
    f" }}"
)

FOOTER_BLOCK = f"""\t<?php /* {MARK2} footer */ {_dock_condition_php()}
\tif ($_lx_svc_dock) {{
\t  include __DIR__ . '/lireate/lireate-service-mobile-bar.inc.php';
\t}}
?>
"""

FOOTER_ANCHOR = "\t<?php /* lireate_site_footer_v1"
HOME_ANCHOR = " if ($temp['page']==='home') echo ' lireate-home-dark';"

MARKED_PHP_RE = re.compile(
    r"\t<\?php /\* lireate_design_service_mobile_dock_v[12] (?:head|footer) \*/.*?"
    r"\?\>\s*\n",
    re.S,
)


def _replace_marked_php_block(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    return text


def _replace_body_snip(text: str) -> str:
    compact_v2 = BODY_SNIP.replace("\n", " ")
    if compact_v2 in text or BODY_SNIP in text:
        return text
    if V1_BODY_SNIP in text:
        return text.replace(V1_BODY_SNIP, compact_v2, 1)
    compact_v1 = V1_BODY_SNIP.replace("\n", " ")
    if compact_v1 in text:
        return text.replace(compact_v1, compact_v2, 1)
    if f"/* {MARK2} body */" in text:
        start = text.find(f"/* {MARK2} body */")
        end = text.find("?>", start)
        if end == -1:
            raise SystemExit("dock v2 body block: ?> not found after marker")
        return text[:start] + compact_v2 + text[end:]
    if f"/* {MARK} body */" in text and V1_BODY_SNIP not in text:
        raise SystemExit(
            "dock v1 body marker present but body snippet mismatch (main.php corrupt); "
            "restore main.php.bak-2026-11-11-design before re-run"
        )
    return text


def _upgrade_legacy_uri_regex(text: str) -> str:
    if URI_LEGACY_REGEX_OLD in text:
        return text.replace(URI_LEGACY_REGEX_OLD, URI_LEGACY_REGEX)
    return text


def _upgrade_dock_blocks(text: str) -> str:
    text = _upgrade_legacy_uri_regex(text)
    text = _replace_marked_php_block(text, V1_HEAD_BLOCK, HEAD_BLOCK)
    text = _replace_marked_php_block(text, V1_FOOTER_BLOCK, FOOTER_BLOCK)
    if f"/* {MARK2} head */" in text and V1_HEAD_BLOCK not in text:
        m = re.search(
            r"\t<\?php /\* lireate_design_service_mobile_dock_v2 head \*/.*?\t<\?php endif; \?>\s*\n",
            text,
            re.S,
        )
        if m:
            text = text[: m.start()] + HEAD_BLOCK + text[m.end() :]
    if f"/* {MARK2} footer */" in text and V1_FOOTER_BLOCK not in text:
        m = MARKED_PHP_RE.search(text)
        while m:
            if "footer" in m.group(0):
                text = text[: m.start()] + FOOTER_BLOCK + text[m.end() :]
                break
            m = MARKED_PHP_RE.search(text, m.end())
    text = _replace_body_snip(text)
    return text


def patch(text: str, *, min_lines: int = MIN_LINES) -> str:
    if text.count("\n") + 1 < min_lines:
        raise SystemExit(f"main.php too short (< {min_lines} lines)")
    text = _upgrade_dock_blocks(text)
    if f"{MARK2} head" not in text and "</head>" in text:
        text = text.replace("</head>", HEAD_BLOCK + "</head>", 1)
    if f"{MARK2} body" not in text and HOME_ANCHOR in text and BODY_SNIP not in text:
        text = text.replace(HOME_ANCHOR, HOME_ANCHOR + BODY_SNIP, 1)
    if (
        f"{MARK2} footer" not in text
        and "lireate-service-mobile-bar.inc.php" not in text
    ):
        if FOOTER_ANCHOR in text:
            text = text.replace(FOOTER_ANCHOR, FOOTER_BLOCK + FOOTER_ANCHOR, 1)
        elif "</body>" in text:
            text = text.replace("</body>", FOOTER_BLOCK + "</body>", 1)
    return text


def _php_lint(content: str) -> None:
    tmp = Path("/tmp/lireate-main-php-lint.php")
    tmp.write_text(content, encoding="utf-8")
    r = subprocess.run(
        ["php", "-l", str(tmp)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if r.returncode != 0:
        raise SystemExit(f"php -l failed: {r.stderr or r.stdout}")


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/main.php [--check]", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    check_only = "--check" in sys.argv
    min_lines = int(os.environ.get("LIREATE_MAIN_MIN_LINES", str(MIN_LINES)))
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw, min_lines=min_lines)
    if check_only:
        _php_lint(out)
        print("CHECK_OK", out.count("\n") + 1, MARK2 in out)
        return
    if out == raw:
        print("UNCHANGED")
        return
    _php_lint(out)
    path.write_text(out, encoding="utf-8")
    print("SERVICE_MOBILE_DOCK_PATCH_OK", MARK2 in out)


if __name__ == "__main__":
    main()
