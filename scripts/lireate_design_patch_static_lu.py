#!/usr/bin/env python3
"""Расширить lireate-cms-page-dark на reviews/portfolio/spasibo/uslugi + static CSS."""
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lireate_design_main_php_sanitize import sanitize_main_php_head  # noqa: E402

MARK = "lireate_design_static_lu_v1"
MARK_PAGES = "lireate_design_cms_dark_pages_v2"
MIN_LINES = 6000

DARK_ARRAY = (
    "array('home','patent','patent_prom_obr','mktu','mktu1',"
    "'reviews','portfolio','spasibo','uslugi','avtor','team','partners','kontaktyi')"
)

STATIC_BODY = (
    f" /* {MARK} */ "
    "$_lx_static = array('reviews','portfolio','spasibo','uslugi');"
    " if (in_array($temp['page'], $_lx_static, true)) echo ' lireate-static-lu';"
    " if ($temp['page']==='reviews') echo ' lireate-reviews-body';"
    " if ($temp['page']==='portfolio') echo ' lireate-portfolio-body';"
    " if ($temp['page']==='spasibo') echo ' lireate-spasibo-body';"
    " $_lx_ru = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';"
    " if (preg_match('#^/reviews(?:[/?]|$)#', $_lx_ru)) { echo ' lireate-cms-page-dark lireate-static-lu lireate-reviews-body'; }"
    " if (preg_match('#^/portfolio(?:[/?]|$)#', $_lx_ru)) { echo ' lireate-cms-page-dark lireate-static-lu lireate-portfolio-body'; }"
    " if (preg_match('#^/spasibo(?:[/?]|$)#', $_lx_ru)) { echo ' lireate-cms-page-dark lireate-static-lu lireate-spasibo-body'; }"
)

HERO_JS = '<script defer src="/template/js/lireate-static-hero-lu.js?v=20261111static3"></script>'

CSS_BLOCK = (
    f'\t<?php /* {MARK} head */ '
    "if (in_array($temp['page'], array('reviews','portfolio','spasibo','uslugi','avtor','team','partners','kontaktyi'), true)): ?>\n"
    '\t<link rel="stylesheet" href="/template/css/lireate-lu-viewport.css?v=20261111vp6" />\n'
    '\t<link rel="stylesheet" href="/template/css/lireate-static-pages-lu.css?v=20261111static3" />\n'
    f'\t{HERO_JS}\n'
    '\t<link rel="stylesheet" href="/template/css/lireate-home-modal-lu.css?v=20261111mod2" />\n'
    '\t<script defer src="/template/js/lireate-home-modal-lu.js?v=20261111mod2"></script>\n'
    "\t<?php endif; ?>\n"
)

PARTIAL_STATIC_USLUGI = (
    f"/* {MARK} */ if($temp['page']=='uslugi') echo ' lireate-uslugi-body';"
)


def _static_body_complete(text: str) -> bool:
    return "$_lx_static" in text and "preg_match('#^/reviews" in text


def _upgrade_static_body(text: str) -> str:
    if PARTIAL_STATIC_USLUGI in text and not _static_body_complete(text):
        text = text.replace(PARTIAL_STATIC_USLUGI, STATIC_BODY.strip(), 1)
    elif MARK in text and not _static_body_complete(text):
        # legacy stub with MARK only
        stub = re.compile(
            re.escape(f"/* {MARK} */") + r"\s*if\s*\(\s*\$temp\['page'\]\s*==\s*'uslugi'\s*\).*?;",
        )
        text, n = stub.subn(STATIC_BODY.strip(), text, count=1)
        if n == 0 and "/* {MARK} */".format(MARK=MARK) in text:
            pass
    return text


STATIC_CSS_LINK = re.compile(
    r'\t<link rel="stylesheet" href="/template/css/lireate-static-pages-lu\.css\?v=20261111static[123]" />\s*\n',
    re.I,
)


def _upgrade_static_hero_js(text: str) -> str:
    if HERO_JS in text:
        return text
    if "lireate-static-pages-lu.css" not in text:
        return text

    def _after_link(m: re.Match) -> str:
        line = m.group(0)
        if 'v=20261111static3' not in line:
            line = re.sub(r"v=20261111static[12]", "v=20261111static3", line)
        return line + f"\t{HERO_JS}\n"

    text2, n = STATIC_CSS_LINK.subn(_after_link, text, count=1)
    return text2 if n else text


def patch(text: str) -> str:
    if text.count("\n") < MIN_LINES:
        raise SystemExit("main.php too short")

    text = sanitize_main_php_head(text)

    broken = "array(home'"
    if broken in text:
        text = text.replace(broken, "array('home'", 1)
    if MARK_PAGES not in text:
        text, n = re.subn(
            r"array\('home','patent','patent_prom_obr','mktu','mktu1'\)",
            f"/* {MARK_PAGES} */ {DARK_ARRAY}",
            text,
            count=1,
        )
        if n != 1 and MARK_PAGES not in text:
            raise SystemExit("cms dark pages array not found")
    body_old = (
        "if (in_array($temp['page'], array('home','patent','patent_prom_obr','mktu','mktu1'), true))"
        " echo ' lireate-cms-page-dark';"
    )
    body_new = (
        f"/* {MARK_PAGES} body */ if (in_array($temp['page'], {DARK_ARRAY}, true))"
        " echo ' lireate-cms-page-dark';"
    )
    if body_old in text:
        text = text.replace(body_old, body_new, 1)

    text = _upgrade_static_body(text)
    if not _static_body_complete(text):
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

    text = _upgrade_static_hero_js(text)
    text = sanitize_main_php_head(text)
    return text


def main() -> None:
    path = Path(sys.argv[1])
    path.write_text(patch(path.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    print("STATIC_LU_PATCH_OK")


if __name__ == "__main__":
    main()
