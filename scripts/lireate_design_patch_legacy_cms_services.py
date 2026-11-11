#!/usr/bin/env python3
"""Legacy CMS service URLs (poisk/ekspertiza/…) → dark LU + legacy-cms-lu.css."""
import subprocess
import sys
from pathlib import Path

MARK = "lireate_design_legacy_cms_services_v1"
MIN_LINES = 6000
PAGE_CONTAINER = "page_container"

URI_REGEX = (
    "#^/(?:poisk_tovarnyh_znakov|ekspertiza_tovarnogo_znaka|"
    "mezhdunarodnaja_registracija_tovarnogo_znaka|"
    "registracija_torgovyh_marok_i_logotipov)"
    "(?:/|$)#"
)

BODY_SNIP = (
    f" /* {MARK} */ $_lx_leg_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';"
    f" if (preg_match('{URI_REGEX}', $_lx_leg_svc_ru))"
    " echo ' lireate-cms-page-dark lireate-legacy-cms-lu';"
)

HEAD_BLOCK = f"""\t<?php /* {MARK} head */ $_lx_leg_svc_ru = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
\tif (preg_match('{URI_REGEX}', $_lx_leg_svc_ru)): ?>
\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" />
\t<link rel="stylesheet" href="/template/css/lireate-cms-page-dark.css?v=20261111design3" />
\t<link rel="stylesheet" href="/template/css/lireate-legacy-cms-lu.css?v=20261111leg2" />
\t<link rel="stylesheet" href="/template/css/lireate-lu-viewport.css?v=20261111vp4" />
\t<link rel="stylesheet" href="/template/css/lireate-home-modal-lu.css?v=20261111mod2" />
\t<script defer src="/template/js/lireate-home-modal-lu.js?v=20261111mod2"></script>
\t<?php endif; ?>
"""


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


def patch(text: str) -> str:
    _validate(text, "before legacy_cms_services")
    if MARK not in text:
        anchor = " if($temp['page']=='home') echo ' lireate-home-dark';?>"
        if anchor in text and BODY_SNIP not in text:
            text = text.replace(anchor, BODY_SNIP + anchor, 1)
    if f"{MARK} head" not in text and "</head>" in text:
        text = text.replace("</head>", HEAD_BLOCK + "</head>", 1)
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
