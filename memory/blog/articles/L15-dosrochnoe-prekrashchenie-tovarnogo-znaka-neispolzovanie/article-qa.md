# QA: L15 dosrochnoe-prekrashchenie-tovarnogo-znaka-neispolzovanie

date: 2026-10-22
score_total: 83/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, ol×6, 2 таблицы, blockquote TL;DR + схема сроков + учебный ответ |
| GEO / citability | 25 | 22 | ст. 1486 календарь, таблица СИП/ППС/1515, чек-лист иска, «Делайте / не делайте» |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 slop (4 предложения >25 слов) |
| Fact safety | 15 | 11 | fact-check WARNING (11 extracted, 4 verified); нормы сверены с research-notes |
| Contract HTML | 10 | 5 | linter PASS, объём ~9.2k ✓; −5 нет `<img>` с alt (cover pending) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — иск за неиспользование, ст. 1486, СИП |
| C02 | ✓ | Lead + TL;DR — предложение, 2 мес, 30 дн, бремя на ответчике |
| C03 | ✓ | Предприниматель, юрист бренда, заявитель в Роспатент |
| C04 | ✓ | ст. 1486, 1483, 1512, 1515, 43.4 АК, 125–126 АПК |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Проверка → СИП/ППС → предложение → сроки → заинтересованность → иск → защита ответчика |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, ol×6, blockquote×4 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | zakonrf.info, base.garant.ru, searchplatform.rospatent.gov.ru |
| R03 | ✓ | СИП-60/2025, СИП-593/2025; без выдуманных «чекеров» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол истца по неиспользованию vs ППС (L08) и претензия (L02) |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA legacy L01/L02, рубрика category=9; ≤3 commercial |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 22.10.2026 |
| Ept02 | ✓ | Internal: L01 чек-лист, L02 претензия, /news?category=9 |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | WARNING | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | PASS | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 13, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1: consultant.ru → zakonrf.info / base.garant.ru (таймауты); fips.ru 403 → текст без ссылки; internal L08 404 → убрана до live slug

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 52.2 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (11 extracted, 4 verified, 7 unverified)
- сверка: ст. 1486 (сроки, бремя), 43.4 АК, исковое трёхлетие, СИП-60/593 — `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — внешние НПА на zakonrf/garant; fips без href; internal L08 → текстовое уточнение

## Optional (не blocker)

- `<img>` с alt после cover-агента
- interlink на L08 после публикации slug на lireate.ru

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
