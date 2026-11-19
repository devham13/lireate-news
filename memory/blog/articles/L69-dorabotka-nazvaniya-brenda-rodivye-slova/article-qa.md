# QA: L69 dorabotka-nazvaniya-brenda-rodivye-slova

date: 2026-11-19
score_total: 85/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, ol×9, 3 таблицы, blockquote TL;DR; cover + 2 inline |
| GEO / citability | 25 | 23 | сценарий «трава», таблицы антипаттернов/маршрута, «Делайте/не делайте» |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 slop hits; −2 за 4 предложения >25 слов |
| Fact safety | 15 | 13 | fact-check PASS (5/5 verified); дисклеймер 19.11.2026 |
| Contract HTML | 10 | 8 | linter PASS, ~8.6k знаков; img cover+inline с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — доработка имени, п. 1/6 ст. 1483 |
| C02 | ✓ | Lead + TL;DR — прямой ответ, без «в этой статье» |
| C03 | ✓ | Маркетинг, заявитель ТЗ, предприниматель с брендом |
| C04 | ✓ | МКТУ, различительная способность, неохраняемый элемент |
| O01 | ✓ | H2 = research action outline |
| O02 | ✓ | п. 1 → виды слов → сценарий → приёмы → антипаттерны → п. 6 → МКТУ → чек-лист |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 3 таблицы, нумерованный чек-лист, blockquote×3 |
| R01 | ✓ | Standalone в FAQ и табличных блоках |
| R02 | ✓ | consultant, tm-patent, searchplatform, research-notes |
| R03 | ✓ | Тариф 46 200 ₽ → garant; без выдуманных процентов |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «родовое ядро + troubleshooting до экспертизы» |
| E02 | ✓ | «Делайте/не делайте» в каждой H2 |
| E03 | ✓ | CTA `/reg-tz-main`; ≤3 commercial |
| Exp01 | ✓ | Режим B (учебный сценарий) |
| Exp02 | ✓ | research-notes, сценарий «трава» |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, без гарантий регистрации |
| Ept02 | ✓ | L64, L06 (live slug), L48, L29, `/reg-tz-main` |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | PASS (L69 not flagged) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 16, failed: 0
- site-base: `https://example.com`, `--timeout 25`
- fix cycle 1 (GEO QA): `/kak-opredelit-klass-mktu/` → `/struktura_mktu_kak_opredelit_klass_dlya_tovara_i_uslugi/`; rospatent.gov.ru/fips.ru (SSL/403 в Cloud) → L48/L29/licensingrussia/base.garant.ru

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 50.0 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (5 extracted, 5 verified)
- see `fact-check-report.json`

## Cannibalization

- L69 not in `issues[]`; repo-level warnings only (other topics)

## Utility gate

- article PASS: 9 list items, 8 H2, 7 FAQ, 3 tables, 13 action markers
- see `utility-gate-report.json`