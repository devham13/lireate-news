#!/usr/bin/env python3
"""Удалить служебные пометки (Вордстат/MCP/среда подготовки) из article.html."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "memory/blog/articles"

# Хвосты и целые фразы в видимом тексте (не трогаем статьи про MCP как тему)
SKIP_DIR_PARTS = ("podklyuchenie-mcp-cursor", "B03-")

STRIP_RES = [
    re.compile(r"\s*[;.]\s*Показы Яндекс (?:Вордстат|Wordstat)[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*показы Яндекс (?:Вордстат|Wordstat)[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*Яндекс Вордстат[^.\"<]*среде подготовки[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*Вордстат в среде подготовки[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*Показы Яндекс Вордстат[^.\"<]*не запрашивал[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*Показы Яндекс Вордстат не включались\s*\([^)]*MCP[^)]*\)\.?", re.I),
    re.compile(r"\s*[;.]\s*Показы Яндекс Вордстат в материал не включались[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*Показы поискового спроса[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*объёмы Вордстата[^.\"<]*\.?", re.I),
    re.compile(r"объёмы Вордстата в текст не включались[^.\"<]*\.?\s*", re.I),
    re.compile(r"\s*[;.]\s*Ключевые запросы сверены по SEO-сводке и Яндекс Вордстат[^.\"<]*\.?", re.I),
    re.compile(r"\s*\(см\.\s*research-notes\)", re.I),
    re.compile(r"\s+research-notes\)\.?", re.I),
    re.compile(r"\s+из research-notes", re.I),
    re.compile(r"\s*[;.]\s*Яндекс Вордстат в этой сессии[^.\"<]*\.?", re.I),
    re.compile(r"\s*[;.]\s*Судебные дела в статью не включались\.?", re.I),
    re.compile(
        r"<b>Достоверность данных:</b>\s*\d{2}\.\d{2}\.\d{4}\.\s*Показы Яндекс Вордстат не включались\s*\([^)]*\)\.?\s*",
        re.I,
    ),
]

# Замена «только дата» после strip MCP (L50/L51)
DATE_ONLY = re.compile(
    r"(<b>Достоверность данных:</b>)\s*(\d{2}\.\d{2}\.\d{4})\.\s*(?=</)",
    re.I,
)


def slug_for(article_dir: Path) -> str | None:
    meta = article_dir / "article.meta.json"
    if meta.is_file():
        try:
            return json.loads(meta.read_text(encoding="utf-8")).get("slug")
        except json.JSONDecodeError:
            pass
    return None


def strip_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    for rx in STRIP_RES:
        text = rx.sub("", text)
    text = DATE_ONLY.sub(r"\1 сверка с официальными источниками на \2.", text)
    # убрать двойные пробелы перед закрытием тега
    text = re.sub(r"  +", " ", text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed: list[dict[str, str]] = []
    for d in sorted(ARTICLES.iterdir()):
        if not d.is_dir() or any(p in d.name for p in SKIP_DIR_PARTS):
            continue
        html = d / "article.html"
        if not html.is_file():
            continue
        if strip_file(html):
            changed.append({"dir": d.name, "slug": slug_for(d) or ""})
    print(json.dumps({"changed_count": len(changed), "changed": changed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
