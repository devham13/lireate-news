#!/usr/bin/env python3
"""CMS news articles: lireate-legacy-article-lu + dark LU assets (idempotent, py3.6)."""
import subprocess
import sys
from pathlib import Path

MARK = "lireate_design_news_lu_v1"
MARK_CSS = "lireate-legacy-article-lu.css"
MIN_LINES = 6000
PAGE_CONTAINER = "page_container"

HEAD_BLOCK = f"""\t<?php /* {MARK} css */ if (!empty($temp["news_id"])): ?>
\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" />
\t<link rel="stylesheet" href="/template/css/lireate-cms-page-dark.css?v=20261111design3" />
\t<link rel="stylesheet" href="/template/css/lireate-legacy-article-lu.css?v=20261111art3" />
\t<link rel="stylesheet" href="/template/css/lireate-legacy-cms-lu.css?v=20261111leg2" />
\t<link rel="stylesheet" href="/template/css/lireate-lu-viewport.css?v=20261111vp5" />
\t<link rel="stylesheet" href="/template/css/lireate-home-modal-lu.css?v=20261111mod2" />
\t<script defer src="/template/js/lireate-home-modal-lu.js?v=20261111mod2"></script>
\t<?php endif; ?>
"""

BODY_SNIP = (
    f" /* {MARK} */ if (!empty($temp['news_id']))"
    " echo ' lireate-legacy-article-lu lireate-cms-page-dark';"
)


def _validate(text: str, label: str) -> None:
    if text.count("\n") + 1 < MIN_LINES:
        raise SystemExit(f"{label}: main.php too short (< {MIN_LINES} lines)")
    if PAGE_CONTAINER not in text:
        raise SystemExit(f"{label}: missing {PAGE_CONTAINER}")


def _php_lint(content: str) -> None:
    tmp = Path("/tmp/lireate-main-php-news-lu.php")
    tmp.write_text(content, encoding="utf-8")
    r = subprocess.run(
        ["php", "-l", str(tmp)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if r.returncode != 0:
        raise SystemExit(f"php -l failed: {r.stderr or r.stdout}")


def patch(text: str) -> str:
    _validate(text, "before news_lu")

    if MARK not in text:
        legacy_home = " if($temp['page']=='home') echo ' lireate-home-dark';?>"
        if BODY_SNIP not in text and legacy_home in text:
            text = text.replace(legacy_home, BODY_SNIP + legacy_home, 1)
        elif "lireate_cms_dark_body_v1" in text:
            anchor = " /* lireate_cms_dark_body_v1 */ if (in_array($temp['page'],"
            if anchor in text and BODY_SNIP not in text:
                text = text.replace(anchor, BODY_SNIP + anchor, 1)

    if f"{MARK} css" not in text and MARK_CSS not in text:
        if "</head>" in text:
            text = text.replace("</head>", HEAD_BLOCK + "</head>", 1)
        else:
            raise SystemExit("news_lu: </head> missing")
    elif f"{MARK} css" not in text and MARK_CSS in text and HEAD_BLOCK.strip() not in text:
        pass

    _validate(text, "after news_lu")
    return text


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/main.php", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw)
    if out == raw:
        print("UNCHANGED")
        return
    _php_lint(out)
    path.write_text(out, encoding="utf-8")
    print("NEWS_LU_PATCH_OK", MARK in out)


if __name__ == "__main__":
    main()
