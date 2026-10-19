# QA: L05 sposoby-zashchity-izobreteniya

date: 2026-10-19
score_total: 90/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×6, FAQ 7, сравнительная таблица, отсечение ПСН/миграции в lead |
| GEO / citability | 25 | 23 | TL;DR, workflow blockquote, 3×`<ol>` (13 шагов), 7 FAQ answer-first |
| CORE-EEAT lite | 15 | 13 | 18/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 семь длинных предложений (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (19 unverified — пошлины/сроки вне fact-bank); сверено с research-notes |
| Contract HTML | 10 | 9 | linter PASS, объём ~8800 ✓, CTA `/patent` ×4; −1 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title закрывают сравнение патент / ноу-хау / публикация |
| C02 | ✓ | Lead — direct answer, отличие от ПСН и миграции |
| C03 | ✓ | Стартап, производство, R&D с технологией |
| C04 | ✓ | Патент, КТ, defensive disclosure, ст. 1350/1465/98-ФЗ |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Матрица → таблица → патент → КТ → публикация → неделя |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, 3×ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | ГК РФ, 98-ФЗ, Роспатент searchplatform, Положение о пошлинах |
| R03 | ✓ | 28 000 ₽ и пятилетия поддержания из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол comparison, не дубль L04 (отказ в выдаче) |
| E02 | ✓ | «Делайте / не делайте» и «Сделайте» в секциях |
| E03 | ✓ | Лирейт CTA `/patent` |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | Brief/research, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения DIY, не юрконсультация |
| Ept02 | ✗ | Карточка: `/kommercheskaya-tayna` → live 404; CTA через `/patent` |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING (acceptable) | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 11, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-10-19): rospatent.gov.ru (SSL в CI), fips.ru (403) → КонсультантПлюс (Положение о пошлинах, Регламент ИЗ); internal `/kommercheskaya-tayna` (404) → `/patent`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 7
- Flesch RU: 50.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (24 extracted, 5 verified, 19 unverified)
- источники в research-notes; блокером не является
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 3 href + чеклист/action-маркеры для utility gate
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish: canonical `/sposoby-zashchity-izobreteniya` на хостинге

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
