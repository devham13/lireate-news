#!/usr/bin/env python3
"""Render sample collage covers and inline templates to artifacts/."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_collage.constants import SLOT_FILES  # noqa: E402
from lireate_collage.derive import derive_cover_spec  # noqa: E402

ARTIFACTS = Path("/opt/cursor/artifacts")
if not ARTIFACTS.is_dir():
    ARTIFACTS = REPO_ROOT / "artifacts"
OUT = ARTIFACTS / "collage-v1-samples"
OUT.mkdir(parents=True, exist_ok=True)

COVER_METAS = [
    {
        "name": "trademark",
        "meta": {
            "topic_id": "SAMPLE-TM",
            "cover_style": "collage-v1",
            "lireate_category_name": "Товарный знак",
            "cover_headline": "Проверка товарного знака до подачи в Роспатент",
            "cover_highlight": "Роспатент",
            "keywords": ["товарный знак", "ФИПС", "сходство"],
        },
    },
    {
        "name": "patent",
        "meta": {
            "topic_id": "SAMPLE-PAT",
            "cover_style": "collage-v1",
            "lireate_category_name": "Патент",
            "cover_headline": "Патент или ноу-хау что выбрать для технологии",
            "cover_highlight": "ноу-хау",
            "keywords": ["патент", "новизна", "формула"],
        },
    },
    {
        "name": "copyright",
        "meta": {
            "topic_id": "SAMPLE-CR",
            "cover_style": "collage-v1",
            "lireate_category_name": "Авторское право",
            "cover_headline": "Авторские права на контент сайта и договор",
            "cover_highlight": "договор",
            "keywords": ["автор", "лицензия", "исключительные права"],
        },
    },
]

INLINE_SAMPLES = [
    {
        "name": "inline-bad-good",
        "item": {
            "slot": "inline_1",
            "template": "bad_good",
            "headline": "Ответ на претензию по товарному знаку: срок и доказательства",
            "chips": [
                {"icon": "tag", "text": "претензия"},
                {"icon": "calendar", "text": "30 дней"},
                {"icon": "clock", "text": "срок"},
            ],
            "sticky": {"text": "молчание дороже", "underline": "дороже", "color": "pink"},
            "bad": {"header": "BAD — игнор", "lines": ["Нет ответа в срок", "Нет позиции по знаку"]},
            "good": {"header": "GOOD — ответ", "lines": ["Ответ в срок", "Доказательства и доводы"]},
            "side_checklist": ["срок соблюдён", "позиция ясна", "риск снижен"],
            "conclusion": {
                "box_lines": ["ответ", "в срок"],
                "highlight_word": "в срок",
                "chip": "меньше риска иска",
            },
            "alt": "Сравнение ответа на претензию по товарному знаку",
        },
    },
    {
        "name": "inline-process",
        "item": {
            "slot": "inline_2",
            "template": "process",
            "headline": "Подача патентной заявки: от поиска до пошлин",
            "chips": [{"icon": "layers", "text": "этапы"}, {"icon": "warning", "text": "новизна"}],
            "sticky": {"text": "приоритет решает", "underline": "приоритет", "color": "pink"},
            "steps": [
                {"title": "Поиск", "subtitle": "ФИПС, публикации", "chip": "база", "variant": "icon"},
                {"title": "Заявка", "subtitle": "описание и формула", "chip": "суть", "variant": "toggles"},
                {"title": "Пошлины", "subtitle": "сроки оплаты", "variant": "lines"},
            ],
            "conclusion": {
                "box_lines": ["срок", "новизны"],
                "highlight_word": "новизны",
                "marker_underline": True,
                "chip": "без потери приоритета",
            },
            "alt": "Этапы подачи патентной заявки",
        },
    },
    {
        "name": "inline-checklist",
        "item": {
            "slot": "inline_3",
            "template": "checklist",
            "headline": "Публикация контента: проверка авторских прав",
            "chips": [{"icon": "globe", "text": "сайт"}, {"icon": "calendar", "text": "релиз"}],
            "sticky": {"text": "без договора — риск", "underline": "риск", "color": "pink"},
            "checklist_title": "Чеклист прав на материалы",
            "checklist_rows": [
                {"text": "договор с автором?", "icon": "person"},
                {"text": "лицензия на веб?", "icon": "doc"},
                {"text": "указан правообладатель?", "icon": "tag"},
                {"text": "срок действия?", "icon": "clock"},
                {"text": "архив исходников?", "icon": "shield"},
            ],
            "conclusion": {
                "box_lines": ["не", "СКРИН"],
                "highlight_word": "СКРИН",
                "marker_underline": True,
                "chip": "нужен договор и лицензия",
            },
            "alt": "Чеклист авторских прав перед публикацией",
        },
    },
]


def main():
    py = sys.executable
    scripts = REPO_ROOT / "scripts"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for sample in COVER_METAS:
            spec = derive_cover_spec(sample["meta"])
            spec_path = tmp / "spec-{0}.json".format(sample["name"])
            spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
            (tmp / "article.meta.json").write_text(
                json.dumps(sample["meta"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            out_dir = tmp / "out-{0}".format(sample["name"])
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
            dest = OUT / "cover-{0}.png".format(sample["name"])
            shutil.copy2(out_dir / "cover.png", dest)
            print("wrote", dest)

        for sample in INLINE_SAMPLES:
            spec_doc = {"version": 1, "style": "collage-v1", "illustrations": [sample["item"]]}
            (tmp / "cover" / "inline-specs.json").parent.mkdir(parents=True, exist_ok=True)
            (tmp / "cover" / "inline-specs.json").write_text(
                json.dumps(spec_doc, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            outd = tmp / "inline-{0}".format(sample["name"])
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
            dest = OUT / "{0}.png".format(sample["name"])
            shutil.copy2(outd / SLOT_FILES[slot], dest)
            print("wrote", dest)

    manifest = {
        "covers": [str(OUT / "cover-{0}.png".format(m["name"])) for m in COVER_METAS],
        "inlines": [str(OUT / "{0}.png".format(s["name"])) for s in INLINE_SAMPLES],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("OK", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
