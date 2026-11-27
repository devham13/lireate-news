#!/usr/bin/env python3
"""Validate editorial blog SEO plan JSON (wave apply input)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TITLE_MAX = 60
DESC_MIN = 120
DESC_MAX = 160

_BAD_END = re.compile(r"[\s,;:\-–—]$")
_BAD_MID = re.compile(
    r"(\s(и|а|но|или|что|как|для|при|по|на|о|об|от|до|без|со|в|во|к|ко|у|с|из|за)\s*$)|"
    r"(\s(и|а|но|или|что|как|для|при|по|на|о|об|от|до|без|со|в|во|к|ко|у|с|из|за)$)",
    re.I,
)
_SERVICE = re.compile(r"\bL\d{2}\b", re.I)
_ANGLO = re.compile(r"\b(vs|workflow|workflow)\b", re.I)
_PROPER_END = re.compile(r'[.!?»"\u201d\u2026…)]$')
_TRAILING_ART = re.compile(r"^[«\"'(\[]+|[»\"')\]]+$")
_CUT_MID = re.compile(
    r"^(Как вы видите|Таким образом|Давайте признаемся|Следует отметить)",
    re.I,
)


def _clean(s: str) -> str:
    return _TRAILING_ART.sub("", (s or "").strip())


def validate_row(row: dict, titles: dict, descs: dict) -> list[str]:
    errs = []
    slug = (row.get("seo_url") or "").strip().strip("/")
    if not slug:
        errs.append("missing seo_url")
        return errs
    title = _clean(row.get("seo_title") or "")
    desc = _clean(row.get("seo_description") or "")
    if not title:
        errs.append("{0}: empty seo_title".format(slug))
    else:
        if len(title) > TITLE_MAX:
            errs.append("{0}: title len {1}>{2}".format(slug, len(title), TITLE_MAX))
        if title.endswith((".", "?", "!", "…")):
            errs.append("{0}: title must not end with sentence punctuation".format(slug))
        if title in titles and titles[title] != slug:
            errs.append("{0}: duplicate title with {1}".format(slug, titles[title]))
    if not desc:
        errs.append("{0}: empty seo_description".format(slug))
    else:
        n = len(desc)
        if n < DESC_MIN or n > DESC_MAX:
            errs.append("{0}: description len {1} not in {2}-{3}".format(slug, n, DESC_MIN, DESC_MAX))
        if not _PROPER_END.search(desc.rstrip()):
            errs.append("{0}: description lacks proper ending".format(slug))
        if _BAD_END.search(desc) or _BAD_MID.search(desc):
            errs.append("{0}: description ends on preposition/conjunction/punctuation".format(slug))
        if _SERVICE.search(title + " " + desc):
            errs.append("{0}: internal Lxx marker in meta".format(slug))
        if _ANGLO.search(title + " " + desc) and not _ANGLO.search(row.get("body_hint", "")):
            errs.append("{0}: anglicism in meta".format(slug))
        if _CUT_MID.match(desc):
            errs.append("{0}: description starts as article mid-stream".format(slug))
        if desc.endswith("."):
            if desc[-2:].isalpha() and len(desc) < DESC_MAX:
                pass
            # forbid lone truncated sentence ending with period mid-thought (heuristic)
        if desc in descs and descs[desc] != slug:
            errs.append("{0}: duplicate description with {1}".format(slug, descs[desc]))
    if title:
        titles[title] = slug
    if desc:
        descs[desc] = slug
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=Path)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    articles = plan.get("articles") or []
    titles: dict = {}
    descs: dict = {}
    all_errs = []
    for row in articles:
        all_errs.extend(validate_row(row, titles, descs))
    if all_errs:
        for e in all_errs:
            print(e)
        print("STATUS: VALIDATE_FAIL count={0}".format(len(all_errs)))
        return 1 if args.strict else 2
    print("STATUS: VALIDATE_OK articles={0}".format(len(articles)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())