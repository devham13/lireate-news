#!/usr/bin/env python3
"""Targeted home (main.php) layout patches — blog teaser + dark footer. Safe replace only."""
import re
import sys
from pathlib import Path

MARK_BLOG = "lireate_design_home_blog_teaser_v1"
MARK_FOOTER = "lireate_design_home_footer_v1"
MARK_HERO = "lireate_design_home_hero_v4"
MARK_ASSETS = "lireate_design_home_hero_assets_v1"
MARK_LU = "lireate_design_home_lu_wrap_v1"
MARK_WHY = "lireate_design_home_why_grid_v1"
MARK_MODAL_BTNS = "lireate_design_home_modal_form_btns_v1"
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

    if MARK_ASSETS not in text:
        assets_pat = re.compile(
            r"(\t<link rel=\"stylesheet\" href=\"/template/css/lireate-home-dark\.css\?v=[^\"]+\" />\n)",
            re.M,
        )
        assets_block = (
            f'\\1\t<?php /* {MARK_ASSETS} */ if ($temp[\'page\'] === \'home\'): ?>\n'
            '\t<link rel="stylesheet" href="/template/page/uslugi/lireate-uslugi.css?v=20261111luhome" />\n'
            '\t<link rel="stylesheet" href="/template/page/home/lireate-home-lu.css?v=20261111luhome" />\n'
            '\t<link rel="stylesheet" href="/template/css/lireate-home-hero.css?v=20261111hero3" />\n'
            '\t<script defer src="/template/js/lireate-home-hero.js?v=20261111hero3"></script>\n'
            '\t<script>document.documentElement.classList.add("lireate-home-lu-html");if(document.body){document.body.classList.add("lireate-home-lu-body");}</script>\n'
            '\t<?php endif; ?>\n'
        )
        text, n = assets_pat.subn(assets_block, text, count=1)
        if n != 1:
            raise SystemExit("patch home-assets: anchor not found")
        _validate(text, "after home assets")
    elif "lireate-uslugi.css" not in text and MARK_ASSETS in text:
        assets_upgrade_pat = re.compile(
            r"\t<\?php /\* " + MARK_ASSETS + r" \*/ if \(\$temp\['page'\] === 'home'\): \?>.*?\t<\?php endif; \?>\n",
            re.S,
        )
        assets_block = (
            f'\t<?php /* {MARK_ASSETS} */ if ($temp[\'page\'] === \'home\'): ?>\n'
            '\t<link rel="stylesheet" href="/template/page/uslugi/lireate-uslugi.css?v=20261111luhome" />\n'
            '\t<link rel="stylesheet" href="/template/page/home/lireate-home-lu.css?v=20261111luhome" />\n'
            '\t<link rel="stylesheet" href="/template/css/lireate-home-hero.css?v=20261111hero3" />\n'
            '\t<script defer src="/template/js/lireate-home-hero.js?v=20261111hero3"></script>\n'
            '\t<script>document.documentElement.classList.add("lireate-home-lu-html");if(document.body){document.body.classList.add("lireate-home-lu-body");}</script>\n'
            '\t<?php endif; ?>\n'
        )
        text, n = assets_upgrade_pat.subn(assets_block, text, count=1)
        if n != 1:
            raise SystemExit("patch home-assets-upgrade failed")

    if MARK_LU not in text:
        lu_open = (
            '        \t<div id="lireate-home" class="lu-page lh-page">\n'
            '        \t<div class="lu-glow" aria-hidden="true"></div>\n'
            '        \t<div class="lu-wrap lh-wrap">\n'
        )
        hero_anchor = '        \t<div class="row main-screen lireate-hero-v4" id="main_back" style="margin: 0;">\n'
        if hero_anchor in text:
            text = text.replace(hero_anchor, lu_open + hero_anchor, 1)
        else:
            raise SystemExit("patch home-lu-open: hero anchor missing")
        idx = text.find("lireate_design_home_blog_teaser")
        if idx < 0:
            raise SystemExit("patch home-lu-close: blog marker missing")
        endif_pos = text.find("<?php endif?>", idx)
        if endif_pos < 0:
            raise SystemExit("patch home-lu-close: endif missing")
        text = (
            text[:endif_pos]
            + "        \t</div>\n\t\t</div><!-- /* "
            + MARK_LU
            + " */ -->\n\t\t"
            + text[endif_pos:]
        )
        _validate(text, "after home-lu")

    if MARK_WHY not in text:
        why_old = (
            '        	<div class="col-xs-12 col-lg-10 col-lg-offset-1">\n'
            '        		<div class="col-xs-12 col-lg-6 advant block-margin">'
        )
        why_new = (
            f'        	<div class="col-xs-12 col-lg-10 col-lg-offset-1 lh-why-grid lu-section"><!-- {MARK_WHY} -->\n'
            '        		<div class="col-xs-12 col-lg-6 advant block-margin">'
        )
        if why_old in text:
            text = text.replace(why_old, why_new, 1)
        _validate(text, "after home-why")

    if MARK_MODAL_BTNS not in text:
        text = text.replace(
            'id="dog_but" style="margin-bottom:0px;">Подробнее</div>',
            f'id="dog_but" style="margin-bottom:0px;" data-lx-home-modal-form="1"><!-- {MARK_MODAL_BTNS} -->Подробнее</div>',
            1,
        )
        dog_old = (
            '<div class="btn content-button red" data-toggle="modal" data-target="#main-modal" id="dog_but" style="margin-bottom:0px;" data-lx-home-modal-form="1">'
        )
        dog_new = (
            '<div class="btn content-button red js-modal-form" data-toggle="modal" data-frm="name,tel" '
            'data-mtitle="Оставьте заявку и мы свяжемся с вами в ближайшее время" data-tomail="Договоры" '
            'data-success="Мы перезвоним Вам в ближайшее время." data-btn="Отправить заявку" '
            'id="dog_but" style="margin-bottom:0px;" data-lx-home-modal-form="1">'
        )
        if dog_old.split("<!--")[0] in text or "id=\"dog_but\"" in text:
            text = re.sub(
                r'<div class="btn content-button red" data-toggle="modal" data-target="#main-modal" id="dog_but"[^>]*>',
                dog_new,
                text,
                count=1,
            )
            pro_new = (
                '<div class="btn content-button red js-modal-form" data-toggle="modal" data-frm="name,tel" '
                'data-mtitle="Оставьте заявку и мы свяжемся с вами в ближайшее время" data-tomail="Программы ЭВМ" '
                'data-success="Мы перезвоним Вам в ближайшее время." data-btn="Отправить заявку" '
                'id="pro_but" style="margin-bottom:0px;">'
            )
            text = re.sub(
                r'<div class="btn content-button red" data-toggle="modal" data-target="#main-modal" id="pro_but"[^>]*>',
                pro_new,
                text,
                count=1,
            )
        _validate(text, "after home-modal-btns")

    if "lh-product" not in text:
        text = text.replace(
            '<div class="col-xs-10 col-xs-offset-1 col-lg-8 col-lg-offset-2 product">',
            '<div class="col-xs-10 col-xs-offset-1 col-lg-8 col-lg-offset-2 product lh-product lu-section">',
            1,
        )

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
