#!/usr/bin/env python3
"""Inject lx-article-cover and inline-collage figures into article.html."""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_collage.constants import SLOT_FILES  # noqa: E402
from lireate_collage.eligibility import collage_allowed  # noqa: E402


def inject_cover_figure(html, alt):
    fig = (
        '\n<figure class="lx-article-cover" data-cover-style="collage-v1">\n'
        '  <img src="cover/cover.png" alt="{0}" loading="eager" width="860" height="400">\n'
        "</figure>\n"
    ).format(alt.replace('"', "&quot;"))
    if 'class="lx-article-cover"' in html:
        return html, "cover figure exists"
    # After first paragraph or at start
    if html.strip().startswith("<p"):
        return re.sub(r"(</p>\s*)", r"\1" + fig, html, count=1), "injected cover after first p"
    return fig + html, "prepended cover"


def inject_inline_figures(html, spec_doc):
    report = []
    illustrations = spec_doc.get("illustrations") or []
    h2_iter = list(re.finditer(r"<h2[^>]*>(.*?)</h2>", html, flags=re.I | re.S))
    titles = []
    for m in h2_iter:
        t = re.sub(r"<[^>]+>", "", m.group(1))
        t = re.sub(r"\s+", " ", t).strip()
        if t.lower() in {"частые вопросы", "faq"}:
            break
        titles.append(t)

    for item in illustrations:
        slot = item.get("slot") or ""
        fname = SLOT_FILES.get(slot, "")
        tmpl = item.get("template") or ""
        alt = item.get("alt") or ""
        cap = item.get("figcaption") or ""
        fig = (
            '\n<figure class="inline-collage" data-inline-style="collage-v1" data-template="{tmpl}" data-slot="{slot}">\n'
            '  <img src="cover/{file}" alt="{alt}" loading="lazy" width="1200" height="675">\n'
        ).format(tmpl=tmpl, slot=slot, file=fname, alt=alt.replace('"', "&quot;"))
        if cap:
            fig += "  <figcaption>{0}</figcaption>\n".format(cap)
        fig += "</figure>\n"

        if 'data-slot="{0}"'.format(slot) in html and "inline-collage" in html:
            report.append("skip {0} exists".format(slot))
            continue

        slot_idx = {"inline_1": 0, "inline_2": 1, "inline_3": 2}.get(slot, 0)
        if slot_idx < len(titles):
            title = titles[slot_idx]
            pattern = re.compile(
                r"(<h2[^>]*>[\s\S]*?" + re.escape(title) + r"[\s\S]*?</h2>)",
                re.I,
            )
            if pattern.search(html):
                html = pattern.sub(r"\1" + fig, html, count=1)
                report.append("injected {0} after H2".format(slot))
                continue
        html += fig
        report.append("appended {0}".format(slot))
    return html, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--article-dir", type=Path, required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    article_dir = args.article_dir.resolve()
    if not args.force:
        ok, reason = collage_allowed(article_dir)
        if not ok:
            print("INJECT_BLOCKER: {0}".format(reason))
            return 2

    html_path = article_dir / "article.html"
    if not html_path.is_file():
        print("INJECT_BLOCKER: no article.html")
        return 2

    meta_path = article_dir / "article.meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    alt = meta.get("h1") or meta.get("title") or "Обложка статьи"

    html = html_path.read_text(encoding="utf-8")
    html, r1 = inject_cover_figure(html, alt)
    spec_path = article_dir / "cover" / "inline-specs.json"
    r2 = []
    if spec_path.is_file():
        doc = json.loads(spec_path.read_text(encoding="utf-8"))
        html, r2 = inject_inline_figures(html, doc)

    html_path.write_text(html, encoding="utf-8")
    print("OK inject", r1, r2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
