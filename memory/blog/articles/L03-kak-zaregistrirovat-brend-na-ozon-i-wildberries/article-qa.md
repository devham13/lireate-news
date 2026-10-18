# QA: L03 kak-zaregistrirovat-brend-na-ozon-i-wildberries

date: 2026-10-18
score_total: 90/100
core_eeat_lite: 19/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, primary query в lead; таблица сценариев WB/Ozon |
| GEO / citability | 25 | 24 | Answer-first, TL;DR, 3×`<ol>`, workflow-схемы, 7 FAQ |
| CORE-EEAT lite | 15 | 14 | 19/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 четыре длинных предложения (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (7 unverified — сроки модерации WB/Ozon, 180 дней); сверено с research-notes |
| Contract HTML | 10 | 8 | linter PASS, объём 8807 ✓, CTA `/reg-tz-main` ×1 ✓; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 19/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title закрывают проверку бренда на WB/Ozon и роль ТЗ |
| C02 | ✓ | Lead — direct answer, два слоя (справочник vs Роспатент) |
| C03 | ✓ | Селлеры WB/Ozon |
| C04 | ✓ | п. 6 ст. 1483, представительство, «Оригинал» объяснены |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Логичный маршрут проверка → ЛК → документы → календарь |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | table, ol×3, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | WB instruction, КонсультантПлюс, Поисковая платформа |
| R03 | ✓ | Сроки модерации с привязкой к ЛК; календарь 289-ФЗ / ПП 821 |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «два слоя: маркетплейс и ТЗ» |
| E02 | ✓ | Типичные ошибки модерации, «делайте / не делайте» |
| E03 | ✓ | CTA Лирейт `/reg-tz-main` |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | Brief, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения DIY, не юрконсультация |
| Ept02 | ✗ | Internal L01/L02 — live seo_url (не slug из meta); осознанно для production |

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

- total: 7, failed: 0
- site-base: публичный домен Lireate (флаг `--site-base` link-verify)
- fix cycle 1 (2026-10-18): L01/L02 href → live seo_url на хостинге (legacy paths без slug из meta)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 63.7 (Easy / Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (13 extracted, 6 verified, 7 unverified — «р.д.», 100 Кб, 180 дней, 2027)
- источники в research-notes; блокером не является
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 2 internal href на production URL L01/L02
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish: canonical `/kak-zaregistrirovat-brend-na-ozon-i-wildberries` на хостинге

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
