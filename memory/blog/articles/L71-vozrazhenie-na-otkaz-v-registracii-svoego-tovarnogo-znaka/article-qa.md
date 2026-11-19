# QA: L71 vozrazhenie-na-otkaz-v-registracii-svoego-tovarnogo-znaka

date: 2026-11-19
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 6, ol×12, 1 таблица, blockquote TL;DR; cover ещё нет |
| GEO / citability | 25 | 23 | workflow 9 шагов, таблица документов, границы L07/L53, «Делайте/не делайте» |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 slop hits; −2 за 4 предложения >25 слов |
| Fact safety | 15 | 12 | fact-check WARNING (18 unverified в fact-bank; сверено с research-notes, consultant/garant) |
| Contract HTML | 10 | 9 | linter PASS, ~8.7k знаков; img cover/inline — после cover |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — возражение на отказ, ст. 1500 |
| C02 | ✓ | Lead + TL;DR — прямой ответ, уведомление vs решение |
| C03 | ✓ | Заявитель своей заявки, предприниматель/маркетолог |
| C04 | ✓ | ППС, МКТУ, 2.28.2, п. 2 ст. 1500 |
| O01 | ✓ | H2 = research action outline |
| O02 | ✓ | отличие этапов → сроки → пошлина → ППС → подача → ошибки → чек-лист |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | таблица, ol×12, blockquote×3, ul типичных ошибок |
| R01 | ✓ | Standalone в FAQ и таблице |
| R02 | ✓ | consultant, garant, searchplatform, research-notes |
| R03 | ✓ | 9 000/6 000/5 000 ₽ по research; klerk + канон rospatent.gov.ru в тексте |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «заявитель после решения, не L53» |
| E02 | ✓ | «Делайте/не делайте» в ключевых H2 |
| E03 | ✓ | CTA `/registraciya_tovarnogo_znaka/`; ≤3 commercial |
| Exp01 | ✓ | Режим B (workflow) |
| Exp02 | ✓ | research-notes, календарь 2+4 мес. |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 19.11.2026, без гарантий регистрации |
| Ept02 | ✓ | L07, L48, L39, L53; граница с L08 (overlap 71% — осознанно) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | WARNING (acceptable) | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo-level; L71 vs L08 71%) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 14, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, timeout default
- fix cycle 1 (GEO QA): rospatent.gov.ru/dues (SSL) → klerk.ru/patent24; fips.ru (403) → patent-family ППС, garant Правила, online.rospatent ЛК

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 51.2 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (22 extracted, 4 verified in fact-bank)
- manual: сроки 4/6 мес., пошлины 2.28.x, п. 2 ст. 1500 — research-notes + НПА
- see `fact-check-report.json`

## Cannibalization

- WARN: primary overlap L71 ↔ L08 (71%) — разные intent (своя заявка / ст. 1500 vs чужая регистрация / ст. 1512)
- L71 not blocking; см. `cannibalization-report.json`

## Utility gate

- article PASS: 12 list items, 9 H2, 6 FAQ, 1 table, 9 action markers
- see `utility-gate-report.json`