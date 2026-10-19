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


def split_headline(text, highlight_hint=None):
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return ["Заголовок"], ""
    words = text.split()
    highlight = (highlight_hint or "").strip()
    if not highlight and len(words) >= 2:
        highlight = words[-1] if len(words[-1]) > 3 else " ".join(words[-2:])
    # Build 2-4 lines
    if len(text) <= 36:
        lines = [text]
    elif len(text) <= 72:
        mid = len(words) // 2
        lines = [" ".join(words[:mid]), " ".join(words[mid:])]
    else:
        third = max(1, len(words) // 3)
        lines = [
            " ".join(words[:third]),
            " ".join(words[third : 2 * third]),
            " ".join(words[2 * third :]),
        ]
    lines = [truncate(l, 42) for l in lines[:4]]
    highlight = truncate(highlight, 24)
    return lines, highlight


def derive_cover_spec(meta):
    headline_src = meta.get("cover_headline") or meta.get("h1") or meta.get("title") or ""
    lines, highlight = split_headline(headline_src, meta.get("cover_highlight"))
    kw = meta.get("keywords") or []
    k0 = kw[0] if kw else meta.get("primary_query") or "тема"
    chips = [
        {"icon": "tag", "text": truncate(k0, 22)},
        {"icon": "shield", "text": truncate(meta.get("lireate_category_name") or "право", 22)},
    ]
    label_chips = []
    for i, w in enumerate(kw[1:4] if isinstance(kw, list) else []):
        variants = ["black", "white", "pink"]
        label_chips.append((truncate(w, 18), variants[i % 3]))
    sticky = meta.get("cover_sticky") or truncate(
        (meta.get("meta_ab") or {}).get("description_ctr") or "проверьте до подачи", 48
    )
    return {
        "headline_lines": lines,
        "highlight": highlight,
        "sticky_text": sticky,
        "sticky_color": meta.get("cover_sticky_color") or "yellow",
        "badge_label": category_badge(meta),
        "chips": chips,
        "label_chips": label_chips,
        "ui_card_title": meta.get("cover_ui_title") or "Настройки проверки",
        "ui_card_rows": meta.get("cover_ui_rows")
        or ["Реестр ФИПС", "МКТУ", "Сходство"],
    }
