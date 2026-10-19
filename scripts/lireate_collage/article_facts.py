"""Strip unverified numbers from inline specs (must appear in article.html)."""

import copy
import json
import re
from html import unescape

_DIGIT_RE = re.compile(r"\d+")
_TAG_RE = re.compile(r"<[^>]+>")
_SCRUB_SKIP_KEYS = frozenset(
    {"slot", "template", "variant", "icon", "color", "alt", "underline", "highlight_word"}
)


def article_plain_text(html):
    text = _TAG_RE.sub(" ", html or "")
    return unescape(re.sub(r"\s+", " ", text)).strip()


def digit_sequences(text):
    return _DIGIT_RE.findall(text or "")


def string_digits_verified(value, article_text):
    seqs = digit_sequences(value)
    if not seqs:
        return True
    return all(seq in article_text for seq in seqs)


def scrub_string(value, article_text):
    if not isinstance(value, str):
        return value
    if string_digits_verified(value, article_text):
        return value
    return ""


def _scrub_obj(obj, article_text, parent_key=None):
    if isinstance(obj, dict):
        out = {}
        for key, val in obj.items():
            if key in _SCRUB_SKIP_KEYS:
                out[key] = val
                continue
            cleaned = _scrub_obj(val, article_text, parent_key=key)
            if cleaned == "" and isinstance(val, str):
                continue
            if cleaned is None:
                continue
            out[key] = cleaned
        return out
    if isinstance(obj, list):
        out = []
        for item in obj:
            cleaned = _scrub_obj(item, article_text, parent_key=parent_key)
            if cleaned == "" and isinstance(item, str):
                continue
            if cleaned is None:
                continue
            if isinstance(cleaned, dict) and not cleaned:
                continue
            out.append(cleaned)
        return out
    if isinstance(obj, str):
        if parent_key in _SCRUB_SKIP_KEYS:
            return obj
        return scrub_string(obj, article_text)
    return obj


def scrub_inline_item(item, article_text):
    """Return a copy with strings containing unverified digit sequences removed."""
    if not article_text:
        return copy.deepcopy(item)
    return _scrub_obj(copy.deepcopy(item), article_text, parent_key=None)


def scrub_inline_doc(doc, article_text):
    out = copy.deepcopy(doc)
    ill = []
    for item in out.get("illustrations") or []:
        ill.append(scrub_inline_item(item, article_text))
    out["illustrations"] = ill
    return out


def collect_unverified_digit_strings(item, article_text):
    """For tests: list string values in spec that contain digits not in article."""
    bad = []
    blob = json.dumps(item, ensure_ascii=False)

    def walk(obj, parent_key=None):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, parent_key=k)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, parent_key=parent_key)
        elif isinstance(obj, str) and digit_sequences(obj):
            if parent_key in _SCRUB_SKIP_KEYS:
                return
            if not string_digits_verified(obj, article_text):
                bad.append(obj)

    walk(item)
    return bad
