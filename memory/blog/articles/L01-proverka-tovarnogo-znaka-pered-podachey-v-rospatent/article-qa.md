# QA: L01 proverka-tovarnogo-znaka-pered-podachey-v-rospatent

date: 2026-10-18
score_total: 92/100
core_eeat_lite: 20/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 19 | H2/H3, primary query, FAQ 7, 2 internal links — OK; −1 длина title/meta на грани CTR |
| GEO / citability | 25 | 24 | Lead answer-first, таблица инструментов, 7 FAQ, blockquote-маршрут, numbered steps |
| CORE-EEAT lite | 15 | 15 | 20/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 три длинных предложения (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (8 unverified — пошлины/«3–5 лет» вне fact-bank); смысл сверен с research-notes |
| Contract HTML | 10 | 8 | linter PASS, объём 9596 ✓, CTA Лирейт ×2 ✓; −2 нет `<img>` с alt |

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
| O04 | ✓ | ol (шаги + чек-лист 18 пунктов), table |
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
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |

## Link verify

- total: 8, failed: 0
- site-base: публичный домен Lireate (флаг `--site-base` link-verify)
- fix cycle 1 (2026-10-18): rospatent.gov.ru (SSL в CI), fips.ru (403) → klerk.ru (пошлины), base.garant.ru (сервисы/тарифы), licensingrussia.ru (реестры); канон fips.ru/rospatent.gov.ru в plain text

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3
- Flesch RU: 52.4 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (14 extracted, 6 verified, 8 unverified — пошлины 4k/1k/13k, «3–5 лет»)
- источники в research-notes; блокером не является
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — замена 4 внешних href + FAQ без ссылки на fips.ru/registers-web (plain text)
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish: повторить link-verify на production canonical

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
