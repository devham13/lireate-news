#!/usr/bin/env python3
"""Targeted home (main.php) layout patches — blog teaser + dark footer. Safe replace only."""
import re
import sys
from pathlib import Path

MARK_BLOG = "lireate_design_home_blog_teaser_v1"
MARK_FOOTER = "lireate_design_home_footer_v1"
MARK_HERO = "lireate_design_home_hero_v4"
MARK_ASSETS = "lireate_design_home_hero_assets_v1"
MIN_LINES = 6000
PAGE_CONTAINER = "page_container"


def _lines(text: str) -> int:
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def _validate(text: str, label: str) -> None:
    if _lines(text) < MIN_LINES:
        raise SystemExit(f"{label}: line count {_lines(text)} < {MIN_LINES}")
    if PAGE_CONTAINER not in text:
        raise SystemExit(f"{label}: missing {PAGE_CONTAINER}")


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        if new.strip() in text or MARK_BLOG in text:
            return text
        raise SystemExit(f"patch {label}: anchor not found")
    out = text.replace(old, new, 1)
    _validate(out, f"after {label}")
    return out


def patch(text: str) -> str:
    _validate(text, "before home patch")

    if MARK_BLOG not in text:
        blog_pat = re.compile(
            r'        \t<div class="col-xs-12 col-lg-10 col-lg-offset-1">\n'
            r'(\t\t\t\t<p style="margin-bottom: 30px;">.*?</p>\n)'
            r'    \t\t</div>\n    \t\t<br />',
            re.S,
        )

        def _blog_repl(m):
            return (
                '        \t<div class="lireate-home-blog">\n'
                '        \t\t<div class="lireate-home-blog-intro">\n'
                + m.group(1)
                + '        \t\t</div>\n'
                + f'\t\t<?php /* {MARK_BLOG} */ if (is_file(dirname(__FILE__) . '
                "'/page/home/lireate-home-blog-teaser.inc.php')) { "
                "include dirname(__FILE__) . '/page/home/lireate-home-blog-teaser.inc.php'; } ?>\n"
                '        \t</div>'
            )

        text, n = blog_pat.subn(_blog_repl, text, count=1)
        if n != 1:
            raise SystemExit("patch home-blog: block not found")
        _validate(text, "after home-blog")

    foot_old = (
        "\t\t<?php\n"
        "\t\t\t\n"
        "\t\t\t    include ('./template/parts/footer.php');\n"
        "\t\t\t    \n"
        "\t\t\t?>"
    )
    foot_new = (
        "\t\t<?php\n"
        f"\t\t\t/* {MARK_FOOTER} */\n"
        "\t\t\tif ($temp['page'] === 'home') {\n"
        "\t\t\t\t$_lx_ul = dirname(__FILE__) . '/page/uslugi/lireate-uslugi-lib.php';\n"
        "\t\t\t\tif (is_file($_lx_ul)) { require_once $_lx_ul; }\n"
        "\t\t\t\tif (function_exists('lireate_uslugi_render_footer')) {\n"
        "\t\t\t\t\tlireate_uslugi_render_footer();\n"
        "\t\t\t\t} else {\n"
        "\t\t\t\t    include ('./template/parts/footer.php');\n"
        "\t\t\t\t}\n"
        "\t\t\t} else {\n"
        "\t\t\t    include ('./template/parts/footer.php');\n"
        "\t\t\t}\n"
        "\t\t\t?>"
    )
    # Repair botched nested <?php from earlier deploy
    foot_broken = "			<?php /* lireate_design_home_footer_v1 */ if ($temp['page'] === 'home') {"
    if foot_broken in text:
        text = re.sub(
            r"\t\t<\?php\s*\n\s*<\?php /\* lireate_design_home_footer_v1 \*/.*?\?\>\s*\n\s*\?\>",
            foot_new,
            text,
            count=1,
            flags=re.S,
        )
    elif MARK_FOOTER not in text:
        text = _replace_once(text, foot_old, foot_new, "home-footer")

    assets_line = '\t<link rel="stylesheet" href="/template/css/lireate-home-dark.css'
    if MARK_ASSETS not in text and assets_line in text:
        insert_after = None
        for marker in [
            '\t<link rel="stylesheet" href="/template/css/lireate-home-dark.css?v=20261111design5" />\n',
            '\t<link rel="stylesheet" href="/template/css/lireate-home-dark.css?v=20261111design3" />\n',
        ]:
            if marker in text:
                insert_after = marker
                break
        if insert_after:
            assets_block = (
                insert_after
                + f'\t<?php /* {MARK_ASSETS} */ if ($temp[\'page\'] === \'home\'): ?>\n'
                '\t<link rel="stylesheet" href="/template/css/lireate-home-hero.css?v=20261111hero1" />\n'
                '\t<script defer src="/template/js/lireate-home-hero.js?v=20261111hero1"></script>\n'
                '\t<?php endif; ?>\n'
            )
            text = text.replace(insert_after, assets_block, 1)
        _validate(text, "after home assets")

    if MARK_HERO not in text:
        hero_pat = re.compile(
            r'        \t<div class="row main-screen main_back" id="main_back" style="margin: 0;">.*?</div>\n        \t\n',
            re.S,
        )
        hero_new = (
            f'        \t<div class="row main-screen lireate-hero-v4" id="main_back" style="margin: 0;">\n'
            f'\t\t<?php /* {MARK_HERO} */ if (is_file(dirname(__FILE__) . '
            "'/page/home/lireate-home-hero.inc.php')) { "
            "include dirname(__FILE__) . '/page/home/lireate-home-hero.inc.php'; } ?>\n"
            '        \t</div>\n'
            '        \t\n'
        )
        text, n = hero_pat.subn(hero_new, text, count=1)
        if n != 1:
            raise SystemExit("patch home-hero: block not found")
        _validate(text, "after home-hero")

    _validate(text, "after home patch")
    return text


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/template/main.php", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    _validate(raw, "input")
    updated = patch(raw)
    if updated == raw:
        print("UNCHANGED")
        return
    tmp = path.with_suffix(path.suffix + ".home-patch-tmp")
    tmp.write_text(updated, encoding="utf-8")
    _validate(tmp.read_text(encoding="utf-8", errors="replace"), "tmp")
    tmp.replace(path)
    print("OK", _lines(updated))


if __name__ == "__main__":
    main()
