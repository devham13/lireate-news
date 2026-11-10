#!/usr/bin/env python3
"""Normalize internal href in L article.html for live 200 without redirect."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARTICLES = REPO / "memory/blog/articles"

CMS_NO_SLASH = frozenset(
    {
        "news",
        "kontaktyi",
        "docs",
        "team",
        "mktu",
        "patent",
        "patent_prom_obr",
        "reviews",
        "portfolio",
        "o_kompanii",
        "partners",
        "reg-tz-main",
    }
)

SERVICE_WITH_SLASH = frozenset(
    {
        "registraciya_tovarnogo_znaka",
        "registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat",
        "findtz",
        "prodlenie_tovarnogo_znaka",
    }
)

NEWS_NUM_REPLACEMENTS = {
    "/news?num=2&category=10": "/dogovor_na_razrabotku_logotipa_kak_poluchit_prava_ot_dizajnera/",
    "/news?num=2&category=12": "/domennoe_imya_nma_ili_net_uchet_i_zaschita_domena_po_fsbu_14_2022/",
    "/news?num=2&category=13": "/kak_zaregistrirovat_brend_na_ozon_i_wildberries_proverka_imeni_i_nuzhen_li_tz/",
    "/news?num=2&category=15": "/chek_list_markirovka_importa_chestnyiy_znak_i_tovarnyiy_znak_brenda/",
    "/news?num=2&category=17": "/chek_list_mozhno_li_publikovat_foto_kartin_i_rabot_xudozhnika_bez_narusheniya_avtorskix_prav/",
    "/news?num=2&category=19": "/registraciya_mobilnogo_prilozheniya_programma_dlya_evm_ili_tovarnyy_znak/",
    "/news?num=2&category=20": "/sposobyi_zaschityi_izobreteniya_patent_nou_xau_ili_publikaciya_sravnenie_i_chek_list/",
    "/news?num=2&category=9": "/registraciya_tovarnogo_znaka/",
}

SPECIAL = {
    "/chto_delat_esli_tovarnyy_znak_zanyat": "/chto_delat_esli_tovarnyiy_znak_zanyat/",
    "/chto_delat_esli_tovarnyy-znak-zanyat": "/chto_delat_esli_tovarnyiy_znak_zanyat/",
    "/blog/kak-opredelit-klass-mktu/": "/struktura_mktu_kak_opredelit_klass_dlya_tovara_i_uslugi/",
    "/markirovka_importa-chestnyy-znak-i-tovarnyy-znak/": "/markirovka_importa-chestnyy-znak-i-tovarnyy-znak/",
}


def normalize_path(path: str) -> str:
    if not path.startswith("/") or path.startswith("//"):
        return path
    if "?" in path:
        return NEWS_NUM_REPLACEMENTS.get(path, path)
    if path in SPECIAL:
        return SPECIAL[path]
    bare = path.rstrip("/")
    slug = bare.lstrip("/")
    if "/" in slug:
        return path
    if slug in CMS_NO_SLASH:
        return "/" + slug
    if slug in SERVICE_WITH_SLASH:
        return "/" + slug + "/"
    return "/" + slug + "/"


def main():
    changed = 0
    for html in sorted(ARTICLES.glob("L*/article.html")):
        text = html.read_text(encoding="utf-8")
        orig = text

        def repl(m):
            path = m.group(1)
            new = normalize_path(path)
            return 'href="' + new + '"'

        text = re.sub(r'href="(/[^"#]+)"', repl, text)
        if text != orig:
            html.write_text(text, encoding="utf-8")
            changed += 1
            print("updated", html.parent.name)
    print("total", changed)


if __name__ == "__main__":
    main()
