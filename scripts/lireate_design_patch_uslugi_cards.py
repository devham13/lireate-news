#!/usr/bin/env python3
"""Inject dogovory + programm_evm lu-cards into uslugi lib before lu-contact."""
import re
import sys
from pathlib import Path

MARK = "lireate_design_uslugi_dogovory_evm_v1"
CONTACT_SECTION_RE = re.compile(
    r'<section\s+class="lu-contact"\s+id="lu-contact"[^>]*>',
    re.I,
)
CARDS = f"""
    <section class="lu-section" aria-labelledby="lu-is-contracts"><!-- {MARK} -->
      <div class="lu-section-head">
        <h2 class="lu-h2" id="lu-is-contracts">Договоры и программы</h2>
        <p class="lu-section-lead">Права на код, контент и сделки с объектами ИС.</p>
      </div>
      <div class="lu-grid">
        <a class="lu-card" href="/dogovory/">
          <span class="lu-card-top"><span class="lu-card-num">01</span><span class="lu-card-tag">ГК РФ</span></span>
          <h3 class="lu-card-title">Договоры в сфере ИС</h3>
          <p class="lu-card-text">Лицензия, франчайзинг, отчуждение, авторский заказ и регистрация распоряжений в Роспатенте.</p>
          <span class="lu-card-more">Подробнее <svg class="lu-ico lu-ico--arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </a>
        <a class="lu-card" href="/registraciya_programm_evm/">
          <span class="lu-card-top"><span class="lu-card-num">02</span><span class="lu-card-tag">ПО и БД</span></span>
          <h3 class="lu-card-title">Регистрация программ для ЭВМ</h3>
          <p class="lu-card-text">Регистрация программы и базы данных, защита сайта и приложений, сопровождение в Роспатенте.</p>
          <span class="lu-card-more">Подробнее <svg class="lu-ico lu-ico--arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </a>
      </div>
    </section>

"""


def patch_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if MARK in raw:
        return False
    m = CONTACT_SECTION_RE.search(raw)
    if not m:
        return False
    anchor = m.group(0)
    out = raw.replace(anchor, CARDS + anchor, 1)
    path.write_text(out, encoding="utf-8")
    return True


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} DOCROOT", file=sys.stderr)
        raise SystemExit(2)
    docroot = Path(sys.argv[1])
    candidates = [
        docroot / "template/page/uslugi/lireate-uslugi-lib.php",
        docroot / "template/page/uslugi/lireate-uslugi-render.php",
    ]
    for p in candidates:
        if not p.is_file():
            continue
        if patch_file(p):
            print("PATCHED", p)
            print("USLUGI_CARDS_OK")
            return
        if MARK in p.read_text(encoding="utf-8", errors="replace"):
            print("USLUGI_CARDS_OK already")
            return
        print(f"USLUGI_CARDS_SKIP anchor missing in {p}", file=sys.stderr)
        raise SystemExit(0)
    print("USLUGI_CARDS_SKIP no uslugi lib", file=sys.stderr)
    raise SystemExit(0)


if __name__ == "__main__":
    main()
