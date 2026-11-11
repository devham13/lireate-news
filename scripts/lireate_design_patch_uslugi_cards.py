#!/usr/bin/env python3
"""Inject dogovory + programm_evm lu-cards into uslugi CMS inc before lu-contact."""
import re
import sys
from pathlib import Path

MARK = "lireate_design_uslugi_dogovory_evm_v1"
CONTACT_SECTION_RE = re.compile(
    r'<section\s+class="lu-contact"\s+id="lu-contact"[^>]*>',
    re.I,
)
TITLE_DOG = "Договоры в сфере ИС"
TITLE_EVM = "Регистрация программ для ЭВМ"
CARDS = """
    <section class="lu-section" aria-labelledby="lu-is-contracts"><!-- {mark} -->
      <div class="lu-section-head">
        <h2 class="lu-h2" id="lu-is-contracts">Договоры и программы</h2>
        <p class="lu-section-lead">Права на код, контент и сделки с объектами ИС.</p>
      </div>
      <div class="lu-grid">
        <a class="lu-card" href="/dogovory/">
          <span class="lu-card-top"><span class="lu-card-num">01</span><span class="lu-card-tag">ГК РФ</span></span>
          <h3 class="lu-card-title">{title_dog}</h3>
          <p class="lu-card-text">Лицензия, франчайзинг, отчуждение, авторский заказ и регистрация распоряжений в Роспатенте.</p>
          <span class="lu-card-more">Подробнее <svg class="lu-ico lu-ico--arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </a>
        <a class="lu-card" href="/registraciya_programm_evm/">
          <span class="lu-card-top"><span class="lu-card-num">02</span><span class="lu-card-tag">ПО и БД</span></span>
          <h3 class="lu-card-title">{title_evm}</h3>
          <p class="lu-card-text">Регистрация программы и базы данных, защита сайта и приложений, сопровождение в Роспатенте.</p>
          <span class="lu-card-more">Подробнее <svg class="lu-ico lu-ico--arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </a>
      </div>
    </section>

""".format(mark=MARK, title_dog=TITLE_DOG, title_evm=TITLE_EVM)

CANDIDATE_NAMES = (
    "lireate-uslugi-cms.inc.php",
    "lireate-uslugi-lib.php",
    "lireate-uslugi-render.php",
)


def cards_already_present(raw):
    if MARK in raw:
        return True
    if TITLE_DOG in raw and TITLE_EVM in raw and "/dogovory/" in raw and "/registraciya_programm_evm/" in raw:
        return True
    if 'id="lu-is-contracts"' in raw or "lu-is-contracts" in raw:
        return True
    return False


def patch_file(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    if cards_already_present(raw):
        return "already"
    contact = CONTACT_SECTION_RE.search(raw)
    if not contact:
        return "no_anchor"
    anchor = contact.group(0)
    out = raw.replace(anchor, CARDS + anchor, 1)
    path.write_text(out, encoding="utf-8")
    return "patched"


def main():
    if len(sys.argv) < 2:
        print("Usage: %s DOCROOT" % sys.argv[0], file=sys.stderr)
        raise SystemExit(2)
    docroot = Path(sys.argv[1])
    uslugi_dir = docroot / "template/page/uslugi"
    found_any = False
    for name in CANDIDATE_NAMES:
        p = uslugi_dir / name
        if not p.is_file():
            continue
        found_any = True
        status = patch_file(p)
        if status == "patched":
            print("PATCHED", p)
            print("USLUGI_CARDS_OK")
            return
        if status == "already":
            print("USLUGI_CARDS_OK already", p.name)
            return
        print("USLUGI_CARDS_SKIP anchor missing in %s" % p, file=sys.stderr)
    if not found_any:
        print("USLUGI_CARDS_SKIP no uslugi template under %s" % uslugi_dir, file=sys.stderr)
    raise SystemExit(0)


if __name__ == "__main__":
    main()
