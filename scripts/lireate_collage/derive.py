import re

from .validate import truncate


def category_badge(meta):
    name = (meta.get("lireate_category_name") or "").lower()
    if "патент" in name:
        return "ПАТЕНТ"
    if "автор" in name or "копирайт" in name:
        return "©"
    if "товар" in name or "бренд" in name or "знак" in name:
        return "ТЗ"
    return "ИС"


def _topic_kind(meta):
    badge = category_badge(meta)
    if badge == "ПАТЕНТ":
        return "patent"
    if badge == "©":
        return "copyright"
    return "trademark"


def split_headline(text, highlight_hint=None):
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return ["Заголовок статьи"], ""
    words = text.split()
    highlight = (highlight_hint or "").strip()
    if not highlight and len(words) >= 2:
        highlight = words[-1] if len(words[-1]) > 4 else " ".join(words[-2:])
    # Prefer 3–4 lines for cover density
    n = len(words)
    if n <= 4:
        lines = [" ".join(words)]
    elif n <= 8:
        mid = n // 2
        lines = [" ".join(words[:mid]), " ".join(words[mid:])]
    elif n <= 12:
        a, b = n // 3, (2 * n) // 3
        lines = [" ".join(words[:a]), " ".join(words[a:b]), " ".join(words[b:])]
    else:
        q = n // 4
        lines = [
            " ".join(words[:q]),
            " ".join(words[q : 2 * q]),
            " ".join(words[2 * q : 3 * q]),
            " ".join(words[3 * q :]),
        ]
    lines = [truncate(l, 36) for l in lines[:4]]
    highlight = truncate(highlight, 22)
    return lines, highlight


def _sticky_pack(text, underline_word=None):
    text = truncate(text, 42)
    words = text.split()
    if len(words) > 6:
        text = " ".join(words[:6])
    if not underline_word:
        underline_word = words[-1] if words else ""
    return text, underline_word


def _topic_copy(kind, meta, kw):
    if kind == "trademark":
        sticky, ul = _sticky_pack("чужой знак — отказ", "отказ")
        chips = [
            ("тождество", "black"),
            ("сходство", "white"),
            ("класс МКТУ", "pink"),
        ]
        if kw:
            chips[0] = (truncate(kw[0], 16), "black")
        ui_title = "Проверка обозначения"
        ui_rows = ["Реестр ФИПС", "Классы МКТУ", "Оценка риска"]
    elif kind == "patent":
        sticky, ul = _sticky_pack("новизна не ждёт", "новизна")
        chips = [
            ("формула", "black"),
            ("экспертиза", "white"),
            ("пошлины", "pink"),
        ]
        ui_title = "Патентная заявка"
        ui_rows = ["Описание и чертежи", "Формула изобретения", "Сроки приоритета"]
    else:
        sticky, ul = _sticky_pack("договор важнее скрина", "договор")
        chips = [
            ("автор", "black"),
            ("лицензия", "white"),
            ("объект", "pink"),
        ]
        ui_title = "Права на контент"
        ui_rows = ["Договор с автором", "Вид лицензии", "Депонирование"]

    return sticky, ul, chips, ui_title, ui_rows


def derive_cover_spec(meta):
    kind = _topic_kind(meta)
    headline_src = meta.get("cover_headline") or meta.get("h1") or meta.get("title") or ""
    lines, highlight = split_headline(headline_src, meta.get("cover_highlight"))
    kw = meta.get("keywords") or []
    if isinstance(kw, str):
        kw = [kw]

    sticky, ul, label_chips, ui_title, ui_rows = _topic_copy(kind, meta, kw)

    if meta.get("cover_sticky"):
        sticky, ul = _sticky_pack(meta["cover_sticky"], meta.get("cover_sticky_underline"))
    if meta.get("cover_label_chips"):
        label_chips = meta["cover_label_chips"]
    elif kw and len(kw) >= 3:
        variants = ["black", "white", "pink"]
        label_chips = [(truncate(kw[i], 16), variants[i]) for i in range(min(3, len(kw)))]

    if meta.get("cover_ui_title"):
        ui_title = meta["cover_ui_title"]
    if meta.get("cover_ui_rows"):
        ui_rows = meta["cover_ui_rows"]

    return {
        "headline_lines": lines,
        "highlight": highlight,
        "sticky_text": sticky,
        "sticky_underline": ul,
        "sticky_color": meta.get("cover_sticky_color") or "yellow",
        "badge_label": category_badge(meta),
        "label_chips": label_chips,
        "ui_card_title": ui_title,
        "ui_card_rows": ui_rows[:4],
    }
