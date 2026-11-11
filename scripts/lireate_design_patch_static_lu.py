#!/usr/bin/env python3
"""Расширить lireate-cms-page-dark на reviews/portfolio/spasibo/uslugi + static CSS."""
import re
import sys
from pathlib import Path

MARK = "lireate_design_static_lu_v1"
MARK_PAGES = "lireate_design_cms_dark_pages_v2"
MIN_LINES = 6000

DARK_PAGES = (
    "home','patent','patent_prom_obr','mktu','mktu1',"
    "'reviews','portfolio','spasibo','uslugi','avtor','team','partners','kontaktyi'"
)
DARK_ARRAY = f"array({DARK_PAGES})"

STATIC_BODY = (
    f" /* {MARK} */ "
    "$_lx_static = array('reviews','portfolio','spasibo','uslugi');"
    " if (in_array($temp['page'], $_lx_static, true)) echo ' lireate-static-lu';"
    " if ($temp['page']==='reviews') echo ' lireate-reviews-body';"
    " if ($temp['page']==='portfolio') echo ' lireate-portfolio-body';"
    " if ($temp['page']==='spasibo') echo ' lireate-spasibo-body';"
)

CSS_BLOCK = (
    f'\t<?php /* {MARK} head */ '
    "if (in_array($temp['page'], array('reviews','portfolio','spasibo','uslugi','avtor','team','partners','kontaktyi'), true)): ?>\n"
    '\t<link rel="stylesheet" href="/template/css/lireate-lu-viewport.css?v=20261111vp4" />\n'
    '\t<link rel="stylesheet" href="/template/css/lireate-static-pages-lu.css?v=20261111static1" />\n'
    '\t<link rel="stylesheet" href="/template/css/lireate-home-modal-lu.css?v=20261111mod2" />\n'
    '\t<script defer src="/template/js/lireate-home-modal-lu.js?v=20261111mod2"></script>\n'
    "\t<?php endif; ?>\n"
)


def patch(text: str) -> str:
    if text.count("\n") < MIN_LINES:
        raise SystemExit("main.php too short")

    # Expand cms dark pages array (idempotent marker)
    if MARK_PAGES not in text:
        text, n = re.subn(
            r"array\('home','patent','patent_prom_obr','mktu','mktu1'\)",
            f"/* {MARK_PAGES} */ {DARK_ARRAY}",
            text,
            count=1,
        )
        if n != 1:
            text, n2 = re.subn(
                r"array\([^)]*'mktu1'[^)]*\)",
                f"/* {MARK_PAGES} */ {DARK_ARRAY}",
                text,
                count=1,
            )
            if n2 != 1:
                raise SystemExit("cms dark pages array not found")

    if MARK not in text:
        anchor = " if($temp['page']=='uslugi') echo ' lireate-uslugi-body';"
        if anchor not in text:
            anchor = "lireate_cms_dark_body_v1"
            if anchor in text:
                idx = text.find(anchor)
                end = text.find(";", idx)
                text = text[:end] + ";" + STATIC_BODY + text[end + 1 :]
        else:
            text = text.replace(anchor, anchor + STATIC_BODY, 1)

    if f"{MARK} head" not in text and "lireate-static-pages-lu.css" not in text:
        if "</head>" in text:
            text = text.replace("</head>", CSS_BLOCK + "</head>", 1)

    return text


def main() -> None:
    path = Path(sys.argv[1])
    path.write_text(patch(path.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    print("STATIC_LU_PATCH_OK")


if __name__ == "__main__":
    main()
