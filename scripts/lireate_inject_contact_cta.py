#!/usr/bin/env python3
"""Insert shared contact CTA block into Lireate article.html (one per article)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNIPPET_PATH = ROOT / "shared" / "lireate-contact-cta-snippet.html"
CTA_MARK = "<b>Консультация в Telegram</b>"
WHATSAPP_MARK = "<b>Написать в WhatsApp</b>"
MAX_MARK = "<b>Написать в MAX</b>"
SNIPPET_BLOCK_RE = re.compile(
    r"<table>\s*<tbody>\s*<tr>.*?Консультация в Telegram.*?"
    r"Написать в WhatsApp.*?"
    r"(?:Написать в MAX.*?)?</table>\s*"
    r"(?:<p align=\"center\">Кратко опишите задачу.*?</p>\s*)?",
    re.DOTALL | re.IGNORECASE,
)
LEGACY_TWO_COL_CTA_RE = re.compile(
    r"<table>\s*<tbody>\s*<tr>\s*"
    r"<td><p align=\"center\"><a href=\"https://t\.me/lireate_patent\"[^>]*>"
    r"<b>Консультация в Telegram</b></a></p></td>\s*"
    r"<td><p align=\"center\"><a href=\"https://wa\.me/79600484957\"[^>]*>"
    r"<b>Написать в WhatsApp</b></a></p></td>\s*"
    r"</tr>\s*</tbody>\s*</table>\s*",
    re.DOTALL | re.IGNORECASE,
)


def load_snippet() -> str:
    raw = SNIPPET_PATH.read_text(encoding="utf-8")
    lines = [ln for ln in raw.splitlines() if not ln.strip().startswith("<!--")]
    return "\n".join(lines).strip() + "\n\n"


def has_cta(html: str) -> bool:
    return CTA_MARK in html and WHATSAPP_MARK in html and MAX_MARK in html


def upgrade_legacy_cta(html: str, snippet: str) -> tuple[str, bool]:
    """Replace old 2-column CTA blocks with the current 3-link snippet."""
    if MAX_MARK in html:
        return html, False
    if not (CTA_MARK in html and WHATSAPP_MARK in html):
        return html, False
    new, n = LEGACY_TWO_COL_CTA_RE.subn(snippet, html)
    return new, n > 0


def dedupe_cta(html: str, snippet: str) -> tuple[str, int]:
    """Leave a single CTA block; remove duplicates."""
    blocks = list(SNIPPET_BLOCK_RE.finditer(html))
    if len(blocks) <= 1:
        return html, 0
    # Prefer the block that includes MAX (current snippet).
    keep_idx = 0
    for i, m in enumerate(blocks):
        if MAX_MARK in m.group(0):
            keep_idx = i
            break
    new = html
    removed = 0
    for i, m in reversed(list(enumerate(blocks))):
        if i == keep_idx:
            continue
        new = new[: m.start()] + new[m.end() :]
        removed += 1
    if removed and MAX_MARK not in blocks[keep_idx].group(0):
        # Replace the surviving legacy block with the full snippet.
        m = blocks[keep_idx]
        new = new[: m.start()] + snippet + new[m.end() :]
    return new, removed


def insertion_point(html: str) -> int | None:
    m = re.search(
        r"<blockquote>\s*\n?\s*<b>Материал проверен:",
        html,
        re.IGNORECASE,
    )
    if m:
        return m.start()
    m = re.search(r"<h2>\s*Частые вопросы\s*</h2>", html, re.IGNORECASE)
    if m:
        return m.start()
    m = re.search(r"<h2>\s*FAQ\s*</h2>", html, re.IGNORECASE)
    if m:
        return m.start()
    h2s = list(re.finditer(r"<h2[^>]*>", html, re.IGNORECASE))
    if len(h2s) >= 2:
        return h2s[1].start()
    return None


def process_file(path: Path, snippet: str, dry_run: bool) -> str:
    html = path.read_text(encoding="utf-8")
    html, upgraded = upgrade_legacy_cta(html, snippet)
    html, removed = dedupe_cta(html, snippet)
    if upgraded and not dry_run:
        path.write_text(html, encoding="utf-8")
    blocks = list(SNIPPET_BLOCK_RE.finditer(html))
    if len(blocks) > 1:
        html, extra_removed = dedupe_cta(html, snippet)
        removed += extra_removed
        blocks = list(SNIPPET_BLOCK_RE.finditer(html))

    if has_cta(html) and len(blocks) <= 1:
        if (removed or upgraded) and not dry_run:
            path.write_text(html, encoding="utf-8")
        return "skip_has_cta" if removed == 0 and not upgraded else "deduped"

    pos = insertion_point(html)
    if pos is None:
        return "no_anchor"

    new_html = html[:pos] + snippet + html[pos:]
    if not dry_run:
        path.write_text(new_html, encoding="utf-8")
    return "injected"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--articles-root",
        type=Path,
        default=ROOT / "memory" / "blog" / "articles",
    )
    args = ap.parse_args()
    snippet = load_snippet()
    stats: dict[str, list[str]] = {}
    for path in sorted(args.articles_root.glob("*/article.html")):
        if path.parent.name.startswith("B"):
            continue
        result = process_file(path, snippet, args.dry_run)
        stats.setdefault(result, []).append(path.parent.name)
    for key, dirs in sorted(stats.items()):
        print(f"{key}: {len(dirs)}")
        for d in dirs:
            print(f"  {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
