#!/usr/bin/env python3
"""Idempotent: dogovory + registraciya_programm_evm in root .htaccess SEO rules."""
from __future__ import annotations

import sys
from pathlib import Path

MARK = "lireate_design_htaccess_new_services_v1"

TRAILING_RULE_OLD = (
    "RewriteRule ^(registraciya_tovarnogo_znaka|registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat|"
    "findtz|prodlenie_tovarnogo_znaka)$ /$1/ [R=301,L]"
)
TRAILING_RULE_NEW = (
    "RewriteRule ^(registraciya_tovarnogo_znaka|registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat|"
    "findtz|prodlenie_tovarnogo_znaka|dogovory|registraciya_programm_evm)$ /$1/ [R=301,L]"
)


def patch(text: str) -> str:
    if "prodlenie_tovarnogo_znaka" not in text:
        raise SystemExit("root .htaccess: prodlenie anchor missing")
    out = text
    if "dogovory|registraciya_programm_evm)$ /$1/" not in out and TRAILING_RULE_OLD in out:
        out = out.replace(TRAILING_RULE_OLD, TRAILING_RULE_NEW, 1)
    anchor = "RewriteCond %{REQUEST_URI} !^/prodlenie_tovarnogo_znaka/?$ [NC]\n"
    insert = (
        f"RewriteCond %{{REQUEST_URI}} !^/dogovory/?$ [NC] /* {MARK} */\n"
        "RewriteCond %{REQUEST_URI} !^/registraciya_programm_evm/?$ [NC]\n"
    )
    if MARK not in out and anchor in out:
        out = out.replace(anchor, anchor + insert, 1)
    return out


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} DOCROOT/.htaccess", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    raw = path.read_text(encoding="utf-8", errors="replace")
    out = patch(raw)
    if out == raw:
        print("HTACCESS_SERVICES_UNCHANGED")
        return
    path.write_text(out, encoding="utf-8")
    print("HTACCESS_SERVICES_OK")


if __name__ == "__main__":
    main()
