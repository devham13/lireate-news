#!/usr/bin/env python3
"""
Safe, idempotent patches for template/main.php (design / SEO).

NEVER truncates the file: all edits are str.replace or bounded slice reassembly.

Historical incident 2026-11-11: hero loop used text[:pos] + block without tail — fixed.
"""
import re
import sys
from pathlib import Path

MARK_OG = "lireate_design_og_image_guard_v1"
MARK_HEAD = "lireate-cms-dark-head-v1"
MARK_BODY = "lireate_cms_dark_body_v1"
MARK_JS = "lireate-cms-dark-skip-main-screen-height"

MIN_LINES = 6000
PAGE_CONTAINER = "page_container"

CMS_DARK_PAGES_PHP = "array('home','patent','patent_prom_obr','mktu','mktu1')"


def _lines(text: str) -> int:
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def _validate(text: str, label: str) -> None:
    if _lines(text) < MIN_LINES:
        raise SystemExit(f"{label}: line count {_lines(text)} < {MIN_LINES}")
    if PAGE_CONTAINER not in text:
        raise SystemExit(f"{label}: missing {PAGE_CONTAINER}")


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"patch {label}: anchor not found")
    out = text.replace(old, new, 1)
    _validate(out, f"after {label}")
    return out


def patch(text: str, *, heroes: bool = False) -> str:
    _validate(text, "before patch")

    body_tail = (
        f" /* {MARK_BODY} */ if (in_array($temp['page'], {CMS_DARK_PAGES_PHP}, true))"
        " echo ' lireate-cms-page-dark';"
        " if ($temp['page']==='home') echo ' lireate-home-dark';?>"
    )
    if MARK_BODY not in text:
        legacy = " if($temp['page']=='home') echo ' lireate-home-dark';?>"
        if legacy in text:
            text = text.replace(legacy, " " + body_tail.strip(), 1)
        elif "lireate-cms-page-dark" not in text:
            raise SystemExit("patch body-class: anchor not found")
    _validate(text, "after body")

    if MARK_OG not in text:
        og_old = "\t <?php if($temp['news_id']!=false){"
        og_new = (
            f"\t <?php /* {MARK_OG} */ if (empty($GLOBALS['lireate_seo_og_done'])) : ?>\n"
            "\t <?php if($temp['news_id']!=false){"
        )
        text = _replace_once(text, og_old, og_new, "og-start")
        og_end_old = "<?php  }?> \n\t\n\n\t<!-- Для рекламы в tiktok 23.09.2020 -->"
        og_end_new = (
            "<?php  }?> \n"
            "\t<?php endif; ?> \n\t\n\n\t<!-- Для рекламы в tiktok 23.09.2020 -->"
        )
        text = _replace_once(text, og_end_old, og_end_new, "og-end")

    head_block = (
        f"\t<?php /* {MARK_HEAD} */ $_lx_cms_dark = {CMS_DARK_PAGES_PHP};"
        " if (in_array($temp['page'], $_lx_cms_dark, true)): ?>\n"
        '\t<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
        '\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
        '\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" />\n'
        '\t<link rel="stylesheet" href="/template/css/lireate-cms-page-dark.css?v=20261111design3" />\n'
        "\t<?php if ($temp['page'] === 'home'): ?>\n"
        '\t<link rel="stylesheet" href="/template/css/lireate-home-dark.css?v=20261111design3" />\n'
        "\t<?php endif; ?>\n"
        "\t<?php endif; ?>\n"
    )

    if "lireate-cms-page-dark.css" not in text:
        if "lireate-home-dark-head-v1" in text:
            text, n = re.subn(
                r"\t<\?php /\* lireate-home-dark-head-v1 \*/.*?\t<\?php endif; \?>\s*\n",
                head_block,
                text,
                count=1,
                flags=re.S,
            )
            if n != 1:
                raise SystemExit("patch head-cms-css: home-head replace failed")
        elif MARK_HEAD not in text:
            head_anchor = "    <?php endif; ?>\n    \n\t\n</head>"
            head_insert = "    <?php endif; ?>\n" + head_block + "    \n\t\n</head>"
            text = _replace_once(text, head_anchor, head_insert, "head-cms-css")

    js_old = "\t\t\t$(window).resize(function() {\n\t\t\t    $('.main-screen').height($(window).height());\n\t\t\t});"
    js_new = (
        f"\t\t\t/* {MARK_JS} */\n"
        "\t\t\tfunction lireateResizeMainScreen() {\n"
        "\t\t\t  if ($('body').hasClass('lireate-cms-page-dark')) return;\n"
        "\t\t\t  $('.main-screen').height($(window).height());\n"
        "\t\t\t}\n"
        "\t\t\t$(window).resize(function() { lireateResizeMainScreen(); });"
    )
    if MARK_JS not in text:
        if "lireate-home-dark-skip-main-screen-height" in text:
            text = text.replace(
                "if ($('body').hasClass('lireate-home-dark')) return;",
                "if ($('body').hasClass('lireate-cms-page-dark')) return;",
                1,
            )
        elif js_old in text:
            text = _replace_once(text, js_old, js_new, "main-screen-js")

    if heroes:
        raise SystemExit(
            "hero patches disabled by default (use lireate_design_patch_heroes.py)"
        )

    _validate(text, "after patch")
    return text


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/template/main.php [--check]", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    check_only = "--check" in sys.argv
    raw = path.read_text(encoding="utf-8", errors="replace")
    _validate(raw, "input")
    if check_only:
        print("CHECK_OK", _lines(raw))
        return
    updated = patch(raw)
    if updated == raw:
        print("UNCHANGED")
        return
    tmp = path.with_suffix(path.suffix + ".patch-tmp")
    tmp.write_text(updated, encoding="utf-8")
    _validate(tmp.read_text(encoding="utf-8", errors="replace"), "tmp file")
    tmp.replace(path)
    print("OK", _lines(updated))


if __name__ == "__main__":
    main()
