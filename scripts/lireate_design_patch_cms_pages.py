#!/usr/bin/env python3
"""CMS patent / patent_prom_obr hero v4, mktu dark body+assets, shared footer."""
import re
import sys
from pathlib import Path

MIN_LINES = 6000
PAGE_CONTAINER = "page_container"
MARK_PATENT_HERO = "lireate_design_patent_hero_v4"
MARK_PROM_HERO = "lireate_design_patent_prom_hero_v4"
MARK_MKTU_BODY = "lireate_design_mktu_lu_body_v1"
MARK_MKTU_HEAD = "lireate_design_mktu_lu_head_v1"
MARK_CMS_FOOTER = "lireate_design_cms_lu_footer_v1"
MARK_CMS_HERO_ASSETS = "lireate_design_cms_hero_assets_v1"


def _lines(text: str) -> int:
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def _validate(text: str, label: str) -> None:
    if _lines(text) < MIN_LINES:
        raise SystemExit(f"{label}: line count {_lines(text)} < {MIN_LINES}")
    if PAGE_CONTAINER not in text:
        raise SystemExit(f"{label}: missing {PAGE_CONTAINER}")


def patch(text: str) -> str:
    _validate(text, "before cms patch")

    def _swap_hero(block: str, marker: str, include_name: str, h1_fragment: str) -> str:
        if marker in block:
            return block
        pat = re.compile(
            r'<div class="row main-screen main_back" id="main_back" style="margin: 0;">\s*'
            r"(?:<br\s*/?>\s*){2,4}\s*"
            r'<div class="main-title">.*?'
            + re.escape(h1_fragment)
            + r".*?</div>\s*"
            r"(?:<br\s*/?>\s*){0,3}\s*"
            r"</div>",
            re.S,
        )
        repl = (
            f'<div class="row main-screen main_back lireate-hero-v4 lireate-cms-hero" id="main_back" '
            f'style="margin: 0;"><!-- {marker} -->\n'
            f"\t\t<?php include dirname(__FILE__) . '/page/cms/{include_name}'; ?>\n"
            "\t        </div>"
        )
        new_block, n = pat.subn(repl, block, count=1)
        return new_block if n else block

    anchor_patent = "\t\t<?php if($temp['page']=='patent'):?>"
    pos_p = text.find(anchor_patent)
    if pos_p != -1:
        end_p = text.find("\t\t<?php if($temp['page']=='patent_prom_obr'):?>", pos_p)
        if end_p != -1:
            seg = text[pos_p:end_p]
            seg2 = _swap_hero(
                seg,
                MARK_PATENT_HERO,
                "lireate-cms-hero-patent.inc.php",
                "Запатентуем Ваше изобретение",
            )
            if seg2 != seg:
                text = text[:pos_p] + seg2 + text[end_p:]

    anchor_prom = "\t\t<?php if($temp['page']=='patent_prom_obr'):?>"
    pos_r = text.find(anchor_prom)
    if pos_r != -1:
        end_r = text.find("\t\t<?php if($temp['page']", pos_r + len(anchor_prom))
        if end_r != -1:
            seg = text[pos_r:end_r]
            seg2 = _swap_hero(
                seg,
                MARK_PROM_HERO,
                "lireate-cms-hero-patent-prom.inc.php",
                "Патентуем дизайн и внешний вид",
            )
            if seg2 != seg:
                text = text[:pos_r] + seg2 + text[end_r:]

    mktu_body_snip = (
        f" /* {MARK_MKTU_BODY} */ "
        "$_lx_mktu_uri = (isset($_SERVER['REQUEST_URI']) && preg_match('#^/mktu(?:[/?]|$)#', $_SERVER['REQUEST_URI'])); "
        "if ($_lx_mktu_uri) echo ' lireate-cms-page-dark lireate-mktu-lu-body';"
    )
    if MARK_MKTU_BODY not in text and "lireate_cms_dark_body_v1" in text:
        text = text.replace(
            "if ($temp['page']==='home') echo ' lireate-home-dark';?>",
            mktu_body_snip + " if ($temp['page']==='home') echo ' lireate-home-dark';?>",
            1,
        )

    mktu_head = (
        f"\t<?php /* {MARK_MKTU_HEAD} */ $_lx_mktu_uri = (isset($_SERVER['REQUEST_URI']) && preg_match('#^/mktu(?:[/?]|$)#', $_SERVER['REQUEST_URI'])); if ($_lx_mktu_uri): ?>\n"
        '\t<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
        '\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
        '\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" />\n'
        '\t<link rel="stylesheet" href="/template/css/lireate-cms-page-dark.css?v=20261111design4" />\n'
        '\t<link rel="stylesheet" href="/template/css/lireate-cms-lu.css?v=20261111lu3" />\n'
        '\t<link rel="stylesheet" href="/template/css/lireate-mktu-lu.css?v=20261111mktu1" />\n'
        "\t<?php endif; ?>\n"
    )
    if MARK_MKTU_HEAD not in text:
        head_anchor = "\t<?php /* lireate-cms-dark-head-v1 */"
        if head_anchor in text:
            text = text.replace(head_anchor, mktu_head + head_anchor, 1)

    hero_assets = (
        f"\t<?php /* {MARK_CMS_HERO_ASSETS} */ if (in_array($temp['page'], array('patent','patent_prom_obr'), true)): ?>\n"
        '\t<link rel="stylesheet" href="/template/css/lireate-home-hero.css?v=20261111hero4" />\n'
        '\t<script defer src="/template/js/lireate-home-hero.js?v=20261111hero4"></script>\n'
        "\t<?php endif; ?>\n"
    )
    if MARK_CMS_HERO_ASSETS not in text and MARK_MKTU_HEAD in text:
        text = text.replace(mktu_head, mktu_head + hero_assets, 1)
    elif MARK_CMS_HERO_ASSETS not in text and "lireate_design_cms_lu_assets_v1" in text:
        cms_lu = "\t<?php /* lireate_design_cms_lu_assets_v1 */"
        text = text.replace(cms_lu, hero_assets + cms_lu, 1)

    foot_if_old = "if ($temp['page'] === 'home') {"
    foot_if_new = (
        f"/* {MARK_CMS_FOOTER} */ if ($temp['page'] === 'home' || in_array($temp['page'], array('patent','patent_prom_obr'), true) "
        "|| (isset($_SERVER['REQUEST_URI']) && preg_match('#^/mktu(?:[/?]|$)#', $_SERVER['REQUEST_URI']))) {"
    )
    if MARK_CMS_FOOTER not in text and foot_if_old in text and "lireate_design_home_footer_v1" in text:
        text = text.replace(foot_if_old, foot_if_new, 1)

    _validate(text, "after cms patch")
    return text


def main() -> None:
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    updated = patch(raw)
    if updated == raw:
        print("UNCHANGED")
        return
    tmp = path.with_suffix(path.suffix + ".cms-patch-tmp")
    tmp.write_text(updated, encoding="utf-8")
    _validate(tmp.read_text(encoding="utf-8", errors="replace"), "tmp")
    tmp.replace(path)
    print("OK", _lines(updated))


if __name__ == "__main__":
    main()
