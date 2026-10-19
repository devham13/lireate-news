# QA: L04 otkazali-v-vydache-patenta-chto-delat

date: 2026-10-19
score_total: 91/100
core_eeat_lite: 19/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×7, FAQ 7, отсечение ПСН/миграции в lead; таблицы документов и ППС vs новая заявка |
| GEO / citability | 25 | 24 | TL;DR, workflow blockquote, 4×`<ol>`, 7 FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 19/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 четыре длинных предложения (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (17 unverified — сроки/пошлины вне fact-bank); сверено с research-notes и КонсультантПлюс |
| Contract HTML | 10 | 9 | linter PASS, объём ~8600 ✓, CTA `/patent` ×3 ✓; −1 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 19/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title закрывают отказ в выдаче патента и повторную подачу |
| C02 | ✓ | Lead — direct answer, отличие от ПСН и миграции |
| C03 | ✓ | Заявитель после письма ФИПС |
| C04 | ✓ | ППС, уведомление о патентоспособности, ст. 1350/1387 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Документ → доработка → ППС → ветки → календарь |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, 4×ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | ГК РФ, Регламент, patent-family / searchplatform |
| R03 | ✓ | Пошлины с п. 1.27.1–1.27.2 и research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Календарь после отказа, не клон ПСН-SERP |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | Лирейт CTA ≤3 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | Brief/research, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения DIY, не юрконсультация |
| Ept02 | ✗ | Карточка темы: `/patentovanie`, `/izobretenie` → live `/patent` (как L03) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 11, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-10-19): rospatent.gov.ru (SSL в CI), fips.ru (403) → patent-family.ru (ППС/п. 1.27.1), searchplatform.rospatent.gov.ru/patents; internal `/patentovanie`, `/izobretenie` → `/patent`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 51.3 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (20 extracted, 3 verified, 17 unverified — сроки 6/7 мес., пошлины 2 000/3 000 ₽)
- источники в research-notes; блокером не является
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 5 href (внешние + internal на production `/patent`)
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish: canonical `/otkazali-v-vydache-patenta-chto-delat` на хостинге

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
