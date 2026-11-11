#!/usr/bin/env python3
"""Normalize lx-mobile-bar on standalone service landings + link template overrides."""
import re
import sys
from pathlib import Path

MARK_CSS = "lireate_design_service_mobile_bar_css_v1"
MARK_SCRIPT = "lireate_design_service_mobile_bar_js_v1"

CANONICAL_BAR = """<aside class="lx-mobile-bar" aria-label="Быстрый звонок и мессенджеры">
  <a class="lx-mobile-bar-btn lx-mobile-bar-btn--call" href="tel:+79600484957">Позвонить</a>
  <a class="lx-mobile-bar-btn" href="https://t.me/lireate_patent" target="_blank" rel="noopener noreferrer" data-lx-icon="telegram" aria-label="Telegram"></a>
  <a class="lx-mobile-bar-btn lx-mobile-bar-btn--max" href="https://max.ru/u/f9LHodD0cOI8jsPagjibEve2cn5_xPW0X1sf3PhbS5TMijA78DnUeDEpUAI" target="_blank" rel="noopener noreferrer" data-lx-icon="max-white" aria-label="MAX"></a>
  <a class="lx-mobile-bar-btn lx-mobile-bar-btn--primary" href="#contact" data-lx-svc-lead="1">Заявка</a>
</aside>"""

LANDING_INDEX = [
    "findtz/index.php",
    "registraciya_tovarnogo_znaka/index.php",
    "registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/index.php",
    "prodlenie_tovarnogo_znaka/index.php",
    "vozrazhenie_protiv_registracii_tovarnogo_znaka/index.php",
    "registraciya_tovarnogo_znaka_v_kitae/index.php",
    "zashchita_avtorskih_prav/index.php",
]

CSS_LINK = (
    f'  <link rel="stylesheet" href="/template/css/lireate-service-mobile-bar.css?v=20261111svc1" '
    f'/><!-- {MARK_CSS} -->\n'
)

METRIKA_SCRIPT = (
    f'  <script defer src="/template/js/lireate-service-metrika-goals.js?v=20261111svc1"></script>'
    f'<!-- {MARK_SCRIPT} -->\n'
)

MOBILE_BAR_RE = re.compile(
    r"<aside\s+class=\"lx-mobile-bar[^\"]*\"[\s\S]*?</aside>",
    re.I,
)


def patch_html(text: str) -> str:
    if MOBILE_BAR_RE.search(text):
        text = MOBILE_BAR_RE.sub(CANONICAL_BAR, text, count=1)
    else:
        if "</body>" in text:
            text = text.replace("</body>", CANONICAL_BAR + "\n</body>", 1)

    if MARK_CSS not in text and "</head>" in text:
        text = text.replace("</head>", CSS_LINK + "</head>", 1)

    if MARK_SCRIPT not in text and "</body>" in text:
        text = text.replace("</body>", METRIKA_SCRIPT + "</body>", 1)

    # Prefer template mobile-bar.js on LU pages (≤768 behavior).
    tpl_bar = "/template/js/lireate-service-mobile-bar.js?v=20261111svc1"
    if tpl_bar not in text:
        text = re.sub(
            r'<script\s+[^>]*src="[^"]*lireate-mobile-bar\.js[^"]*"[^>]*>\s*</script>',
            f'<script defer src="{tpl_bar}"></script>',
            text,
            count=1,
            flags=re.I,
        )

    return text


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: patch_service_landings.py DOCROOT", file=sys.stderr)
        raise SystemExit(2)
    docroot = Path(sys.argv[1])
    changed = []
    for rel in LANDING_INDEX:
        path = docroot / rel
        if not path.is_file():
            print(f"SKIP missing {rel}", file=sys.stderr)
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        out = patch_html(raw)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            changed.append(rel)
    print("LANDING_PATCH_OK", len(changed), *changed)


if __name__ == "__main__":
    main()
