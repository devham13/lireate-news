# QA: L21 osparivanie-tovarnogo-znaka-v-rospatente

date: 2026-10-30
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, таблица 1493/1500/1512, ol×7, TL;DR blockquote |
| GEO / citability | 25 | 23 | workflow-карта трёх процедур, «Делайте / не делайте», FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 четыре предложения >25 слов |
| Fact safety | 15 | 12 | fact-check WARNING (19 extracted, 2 verified); сверено с research-notes |
| Contract HTML | 10 | 9 | linter PASS, объём ~8.5k ✓; −1 нет `<img>` с alt (cover после cover-агента) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — оспаривание ТЗ в Роспатенте, три процедуры |
| C02 | ✓ | Lead + TL;DR — 1493 / 1500 / 1512-1513 |
| C03 | ✓ | Заявитель, третье лицо, правообладатель |
| C04 | ✓ | ст. 1493, 1500, 1512-1513, 1248; 9 000 / 14 000 ₽ |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Карта → таблица → каналы → 1500 → отличие L08 → 7 шагов → суд |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol, blockquote |
| R01 | ✓ | Standalone блоки в секциях |
| R02 | ✓ | КонсультантПлюс, ГАРАНТ, Поисковая платформа, klerk |
| R03 | ✓ | 4 мес., 9k/14k, 5 лет — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L08 (детальная атака) и ст. 1500 vs 1513 |
| E02 | ✓ | «Делайте / не делайте» |
| E03 | ✓ | CTA защита знака ×1, чек-лист L01 legacy, рубрика category=9 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, дата 30.10.2026 |
| Ept02 | ✗ | Interlink L08 slug отложен (404 на live); L08/L21 WARN в cannibalization |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS (acceptable) | slop-detector-report.json |
| cannibalization | WARNING (acceptable) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 13, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1 (2026-10-30): удалён `<figure>`; fips 403 / rospatent SSL → garant, licensingrussia, klerk; internal slug 404 → legacy чек-лист L01 + consultant вместо L08 slug

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 61.0 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (19 extracted, 2 verified, 17 unverified)
- факты сверены с `research-notes.md` (1493/1500/1512-1513, 9 000 / 14 000 ₽, 4 мес.)
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING — primary L08 ↔ secondary L21 «возражение против регистрации…» 83% (ожидаемо: L21 = карта, L08 = deep dive)
- repo fix: `L18` primary_query уточнён (снят дубликат с L03, CRITICAL)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — правки href и удаление cover `<figure>` в `article.html`
- cycle 2: не требовался

## Optional (не blocker)

- `<img>` с alt после cover-агента
- после publish L08: вернуть interlink на `/vozrazhenie-protiv-registracii-tovarnogo-znaka-sroki-poryadok`

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
