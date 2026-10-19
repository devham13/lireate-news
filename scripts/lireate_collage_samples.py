#!/usr/bin/env python3
"""Render sample collage covers and inline templates to artifacts/."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = Path("/opt/cursor/artifacts")
if not ARTIFACTS.is_dir():
    ARTIFACTS = REPO_ROOT / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

COVER_SAMPLES = [
    {
        "name": "trademark",
        "spec": {
            "headline_lines": ["Проверка знака", "до подачи —", "риск не бесплатен"],
            "highlight": "не бесплатен",
            "sticky_text": "пост без метки — риск",
            "sticky_color": "yellow",
            "badge_label": "ТЗ",
            "chips": [{"icon": "tag", "text": "товарный знак"}, {"icon": "shield", "text": "Роспатент"}],
            "label_chips": [("публикация", "black"), ("прозрачность", "white"), ("ответственность", "pink")],
            "ui_card_title": "Настройки проверки",
            "ui_card_rows": ["Реестр ФИПС", "МКТУ", "Сходство"],
        },
    },
    {
        "name": "patent",
        "spec": {
            "headline_lines": ["Патент или", "секрет?", "Сравните до подачи"],
            "highlight": "секрет",
            "sticky_text": "новизна уходит быстро",
            "badge_label": "ПАТЕНТ",
            "label_chips": [("формула", "black"), ("ноу-хау", "white"), ("пошлины", "pink")],
        },
    },
    {
        "name": "copyright",
        "spec": {
            "headline_lines": ["Авторские права", "на контент:", "фиксируйте доказательства"],
            "highlight": "доказательства",
            "sticky_text": "скрин — не договор",
            "badge_label": "©",
            "label_chips": [("лицензия", "black"), ("договор", "white")],
        },
    },
]

INLINE_SAMPLES = [
    {
        "name": "inline-bad-good",
        "item": {
            "slot": "inline_1",
            "template": "bad_good",
            "headline": "Ответ на претензию по знаку: сроки и доказательства",
            "chips": [
                {"icon": "tag", "text": "товарный знак"},
                {"icon": "calendar", "text": "30 дней"},
                {"icon": "clock", "text": "без отсрочки"},
            ],
            "sticky": {"text": "правило сейчас, не потом", "color": "pink"},
            "bad": {"header": "BAD — молчание", "lines": ["Игнор письма правообладателя", "P.S. ответ потом"]},
            "good": {"header": "GOOD — ответ в срок", "lines": ["Привет! Ответ в установленный срок.", "Доказательства и позиция"]},
            "side_checklist": ["прозрачно сразу", "понятно аудитории", "соответствует правилу"],
            "conclusion": {
                "box_lines": ["ответ", "вовремя"],
                "highlight_word": "вовремя",
                "chip": "снижение риска иска",
            },
            "alt": "Сравнение правильного и неправильного ответа на претензию по товарному знаку",
        },
    },
    {
        "name": "inline-process",
        "item": {
            "slot": "inline_2",
            "template": "process",
            "headline": "Регистрация патента: три слоя защиты решения",
            "chips": [{"icon": "layers", "text": "три слоя"}, {"icon": "warning", "text": "новизна"}],
            "sticky": {"text": "сначала заявка — потом публикация", "color": "pink"},
            "steps": [
                {"title": "Поиск", "subtitle": "ФИПС и открытые базы", "chip": "первый слой", "variant": "icon"},
                {"title": "Заявка", "subtitle": "формула и описание", "chip": "второй слой", "variant": "toggles"},
                {"title": "Пошлины", "subtitle": "сроки Роспатента", "variant": "lines"},
            ],
            "conclusion": {
                "box_lines": ["оба", "слоя"],
                "highlight_word": "слоя",
                "marker_underline": True,
                "chip": "прозрачность по всей цепочке",
            },
            "alt": "Трёхшаговый процесс подготовки патентной заявки",
        },
    },
    {
        "name": "inline-checklist",
        "item": {
            "slot": "inline_3",
            "template": "checklist",
            "headline": "Авторский договор: чеклист до публикации контента",
            "chips": [
                {"icon": "globe", "text": "онлайн"},
                {"icon": "calendar", "text": "до релиза"},
            ],
            "sticky": {"text": "быстро сегодня — спор завтра", "color": "pink"},
            "checklist_title": "Чеклист перед публикацией",
            "checklist_rows": [
                {"text": "есть договор с автором?", "icon": "person"},
                {"text": "лицензия на переработку?", "icon": "doc"},
                {"text": "указан правообладатель?", "icon": "tag"},
                {"text": "срок и территория?", "icon": "globe"},
                {"text": "архив исходников?", "icon": "shield"},
            ],
            "conclusion": {
                "box_lines": ["не", "ЭКОНОМИЯ"],
                "highlight_word": "ЭКОНОМИЯ",
                "marker_underline": True,
                "chip": "иски, блоки, потеря доверия",
            },
            "alt": "Чеклист проверки авторских прав перед публикацией",
        },
    },
]


def main():
    py = sys.executable
    scripts = REPO_ROOT / "scripts"
    out_covers = ARTIFACTS / "collage-v1-samples" / "covers"
    out_inlines = ARTIFACTS / "collage-v1-samples" / "inlines"
    out_covers.mkdir(parents=True, exist_ok=True)
    out_inlines.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "article.meta.json").write_text('{"topic_id":"SAMPLE","cover_style":"collage-v1"}\n', encoding="utf-8")
        for sample in COVER_SAMPLES:
            spec_path = tmp / "cover-spec-{0}.json".format(sample["name"])
            spec_path.write_text(json.dumps(sample["spec"], ensure_ascii=False, indent=2), encoding="utf-8")
            import shutil

            out = out_covers / "{0}.png".format(sample["name"])
            out_dir = out_covers / "{0}_dir".format(sample["name"])
            subprocess.check_call(
                [
                    py,
                    str(scripts / "lireate_cover_collage.py"),
                    "--article-dir",
                    str(tmp),
                    "--spec-json",
                    str(spec_path),
                    "--force",
                    "--out-dir",
                    str(out_dir),
                ]
            )
            src = out_dir / "cover.png"
            shutil.copy2(src, out)
            print("wrote", out)

        for sample in INLINE_SAMPLES:
            spec_doc = {"version": 1, "style": "collage-v1", "illustrations": [sample["item"]]}
            (tmp / "cover" / "inline-specs.json").parent.mkdir(parents=True, exist_ok=True)
            (tmp / "cover" / "inline-specs.json").write_text(
                json.dumps(spec_doc, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            outd = out_inlines / "{0}_dir".format(sample["name"])
            subprocess.check_call(
                [
                    py,
                    str(scripts / "lireate_inline_collage.py"),
                    "--article-dir",
                    str(tmp),
                    "--force",
                    "--out-dir",
                    str(outd),
                ]
            )
            slot = sample["item"]["slot"]
            from lireate_collage.constants import SLOT_FILES

            shutil.copy2(outd / SLOT_FILES[slot], out_inlines / "{0}.png".format(sample["name"]))
            print("wrote", out_inlines / "{0}.png".format(sample["name"]))

    manifest = {
        "covers": [str(out_covers / "{0}.png".format(s["name"])) for s in COVER_SAMPLES],
        "inlines": [str(out_inlines / "{0}.png".format(s["name"])) for s in INLINE_SAMPLES],
    }
    (ARTIFACTS / "collage-v1-samples" / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print("OK samples", ARTIFACTS / "collage-v1-samples")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    raise SystemExit(main())
