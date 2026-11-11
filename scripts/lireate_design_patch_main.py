#!/usr/bin/env python3
"""Idempotent patches for template/main.php (CMS dark pages + og guard + CLS)."""
import sys
from pathlib import Path

MARK_OG = "lireate_design_og_image_guard_v1"
MARK_HEAD = "lireate-cms-dark-head-v1"
MARK_BODY = "lireate_cms_dark_body_v1"
MARK_HERO_HOME = 'class="row main-screen main_back" id="main_back"'
MARK_JS = "lireate-cms-dark-skip-main-screen-height"

CMS_DARK_PAGES_PHP = (
    "array('home','patent','patent_prom_obr','mktu','mktu1')"
)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text and new in text:
        return text
    if old not in text:
        raise SystemExit(f"patch {label}: anchor not found")
    if new in text:
        return text
    return text.replace(old, new, 1)


def _hero_patch(block: str, marker: str) -> str:
    hero_old = '\t\t\t<div class="row main-screen" style="margin: 0;">'
    hero_new = f'\t\t\t<div {MARK_HERO_HOME} style="margin: 0;" data-lx-hero="{marker}">'
    if marker in block or 'main-screen main_back"' in block:
        return block
    if hero_old not in block:
        hero_old2 = '        \t<div class="row main-screen" style="margin: 0;">'
        hero_new2 = f'        \t<div {MARK_HERO_HOME} style="margin: 0;" data-lx-hero="{marker}">'
        if hero_old2 in block:
            return block.replace(hero_old2, hero_new2, 1)
        return block
    return block.replace(hero_old, hero_new, 1)


def patch(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")

    body_tail = (
        f" /* {MARK_BODY} */ if (in_array($temp['page'], {CMS_DARK_PAGES_PHP}, true))"
        " echo ' lireate-cms-page-dark';"
        " if ($temp['page']==='home') echo ' lireate-home-dark';?>"
    )
    body_legacy = " if($temp['page']=='home') echo ' lireate-home-dark';?>"
    if MARK_BODY not in text:
        if body_legacy in text:
            text = text.replace(body_legacy, " " + body_tail.strip(), 1)
        elif "lireate-cms-page-dark" not in text:
            raise SystemExit("patch body-class: anchor not found")

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
        import re

        if "lireate-home-dark-head-v1" in text:
            text = re.sub(
                r"\t<\?php /\* lireate-home-dark-head-v1 \*/.*?\t<\?php endif; \?>\s*\n",
                head_block,
                text,
                count=1,
                flags=re.S,
            )
        elif MARK_HEAD not in text:
            head_anchor = "    <?php endif; ?>\n    \n\t\n</head>"
            head_insert = "    <?php endif; ?>\n" + head_block + "    \n\t\n</head>"
            text = _replace_once(text, head_anchor, head_insert, "head-cms-css")

    markers = [
        ("home", "\t\t<?php if($temp['page']=='home'):?>"),
        ("patent", "\t\t<?php if($temp['page']=='patent'):?>"),
        ("patent_prom_obr", "\t\t<?php if($temp['page']=='patent_prom_obr'):?>"),
    ]
    for name, anchor in markers:
        pos = text.find(anchor)
        if pos == -1:
            continue
        next_else = text.find("<?php if($temp['page']", pos + len(anchor))
        if next_else == -1:
            next_else = len(text)
        before, block_rest = text[:pos], text[pos:next_else]
        block_rest = _hero_patch(block_rest, name)
        text = before + block_rest

    if MARK_JS not in text:
        js_old = "\t\t\t$(window).resize(function() {\n\t\t\t    $('.main-screen').height($(window).height());\n\t\t\t});"
        js_new = (
            f"\t\t\t/* {MARK_JS} */\n"
            "\t\t\tfunction lireateResizeMainScreen() {\n"
            "\t\t\t  if ($('body').hasClass('lireate-cms-page-dark')) return;\n"
            "\t\t\t  $('.main-screen').height($(window).height());\n"
            "\t\t\t}\n"
            "\t\t\t$(window).resize(function() { lireateResizeMainScreen(); });"
        )
        if "lireate-home-dark-skip-main-screen-height" in text:
            text = text.replace(
                "if ($('body').hasClass('lireate-home-dark')) return;",
                "if ($('body').hasClass('lireate-cms-page-dark')) return;",
            )
        else:
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
