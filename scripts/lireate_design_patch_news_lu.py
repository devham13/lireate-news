#!/usr/bin/env python3
"""Add lireate-legacy-article-lu body class + CSS for CMS news articles."""
import sys
from pathlib import Path

MARK = "lireate_design_news_lu_v1"
MARK_CSS = "lireate-legacy-article-lu.css"
MIN_LINES = 6000


def patch(text: str) -> str:
    if text.count("\n") < MIN_LINES:
        raise SystemExit("main.php too short")

    if MARK not in text:
        anchor = " if($temp['news_id']!=false){"
        if anchor not in text:
            raise SystemExit("news_id anchor missing")
        insert = (
            f"<?php /* {MARK} */ if (!empty($temp['news_id']))"
            " echo ' lireate-legacy-article-lu lireate-cms-page-dark'; ?>"
        )
        # After body class output — find cms-default body tag area
        body_cls = "lireate_cms_dark_body_v1"
        if body_cls in text and MARK not in text:
            old = (
                f" /* {body_cls} */ if (in_array($temp['page'],"
            )
            if old in text:
                text = text.replace(
                    old,
                    f" /* {MARK} */ if (!empty($temp['news_id']))"
                    " echo ' lireate-legacy-article-lu lireate-cms-page-dark';"
                    + old,
                    1,
                )

    if MARK_CSS not in text:
        head_anchor = "</head>"
        block = (
            f'\t<?php /* {MARK} css */ if (!empty($temp["news_id"])): ?>\n'
            '\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" />\n'
            '\t<link rel="stylesheet" href="/template/css/lireate-cms-page-dark.css?v=20261111design3" />\n'
            f'\t<link rel="stylesheet" href="/template/css/lireate-legacy-article-lu.css?v=20261111art2" />\n'
            f'\t<link rel="stylesheet" href="/template/css/lireate-legacy-cms-lu.css?v=20261111leg1" />\n'
            f'\t<link rel="stylesheet" href="/template/css/lireate-lu-viewport.css?v=20261111vp3" />\n'
            f'\t<link rel="stylesheet" href="/template/css/lireate-home-modal-lu.css?v=20261111mod2" />\n'
            f'\t<script defer src="/template/js/lireate-home-modal-lu.js?v=20261111mod2"></script>\n'
            "\t<?php endif; ?>\n"
        )
        if head_anchor in text:
            text = text.replace(head_anchor, block + head_anchor, 1)

    return text


def main() -> None:
    path = Path(sys.argv[1])
    out = patch(path.read_text(encoding="utf-8", errors="replace"))
    path.write_text(out, encoding="utf-8")
    print("NEWS_LU_PATCH_OK")


if __name__ == "__main__":
    main()
