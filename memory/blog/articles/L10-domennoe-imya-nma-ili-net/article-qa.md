# QA: L10 domennoe-imya-nma-ili-net

date: 2026-10-21
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, 3 таблицы, ol×9, blockquote workflow |
| GEO / citability | 25 | 23 | TL;DR, таблица п. 4, сценарии учёта, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 пять предложений >25 слов |
| Fact safety | 15 | 12 | fact-check WARNING (10 unverified; сверено с research-notes) |
| Contract HTML | 10 | 8 | linter PASS, объём ~8.5k ✓; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — домен, НМА, ФСБУ 14/2022 |
| C02 | ✓ | Lead + TL;DR — п. 4, 08/26/97, L01 |
| C03 | ✓ | Бухгалтер + владелец сайта |
| C04 | ✓ | ФСБУ 14/2022, 26/2020, 149-ФЗ, 1484, НК 256/264, Положение КЦ |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Признаки → объект → проводки → НУ → защита → чек-лист → дальше |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | Consultant, ГАРАНТ, klerk, IPBR, cctld |
| R03 | ✓ | 14 дней досудебных ограничений, 100k НК — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L01 (ТЗ) и L09 (реклама) |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA L01, рубрика ТЗ, защита в сети |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не аудит/юруслуга, без «всегда НМА» |
| Ept02 | ✗ | minfin.gov.ru 403 в CI link-verify (заменены на consultant) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS (acceptable) | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 16, failed: 0
- site-base: публичный домен Lireate (`--site-base`, timeout 25s)
- fix cycle 1 (2026-10-21): minfin.gov.ru 403 → `cons_doc_LAW_419062`; SIC/minfin → `LAW_363409`; glavbukh 302 loop → klerk.ru 643209

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 59.7 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (14 extracted, 4 verified, 10 unverified)
- факты сверены с `research-notes.md` (ФСБУ 14 п. 4, продление, КЦ 14 дней, ст. 1484)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 5 правок href в `article.html` (minfin×3, minfin SIC, glavbukh)
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
