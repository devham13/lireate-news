"""UTF-8 safe text truncation at word boundaries (Py3.6+)."""

from __future__ import annotations

import re

_WS = re.compile(r"\s+")


def truncate_utf8(text, max_len, ellipsis=""):
    """Truncate without cutting a word; optional ellipsis counts toward max_len."""
    text = (text or "").strip()
    if max_len <= 0:
        return ""
    if len(text) <= max_len:
        return text
    ell = ellipsis or ""
    budget = max_len - len(ell) if ell else max_len
    if budget < 1:
        return ell[:max_len] if ell else text[:max_len]
    chunk = text[:budget]
    last_space = chunk.rfind(" ")
    if last_space > budget // 2:
        chunk = chunk[:last_space]
    chunk = chunk.rstrip(" ,.-:;—–")
    if not chunk:
        chunk = text[:budget].rstrip(" ,.-:;—–")
    if ell and len(text) > len(chunk):
        chunk = chunk + ell
    return chunk


def normalize_seo_title(title, max_len=70):
    """Prefer full title under max_len; otherwise drop trailing words."""
    title = _WS.sub(" ", (title or "").strip())
    if len(title) <= max_len:
        return title
    return truncate_utf8(title, max_len, ellipsis="")


def normalize_seo_description(desc, max_len=200, ellipsis="…"):
    desc = _WS.sub(" ", (desc or "").strip())
    if len(desc) <= max_len:
        return desc
    return truncate_utf8(desc, max_len, ellipsis=ellipsis)