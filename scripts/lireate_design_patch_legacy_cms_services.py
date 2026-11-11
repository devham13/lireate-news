#!/usr/bin/env python3
"""Legacy CMS service URLs (poisk/ekspertiza/…) → dark LU + legacy-cms-lu.css."""
import re
import subprocess
import sys
from pathlib import Path

MARK = "lireate_design_legacy_cms_services_v1"
PAGEKEY_MARK = "lireate_hide_pagekey_v1"
MIN_LINES = 6000
PAGE_CONTAINER = "page_container"

URI_REGEX = (
    "#^/(?:poisk_tovarnyh_znakov|ekspertiza_tovarnogo_znaka|"
    "mezhdunarodnaja_registracija_tovarnogo_znaka|"
    "registracija_torgovyh_marok_i_logotipov)"
    "(?:/|$)#"
)

LEGACY_BODY_ECHO = " lireate-cms-page-dark lireate-legacy-cms-lu"

BODY_SNIP = (
    f" /* {MARK} body */ $_lx_leg_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';"
    f" if (preg_match('{URI_REGEX}', $_lx_leg_svc_ru)) echo '{LEGACY_BODY_ECHO}';"
)

BODY_SNIP_LEGACY = (
    f" /* {MARK} */ $_lx_leg_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';"
    f" if (preg_match('{URI_REGEX}', $_lx_leg_svc_ru)) echo '{LEGACY_BODY_ECHO}';"
)

HEAD_BLOCK = f"""\t<?php /* {MARK} head */ $_lx_leg_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\tif (preg_match('{URI_REGEX}', $_lx_leg_svc_ru)): ?>
\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" />
\t<link rel="stylesheet" href="/template/css/lireate-cms-page-dark.css?v=20261111design3" />
\t<link rel="stylesheet" href="/template/css/lireate-legacy-cms-lu.css?v=20261111leg3" />
\t<link rel="stylesheet" href="/template/css/lireate-lu-viewport.css?v=20261111vp4" />
\t<link rel="stylesheet" href="/template/css/lireate-home-modal-lu.css?v=20261111mod2" />
\t<script defer src="/template/js/lireate-home-modal-lu.js?v=20261111mod2"></script>
\t<?php endif; ?>
"""

HOME_ANCHOR = " if ($temp['page']==='home') echo ' lireate-home-dark';"
HOME_ANCHORS = (
    HOME_ANCHOR,
    " if($temp['page']=='home') echo ' lireate-home-dark';",
    " if($temp['page']=='home') echo ' lireate-home-dark';?>",
)
DOCK_V2_BODY = "/* lireate_design_service_mobile_dock_v2 body */"
DOCK_V1_BODY = "/* lireate_design_service_mobile_dock_v1 body */"

PAGEKEY_COMMENT = f"/* {PAGEKEY_MARK} */"
PAGEKEY_BOTCH_TAG = re.compile(
    r"<\?php\s*/\*\s*lireate_hide_pagekey_v1\s*\*/\s*\?>",
    re.I,
)
PAGEKEY_ECHO_LINE = re.compile(r"(?m)^(\s*)echo\s+\$temp\['pagekey'\]\s*;\s*$")
PAGEKEY_ECHO_SHORT_TAG = re.compile(
    r"<\?php\s+echo\s+\$temp\['pagekey'\]\s*;\s*\?>",
    re.I,
)
PAGEKEY_ECHO_ECHO_TAG = re.compile(r"<\?=\s*\$temp\['pagekey'\]\s*\?>", re.I)


def _validate(text: str, label: str) -> None:
    if text.count("\n") + 1 < MIN_LINES:
        raise SystemExit(f"{label}: main.php too short")
    if PAGE_CONTAINER not in text:
        raise SystemExit(f"{label}: missing {PAGE_CONTAINER}")


def _php_lint(content: str) -> None:
    tmp = Path("/tmp/lireate-main-php-legacy-svc.php")
    tmp.write_text(content, encoding="utf-8")
    r = subprocess.run(
        ["php", "-l", str(tmp)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if r.returncode != 0:
        raise SystemExit(f"php -l failed: {r.stderr or r.stdout}")


def _has_legacy_body(text: str) -> bool:
    if "lireate-legacy-cms-lu" not in text:
        return False
    if f"/* {MARK} body */" in text or BODY_SNIP_LEGACY in text:
        return True
    return bool(
        re.search(
            r"preg_match\('\#\^\(/\(?:poisk_tovarnyh_znakov|ekspertiza",
            text,
        )
        and LEGACY_BODY_ECHO in text
    )


def _insert_legacy_body(text: str) -> str:
    if _has_legacy_body(text):
        return text
    compact = BODY_SNIP.replace("\n", " ")
    for anchor in HOME_ANCHORS:
        if anchor in text:
            return text.replace(anchor, compact + anchor, 1)
    if DOCK_V2_BODY in text:
        return text.replace(DOCK_V2_BODY, DOCK_V2_BODY + " " + compact, 1)
    if DOCK_V1_BODY in text:
        return text.replace(DOCK_V1_BODY, DOCK_V1_BODY + " " + compact, 1)
    if HOME_ANCHOR in text:
        return text.replace(HOME_ANCHOR, compact + HOME_ANCHOR, 1)
    return text


def _normalize_legacy_body_marker(text: str) -> str:
    if BODY_SNIP_LEGACY in text and f"/* {MARK} body */" not in text:
        return text.replace(BODY_SNIP_LEGACY, BODY_SNIP.replace("\n", " "), 1)
    return text


def _hide_pagekey(text: str) -> str:
    """Replace pagekey echo with inline PHP comment (safe inside open <?php blocks)."""
    text = PAGEKEY_BOTCH_TAG.sub(PAGEKEY_COMMENT, text)
    text = PAGEKEY_ECHO_LINE.sub(rf"\1{PAGEKEY_COMMENT}", text)
    text = PAGEKEY_ECHO_SHORT_TAG.sub(PAGEKEY_COMMENT, text)
    text = PAGEKEY_ECHO_ECHO_TAG.sub(PAGEKEY_COMMENT, text)
    return text


def patch(text: str) -> str:
    _validate(text, "before legacy_cms_services")
    text = _normalize_legacy_body_marker(text)
    text = _insert_legacy_body(text)
    if f"{MARK} head" not in text and "</head>" in text:
        text = text.replace("</head>", HEAD_BLOCK + "</head>", 1)
    text = _hide_pagekey(text)
    if f"{MARK} head" in text and not _has_legacy_body(text):
        raise SystemExit(f"{MARK}: head present but body class snippet missing (anchor not found)")
    _validate(text, "after legacy_cms_services")
    return text


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: patch_legacy_cms_services.py main.php")
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw)
    if out == raw:
        print("UNCHANGED")
        return
    _php_lint(out)
    path.write_text(out, encoding="utf-8")
    print("LEGACY_CMS_SERVICES_PATCH_OK")


if __name__ == "__main__":
    main()
