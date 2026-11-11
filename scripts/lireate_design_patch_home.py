#!/usr/bin/env python3
"""Targeted home (main.php) layout patches — blog teaser + dark footer. Safe replace only."""
import sys
from pathlib import Path

MARK_BLOG = "lireate_design_home_blog_teaser_v1"
MARK_FOOTER = "lireate_design_home_footer_v1"
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

    blog_old = (
        '\t\t<div class="col-xs-12 col-lg-10 col-lg-offset-1">\n'
        '\t\t\t\t<p style="margin-bottom: 30px;">В блоге мы публикуем полезные материалы'
    )
    blog_new = (
        '\t\t<div class="lireate-home-blog">\n'
        '\t\t\t<div class="lireate-home-blog-intro">\n'
        '\t\t\t\t<p style="margin-bottom: 30px;">В блоге мы публикуем полезные материалы'
    )
    if MARK_BLOG not in text and blog_old in text:
        text = _replace_once(text, blog_old, blog_new, "blog-wrap-start")

    blog_close_old = (
        '    		</div>\n'
        '    		<br />\n'
        '    	\t\n'
        '\t\t<?php endif?>\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t<!-- ================================================================================================-->\n'
        '\t\t\n'
        '\t\t<!-- =====================       РАЗДЕЛ САЙТА - РЕГИСТРАЦИЯ ТОВАРНОГО ЗНАКА'
    )
    blog_close_new = (
        '    		</div>\n'
        f'\t\t<?php /* {MARK_BLOG} */ if (is_file(dirname(__FILE__) . '
        "'/page/home/lireate-home-blog-teaser.inc.php')) { "
        "include dirname(__FILE__) . '/page/home/lireate-home-blog-teaser.inc.php'; } ?>\n"
        '\t\t</div>\n'
        '\t\t\n'
        '\t\t<?php endif?>\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t\n'
        '\t\t<!-- ================================================================================================-->\n'
        '\t\t\n'
        '\t\t<!-- =====================       РАЗДЕЛ САЙТА - РЕГИСТРАЦИЯ ТОВАРНОГО ЗНАКА'
    )
    if MARK_BLOG not in text and blog_close_old in text:
        text = _replace_once(text, blog_close_old, blog_close_new, "blog-teaser")

    foot_old = "\t\t    include ('./template/parts/footer.php');"
    foot_new = (
        f"\t\t<?php /* {MARK_FOOTER} */ if ($temp['page'] === 'home') {{\n"
        "\t\t\t$_lx_ul = dirname(__FILE__) . '/page/uslugi/lireate-uslugi-lib.php';\n"
        "\t\t\tif (is_file($_lx_ul)) { require_once $_lx_ul; }\n"
        "\t\t\tif (function_exists('lireate_uslugi_render_footer')) {\n"
        "\t\t\t\tlireate_uslugi_render_footer();\n"
        "\t\t\t} else {\n"
        "\t\t\t    include ('./template/parts/footer.php');\n"
        "\t\t\t}\n"
        "\t\t} else {\n"
        "\t\t    include ('./template/parts/footer.php');\n"
        "\t\t} ?>"
    )
    if MARK_FOOTER not in text:
        text = _replace_once(text, foot_old, foot_new, "home-footer")

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
