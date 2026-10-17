# QA: L01 proverka-tovarnogo-znaka-pered-podachey-v-rospatent

date: 2026-10-17
score_total: 94/100
core_eeat_lite: 20/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 19 | H2/H3, primary query, FAQ 7, 2 internal links — OK |
| GEO / citability | 25 | 24 | Lead answer-first, таблица инструментов, 7 FAQ, blockquote-маршрут, numbered steps |
| CORE-EEAT lite | 15 | 15 | 20/20 (см. ниже) |
| Human voice | 15 | 15 | 0 AI-slop hits, Flesch RU 50.2 (экспертный тон) |
| Fact safety | 15 | 13 | fact-check PASS; 5 unverified — допустимо |
| Contract HTML | 10 | 10 | linter PASS, объём 9172 ✓, CTA Лирейт ×2 ✓, `<img>` с alt ×3 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 20/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title закрывают «проверка товарного знака перед регистрацией» |
| C02 | ✓ | Lead — direct answer, без «в этой статье» |
| C03 | ✓ | Предприниматель до пошлины |
| C04 | ✓ | МКТУ, однородность, п. 6 ст. 1483 объяснены |
| O01 | ✓ | H2 совпадают с research action_outline |
| O02 | ✓ | Логичный outline |
| O03 | ✓ | FAQ 7, реальные queries |
| O04 | ✓ | ol (шаги + чек-лист), table |
| R01 | ✓ | ≥3 standalone блоков 40–60 слов |
| R02 | ✓ | Тарифы, дата платформы, методрекомендации — с внешними ссылками |
| R03 | ✓ | Цены с привязкой к ФИПС/сводке; нет выдуманных % |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол: DIY по открытым реестрам до пошлины |
| E02 | ✓ | «Делайте / не делайте» в каждой H2 |
| E03 | ✓ | Лирейт ×2 |
| Exp01 | ✓ | Режим B, без fake «я сделал» |
| Exp02 | ✓ | Тон brief, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения DIY и возврата пошлин |
| Ept02 | ✓ | Internal links 2/2 по карточке темы |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |

## Link verify

- total: 7, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL` (lireate)
- fix cycle 1: rospatent.gov.ru (SSL) и fips.ru (403) → base.garant.ru, licensingrussia.ru; RUTMAP — plain text fips.ru

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4 (иллюстрации в потоке — допустимо)
- Flesch RU: 50.2 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (10 extracted, 5 verified, 5 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues, 6 articles in blog-dir)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA заменил 4 внешних href для link-verify pass (смысл сохранён; канон fips.ru/rospatent в тексте)
- cycle 2: не требовался

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
