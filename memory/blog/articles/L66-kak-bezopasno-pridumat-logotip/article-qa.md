# QA: L66 kak-bezopasno-pridumat-logotip

date: 2026-11-18
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, таблица×1, ol×9, TL;DR blockquote |
| GEO / citability | 25 | 23 | Пять слоёв, схема в blockquote, чек-лист 9 шагов, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop; Flesch 54.7; 6 предложений >25 слов (WARNING slop) |
| Fact safety | 14 | 11 | fact-check PASS; 4/13 verified; нормы ГК сверены с research-notes |
| Contract HTML | 12 | 12 | linter PASS, char_count 8698, TOC в теле нет |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — безопасный логотип, АП и ТЗ |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Предприниматель до первого тиража |
| C04 | ✓ | 1225, 1259, 1234, 1270, 1288, 1477, 1483, 1301 в первых блоках |
| O01 | ✓ | H2 по research action_outline (5 слоёв) |
| O02 | ✓ | © vs ® → автор → реестр → шрифт → ФИПС → 1483 → ol → папка → CTA |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol×9, blockquote×3 |
| R01 | ✓ | «Делайте / не делайте» в секциях |
| R02 | ✓ | Consultant, ГАРАНТ, TypeType, ParaType, L11/L39/L64 live paths |
| R03 | ✓ | 11.12.2023 ФИПС, 10 000–10 000 000 ₽ — research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «чек-лист до тиража» vs L11 договор, L39 доработка, L64 нейминг |
| E02 | ✓ | Реестр элементов и папка доказательств в каждом слое |
| E03 | ✓ | Telegram CTA; backlinks L11/L39/L64 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 18.11.2026 |
| Ept02 | ✗ | Primary близок к L11/L34 по «логотип» — разведение через «безопасно/до тиража» |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | WARNING | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (legacy-пары; L66 не в списке) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 16, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix (GEO QA cycle 1): внутренние L11/L64 → live `seo_url` с подчёркиваниями (`dogovor_na_razrabotku_logotipa_kak_poluchit_prava_ot_dizaynera`, `nejming_i_logotip_soglasovanie`)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 6
- Flesch RU: 54.7 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (13 extracted, 4 verified, 9 unverified)
- unverified: статьи ГК, суммы 1301 — сверено с `research-notes.md` и Consultant
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (7 cross-topic warnings в репо; primary L66 «как безопасно придумать логотип» не конфликтует с L11/L34 в отчёте)
- **L66-specific:** acceptable (handoff к L11/L39/L64 в тексте)
- see `cannibalization-report.json`

## GEO QA edits

- `article.html`: internal L11/L64 paths → live underscore `seo_url` (404 на slug-with-dashes)