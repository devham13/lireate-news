#!/usr/bin/env python3
"""Idempotent patches for template/main.php (home dark + og:image guard + CLS)."""
import sys
from pathlib import Path

MARK_BODY = "lireate-home-dark"
MARK_OG = "lireate_design_og_image_guard_v1"
MARK_HEAD = "lireate-home-dark-head-v1"
MARK_HERO = 'class="row main-screen main_back" id="main_back"'
MARK_JS = "lireate-home-dark-skip-main-screen-height"


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"patch {label}: anchor not found")
    return text.replace(old, new, 1)


def patch(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")

    body_needle = "if($temp['page']=='uslugi') echo ' lireate-uslugi-body';?>"
    body_patch = (
        "if($temp['page']=='uslugi') echo ' lireate-uslugi-body';"
        " if($temp['page']=='home') echo ' lireate-home-dark';?>"
    )
    text = _replace_once(text, body_needle, body_patch, "body-class")

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

    if MARK_HEAD not in text:
        head_anchor = "    <?php endif; ?>\n    \n\t\n</head>"
        head_insert = (
            "    <?php endif; ?>\n"
            f"\t<?php /* {MARK_HEAD} */ if ($temp['page'] === 'home'): ?>\n"
            '\t<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
            '\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
            '\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" />\n'
            '\t<link rel="stylesheet" href="/template/css/lireate-home-dark.css?v=20261111design" />\n'
            "\t<?php endif; ?>\n"
            "    \n\t\n</head>"
        )
        text = _replace_once(text, head_anchor, head_insert, "head-home-css")

    hero_old = '        \t<div class="row main-screen" style="margin: 0;">'
    hero_new = f'        \t<div {MARK_HERO} style="margin: 0;">'
    # Only first home hero: split at home block
    home_pos = text.find("\t\t<?php if($temp['page']=='home'):?>")
    if home_pos == -1:
        raise SystemExit("home block not found")
    before, after = text[:home_pos], text[home_pos:]
    if 'main-screen main_back"' not in after:
        if hero_old not in after:
            raise SystemExit("home hero div not found")
        after = after.replace(hero_old, hero_new, 1)
        text = before + after

    if MARK_JS not in text:
        js_old = "\t\t\t$(window).resize(function() {\n\t\t\t    $('.main-screen').height($(window).height());\n\t\t\t});"
        js_new = (
            f"\t\t\t/* {MARK_JS} */\n"
            "\t\t\tfunction lireateResizeMainScreen() {\n"
            "\t\t\t  if ($('body').hasClass('lireate-home-dark')) return;\n"
            "\t\t\t  $('.main-screen').height($(window).height());\n"
            "\t\t\t}\n"
            "\t\t\t$(window).resize(function() { lireateResizeMainScreen(); });"
        )
        text = _replace_once(text, js_old, js_new, "main-screen-js")

    path.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/template/main.php", file=sys.stderr)
        raise SystemExit(2)
    patch(Path(sys.argv[1]))
    print("OK")


if __name__ == "__main__":
    main()
