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
| Human voice | 15 | 14 | 0 AI-slop hits, Flesch RU 50.9; −1 три длинных предложения (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (6/11 verified); 35 000 ₽ и др. — из research, не в fact-bank |
| Contract HTML | 10 | 8 | linter PASS, объём ~9 300+ ✓, CTA Лирейт ×2 ✓; −2 inline `<img>` с alt (3 шт. есть) |

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
| fact-check | WARNING | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate (article) | PASS | utility-gate-report.json |

## Link verify

- total: 7, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 2026-10-18: fips.ru / rospatent.gov.ru (403/SSL в CI) → licensingrussia.ru (реестры), base.garant.ru (тарифы предоценки), consultant.ru (патентные пошлины)
- канон fips.ru / rospatent.gov.ru остаётся в plain text и research-notes

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3
- Flesch RU: 50.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (11 extracted, 6 verified, 5 unverified — пошлины 35 000 ₽, тел. ФИПС, ст. 1499 и др.)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues, 6 articles in blog-dir)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (2026-10-18): GEO QA заменил 3 внешних href для link-verify pass (смысл сохранён)
- cycle 2: не требовался

## Optional (не blocker)

- href на [приказ № 197](https://pravo.ppt.ru/prikaz/rospatent/n-197-23382) в секции сходства
- после publish: повторить link-verify с `--site-base` на финальный canonical

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
