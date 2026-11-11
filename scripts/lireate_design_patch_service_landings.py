#!/usr/bin/env python3
"""Exactly one lx-mobile-bar on standalone LU service landings (idempotent)."""
import re
import sys
from pathlib import Path

MARK_CSS = "lireate_design_service_mobile_bar_css_v1"
MARK_SCRIPT = "lireate_design_service_mobile_bar_js_v1"
MARK_BAR = 'data-lx-svc-mobile-bar="canonical"'
MARK_STICKY = "lireate_design_sticky_blocks_cleared_v1"

CANONICAL_BAR = f"""<aside class="lx-mobile-bar" {MARK_BAR} aria-label="Быстрый звонок и мессенджеры">
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

# Empty sticky includes (no second lx-mobile-bar).
STICKY_REL_PATHS = [
    "findtz/blocks/lireate-sticky-mobile.inc.php",
    "registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/blocks/lireate-sticky-mobile.inc.php",
    "prodlenie_tovarnogo_znaka/blocks/lireate-sticky-mobile.inc.php",
    "vozrazhenie_protiv_registracii_tovarnogo_znaka/blocks/lireate-sticky-mobile.inc.php",
    "registraciya_tovarnogo_znaka_v_kitae/blocks/lireate-sticky-mobile.inc.php",
    "zashchita_avtorskih_prav/blocks/lireate-sticky-mobile.inc.php",
    "registraciya_tovarnogo_znaka/blocks/lireate-sticky-mobile-landing.inc.php",
]

CSS_LINK = (
    '  <link rel="stylesheet" href="/template/css/lireate-service-mobile-bar.css?v=20261111svc3" '
    f'/><!-- {MARK_CSS} -->\n'
)

METRIKA_SCRIPT = (
    '  <script defer src="/template/js/lireate-service-metrika-goals.js?v=20261111svc3"></script>'
    f'<!-- {MARK_SCRIPT} -->\n'
)

EMPTY_STICKY_BODY = (
    "<?php\n/* "
    + MARK_STICKY
    + ' — canonical bar only in index.php (data-lx-svc-mobile-bar="canonical"). */\n'
)

MOBILE_BAR_RE = re.compile(
    r"<aside\s+class=\"lx-mobile-bar[^\"]*\"[\s\S]*?</aside>\s*",
    re.I,
)


def strip_all_bars(text: str) -> str:
    while MOBILE_BAR_RE.search(text):
        text = MOBILE_BAR_RE.sub("", text, count=1)
    return text


def patch_html(text: str) -> str:
    text = strip_all_bars(text)

    if "</body>" in text:
        if MARK_BAR not in text:
            text = text.replace("</body>", CANONICAL_BAR + "\n</body>", 1)

    while text.count(MARK_CSS) > 1:
        idx = text.rfind(CSS_LINK.strip())
        if idx == -1:
            break
        text = text[:idx] + text[idx + len(CSS_LINK.strip()) + 1 :]

    if MARK_CSS not in text and "</head>" in text:
        text = text.replace("</head>", CSS_LINK + "</head>", 1)

    metrika_re = re.compile(
        r'\s*<script defer src="/template/js/lireate-service-metrika-goals\.js[^"]*"></script>'
        rf'<!-- {MARK_SCRIPT} -->\s*',
        re.I,
    )
    text = metrika_re.sub("", text)
    if MARK_SCRIPT not in text and "</body>" in text:
        text = text.replace("</body>", METRIKA_SCRIPT + "</body>", 1)

    tpl_bar = "/template/js/lireate-service-mobile-bar.js?v=20261111svc3"
    text = re.sub(
        r'<script\s+[^>]*src="[^"]*lireate-mobile-bar\.js[^"]*"[^>]*>\s*</script>\s*',
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'<script defer src="/template/js/lireate-service-mobile-bar\.js[^"]*"></script>\s*',
        "",
        text,
        flags=re.I,
    )
    if tpl_bar not in text and "</body>" in text:
        text = text.replace("</body>", '  <script defer src="' + tpl_bar + '"></script>\n</body>', 1)

    return text


def clear_sticky_blocks(docroot, repo_root=None):
    changed = []
    bak_suffix = "bak-2026-11-11-dock"
    template_std = None
    template_land = None
    if repo_root:
        tdir = repo_root / "hosting-design" / "service-landings" / "blocks"
        template_std = tdir / "lireate-sticky-mobile.inc.php"
        template_land = tdir / "lireate-sticky-mobile-landing.inc.php"

    for rel in STICKY_REL_PATHS:
        path = docroot / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if template_land and rel.endswith("lireate-sticky-mobile-landing.inc.php") and template_land.is_file():
            body = template_land.read_text(encoding="utf-8", errors="replace")
        elif template_std and template_std.is_file():
            body = template_std.read_text(encoding="utf-8", errors="replace")
        else:
            body = EMPTY_STICKY_BODY
        if path.is_file() and path.read_text(encoding="utf-8", errors="replace") == body:
            continue
        if path.is_file():
            bak = path.with_suffix(path.suffix + f".{bak_suffix}")
            bak.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        path.write_text(body, encoding="utf-8")
        changed.append(rel)
    return changed


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: patch_service_landings.py DOCROOT [REPO_ROOT]", file=sys.stderr)
        raise SystemExit(2)
    docroot = Path(sys.argv[1])
    repo_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1]
    changed = clear_sticky_blocks(docroot, repo_root)
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
