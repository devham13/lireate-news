"""Pre-publish SEO meta validation for Lireate news (stdlib, Py3.6+)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from lireate_meta_text import normalize_seo_description, normalize_seo_title

_TITLE_MAX = 255
_DESC_MAX = 200
_DESC_MIN = 80
_BAD_END = re.compile(r"[\wа-яА-ЯёЁ]$")
_REQUIRED_CANONICAL_KEYS = ("slug", "lireate_seo_url")


def _slug_from_meta(meta):
    explicit = (meta.get("lireate_seo_url") or meta.get("slug") or "").strip().strip("/")
    return explicit.replace("/", "_")


def validate_article_meta(meta, html=""):
    """Return list of error strings; empty means OK."""
    errors = []
    if not isinstance(meta, dict):
        return ["meta must be a dict"]
    title = (meta.get("seo_title") or meta.get("title") or meta.get("h1") or "").strip()
    if title == "":
        errors.append("missing seo_title/title/h1")
    elif len(title) > _TITLE_MAX:
        errors.append("seo_title longer than {0} chars".format(_TITLE_MAX))
    desc = (meta.get("description") or "").strip()
    if desc == "":
        errors.append("missing meta description")
    elif len(desc) < _DESC_MIN:
        errors.append("description shorter than {0} chars".format(_DESC_MIN))
    elif len(desc) > _DESC_MAX + 5:
        errors.append("description longer than {0} chars before normalize".format(_DESC_MAX))
    norm_desc = normalize_seo_description(desc, _DESC_MAX)
    if norm_desc != desc and _BAD_END.search(desc[_DESC_MAX - 1 : _DESC_MAX + 2] if len(desc) > _DESC_MAX else ""):
        errors.append("description appears truncated mid-word in source meta")
    slug = _slug_from_meta(meta)
    if slug == "":
        errors.append("missing slug / lireate_seo_url")
    h1 = (meta.get("h1") or meta.get("lireate_display_name") or "").strip()
    if h1 == "":
        errors.append("missing h1 / lireate_display_name")
    if html:
        if "<h1" in html.lower():
            errors.append("article.html must not contain h1 (CMS provides H1 from name)")
        if re.search(r"<title[\s>]", html, re.I):
            errors.append("article.html must not contain <title>")
    return errors


def find_similar_published_titles(meta, articles_root, state_file=None):
    """Block new publish when same primary_query or very similar title exists."""
    warnings = []
    primary = (meta.get("primary_query") or meta.get("title_seo") or meta.get("title") or "").strip().lower()
    if not primary:
        return warnings
    root = Path(articles_root)
    if not root.is_dir():
        return warnings
    for meta_path in root.glob("L*/article.meta.json"):
        try:
            other = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if other.get("topic_id") == meta.get("topic_id"):
            continue
        oq = (other.get("primary_query") or other.get("title_seo") or other.get("title") or "").strip().lower()
        if oq and oq == primary:
            warnings.append(
                "duplicate primary_query/intent with {0}: {1!r}".format(meta_path.parent.name, primary)
            )
    if state_file:
        state_path = Path(state_file)
        if state_path.is_file():
            try:
                data = json.loads(state_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                data = {}
            for entry in data.values() if isinstance(data, dict) else []:
                if not isinstance(entry, dict):
                    continue
                st = (entry.get("status") or "").lower()
                if st != "published":
                    continue
                nm = (entry.get("title") or entry.get("name") or "").strip().lower()
                if nm and primary in nm:
                    warnings.append("similar published title in state: {0!r}".format(nm))
    return warnings


def validate_for_publish(meta, html, repo_root, state_file=None):
    errors = validate_article_meta(meta, html)
    arts = Path(repo_root) / "memory" / "blog" / "articles"
    dups = find_similar_published_titles(meta, arts, state_file)
    errors.extend(dups)
    return errors