"""SEO URL translit matching lireate.ru news (Py3.6+)."""

import re

_SEQ = (
    ("щ", "sch"),
    ("ш", "sh"),
    ("ч", "ch"),
    ("ж", "zh"),
    ("ю", "yu"),
    ("я", "ya"),
    ("ё", "e"),
    ("й", "y"),
    ("ы", "yi"),
    ("э", "e"),
    ("х", "x"),
    ("ц", "c"),
    ("а", "a"),
    ("б", "b"),
    ("в", "v"),
    ("г", "g"),
    ("д", "d"),
    ("е", "e"),
    ("з", "z"),
    ("и", "i"),
    ("к", "k"),
    ("л", "l"),
    ("м", "m"),
    ("н", "n"),
    ("о", "o"),
    ("п", "p"),
    ("р", "r"),
    ("с", "s"),
    ("т", "t"),
    ("у", "u"),
    ("ф", "f"),
    ("ъ", ""),
    ("ь", ""),
)


def _map_char(ch):
    low = ch.lower()
    for src, dst in _SEQ:
        if low == src:
            return dst
    return ch


def translit_seo_url(name):
    text = (name or "").strip()
    if not text:
        return ""
    s = "".join(_map_char(c) for c in text).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_")


def truncate_utf8(text, max_len):
    text = text or ""
    if len(text) <= max_len:
        return text
    return text[:max_len]
