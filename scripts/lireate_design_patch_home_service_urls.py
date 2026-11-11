#!/usr/bin/env python3
"""Home: ссылки на /dogovory/ и /registraciya_programm_evm/ (modal lurl + Подробнее + hero)."""
import re
import sys
from pathlib import Path

MARK = "lireate_design_home_service_urls_v1"
MIN_LINES = 6000
PAGE_CONTAINER = "page_container"


def _lines(text: str) -> int:
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def _validate(text: str, label: str) -> None:
    if _lines(text) < MIN_LINES:
        raise SystemExit(f"{label}: line count {_lines(text)} < {MIN_LINES}")
    if PAGE_CONTAINER not in text:
        raise SystemExit(f"{label}: missing {PAGE_CONTAINER}")


def patch(text: str) -> str:
    _validate(text, "before home service urls")
    if MARK in text:
        return text

    old_lurl = (
        'var lurl = [["/reg-tz-main","/findtz","#","#","#","#"],\n'
        '\t\t\t\t\t["#","#","#","#"],\n'
        '\t\t\t\t\t["/patent_prom_obr","#","/findtz"],\n'
        '\t\t\t\t\t["#","#","#"]]; // массив ссылок'
    )
    new_lurl = (
        f'var lurl = [["/reg-tz-main","/findtz","#","#","#","#"],\n'
        f'\t\t\t\t\t["/dogovory/#licenziya","/dogovory/#franchise","/dogovory/#otchuzhdenie","/dogovory/#avtorskij-zakaz"],\n'
        f'\t\t\t\t\t["/patent_prom_obr","#","/findtz"],\n'
        f'\t\t\t\t\t["/registraciya_programm_evm/","/registraciya_programm_evm/#registraciya-bd","/registraciya_programm_evm/#zaschita-sajta"]]; /* {MARK} */'
    )
    if old_lurl in text:
        text = text.replace(old_lurl, new_lurl, 1)
    else:
        pat = re.compile(
            r"var lurl = \[\[[\s\S]*?\]\]; // массив ссылок",
            re.M,
        )
        text, n = pat.subn(new_lurl, text, count=1)
        if n != 1:
            raise SystemExit("patch home lurl: anchor not found")

    dog_old = (
        '<div class="btn content-button red js-modal-form" data-toggle="modal" data-frm="name,tel" '
        'data-mtitle="Оставьте заявку и мы свяжемся с вами в ближайшее время" data-tomail="Договоры" '
        'data-success="Мы перезвоним Вам в ближайшее время." data-btn="Отправить заявку" '
        'id="dog_but" style="margin-bottom:0px;" data-lx-home-modal-form="1">'
    )
    dog_new = (
        f'<a class="btn content-button red" href="/dogovory/" id="dog_but" '
        f'style="margin-bottom:0px;" data-lx-home-more="1">'
        f'<!-- lireate_design_home_modal_form_btns_v1 --><!-- {MARK} -->'
    )
    text = re.sub(
        r'<div class="btn content-button red js-modal-form"[^>]*id="dog_but"[^>]*>',
        dog_new,
        text,
        count=1,
    )
    text = text.replace(
        '<!-- lireate_design_home_modal_form_btns_v1 -->Подробнее</div>',
        "Подробнее</a>",
        1,
    )

    pro_pat = re.compile(
        r'<div class="btn content-button red js-modal-form"[^>]*id="pro_but"[^>]*>\s*Подробнее</div>',
        re.S,
    )
    pro_new = (
        f'<a class="btn content-button red" href="/registraciya_programm_evm/" id="pro_but" '
        f'style="margin-bottom:0px;" data-lx-home-more="1">Подробнее</a>'
    )
    text, n = pro_pat.subn(pro_new, text, count=1)
    if n != 1:
        raise SystemExit("patch home pro_but failed")

    _validate(text, "after home service urls")
    return text


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/template/main.php", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    updated = patch(raw)
    if updated == raw:
        print("UNCHANGED")
        return
    path.write_text(updated, encoding="utf-8")
    print("OK", _lines(updated))


if __name__ == "__main__":
    main()
