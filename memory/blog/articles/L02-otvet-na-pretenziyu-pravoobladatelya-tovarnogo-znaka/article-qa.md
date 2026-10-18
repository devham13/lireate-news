# QA: L02 otvet-na-pretenziyu-pravoobladatelya-tovarnogo-znaka

date: 2026-10-18
score_total: 91/100
core_eeat_lite: 19/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×6, FAQ 7, primary query в lead; −2 длина `title` (meta) на грани CTR |
| GEO / citability | 25 | 24 | Answer-first, 2 таблицы, 7 FAQ, blockquote-маршрут, numbered steps |
| CORE-EEAT lite | 15 | 14 | 19/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 два длинных предложения (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (9 unverified — лимиты 10 млн, вторичные даты); сверено с research-notes |
| Contract HTML | 10 | 9 | linter PASS, объём 9108 ✓, CTA Лирейт ×2 ✓; −1 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 19/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title закрывают ответ на претензию по ТЗ |
| C02 | ✓ | Lead — direct answer |
| C03 | ✓ | ИП, ООО, селлеры |
| C04 | ✓ | ст. 1252, 1483, 1487, 1515 объяснены |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Логичный workflow |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | ol, table, blockquote-шаблон |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | КонсультантПлюс, Поисковая платформа, licensingrussia (ФИПС) |
| R03 | ✓ | Лимиты компенсации с 04.01.2026 с ссылкой на ст. 1515 |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «10 дней + без признания вины» |
| E02 | ✓ | «Делайте / не делайте» в H2 |
| E03 | ✓ | Лирейт ×2 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | Brief, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения DIY / не юрконсультация |
| Ept02 | ✗ | Internal L01 — live seo_url (не slug из meta); задумано для post-merge |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |

## Link verify

- total: 8, failed: 0
- fix cycle 1: fips.ru (403) → licensingrussia.ru + plain fips.ru; L01 href → `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (200)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 55.0 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (16 extracted, 7 verified, 9 unverified — компенсация 10 млн, часть дат)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — `<pre>/<code>` → blockquote; ссылки fips + L01; `meta_ab.title_seo` (67 симв., primary_query)
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту (cover/indexer)
- после publish L02: повторить link-verify на canonical

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
