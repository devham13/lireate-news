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
            "bad": {
                "header": "BAD — игнор",
                "lines": ["Нет ответа в срок", "Нет позиции по знаку", "Риск иска и блокировки"],
            },
            "good": {
                "header": "GOOD — ответ",
                "lines": ["Ответ в срок", "Доказательства и доводы", "Снижение претензий"],
            },
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
                {
                    "title": "Пошлины",
                    "subtitle": "сроки оплаты",
                    "variant": "fee",
                    "mini_rows": ["пошлина подана", "квитанция", "срок сохранён"],
                },
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
    _build_comparison_sheet(REPO_ROOT, OUT)
    print("OK", OUT)
    return 0


def _build_comparison_sheet(repo_root, out_dir):
    from PIL import Image, ImageDraw, ImageFont

    ref_dir = repo_root / "memory" / "cover" / "collage-v1" / "refs"
    pairs = [
        (ref_dir / "cover-style-ref.png", out_dir / "cover-trademark.png", "cover"),
        (ref_dir / "inline-ref-1.png", out_dir / "inline-bad-good.png", "inline bad/good"),
        (ref_dir / "inline-ref-2.png", out_dir / "inline-process.png", "inline process"),
        (ref_dir / "inline-ref-3.png", out_dir / "inline-checklist.png", "inline checklist"),
    ]
    rows = []
    label_h = 36
    for ref_path, sample_path, title in pairs:
        if not ref_path.is_file() or not sample_path.is_file():
            continue
        ref = Image.open(ref_path).convert("RGB")
        sample = Image.open(sample_path).convert("RGB")
        target_h = 380
        ref = _fit_height(ref, target_h)
        sample = _fit_height(sample, target_h)
        gap = 16
        row_w = ref.width + gap + sample.width
        row = Image.new("RGB", (row_w, target_h + label_h), "#1e293b")
        draw = ImageDraw.Draw(row)
        draw.text((8, 6), "REF: {0}".format(title), fill="#e2e8f0")
        draw.text((ref.width + gap + 8, 6), "RENDER", fill="#e2e8f0")
        row.paste(ref, (0, label_h))
        row.paste(sample, (ref.width + gap, label_h))
        rows.append(row)
    if not rows:
        _build_render_grid(out_dir)
        return
    total_h = sum(r.height for r in rows) + 12 * (len(rows) - 1)
    sheet = Image.new("RGB", (max(r.width for r in rows), total_h), "#0f172a")
    y = 0
    for row in rows:
        sheet.paste(row, (0, y))
        y += row.height + 12
    dest = out_dir / "comparison-ref-vs-render.png"
    sheet.save(dest, format="PNG", optimize=True)
    print("wrote", dest)


def _build_render_grid(out_dir):
    from PIL import Image, ImageDraw

    files = [
        ("cover-trademark", out_dir / "cover-trademark.png"),
        ("cover-patent", out_dir / "cover-patent.png"),
        ("cover-copyright", out_dir / "cover-copyright.png"),
        ("inline-bad-good", out_dir / "inline-bad-good.png"),
        ("inline-process", out_dir / "inline-process.png"),
        ("inline-checklist", out_dir / "inline-checklist.png"),
    ]
    imgs = []
    for label, path in files:
        if path.is_file():
            imgs.append((label, _fit_height(Image.open(path).convert("RGB"), 300)))
    if not imgs:
        return
    cols = 2
    rows_n = (len(imgs) + 1) // cols
    cell_w = max(i[1].width for i in imgs) + 20
    cell_h = 300 + 28
    sheet = Image.new("RGB", (cols * cell_w, rows_n * cell_h), "#0f172a")
    draw = ImageDraw.Draw(sheet)
    for idx, (label, im) in enumerate(imgs):
        c, r = idx % cols, idx // cols
        x, y = c * cell_w + 10, r * cell_h + 24
        draw.text((x, r * cell_h + 4), label, fill="#e2e8f0")
        sheet.paste(im, (x, y))
    dest = out_dir / "comparison-ref-vs-render.png"
    sheet.save(dest, format="PNG", optimize=True)
    print("wrote", dest, "(render grid; add refs under memory/cover/collage-v1/refs/)")


def _fit_height(im, h):
    from PIL import Image

    w = int(im.width * (float(h) / float(im.height)))
    return im.resize((w, h), Image.Resampling.LANCZOS)


if __name__ == "__main__":
    raise SystemExit(main())
