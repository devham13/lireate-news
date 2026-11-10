# QA: L50 prodazha-tovarnogo-znaka-dogovor-nalogi

date: 2026-11-10
score_total: 86/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×9, FAQ 7, таблицы продажа/лицензия и налоги, workflow blockquote |
| GEO / citability | 25 | 22 | TL;DR, ol, 2 таблицы, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 18/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 три предложения >25 слов |
| Fact safety | 15 | 12 | fact-check PASS; 12 unverified в bank — сверено с research-notes |
| Contract HTML | 10 | 9 | linter PASS, ~9124 символов; −1 нет `<img>` с alt (ожидается после cover) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — продажа, отчуждение, налоги, Роспатент |
| C02 | ✓ | Lead + TL;DR — ст. 1488–1490, 1234 п. 4, п. 3.11 15 000 ₽ |
| C03 | ✓ | Продавец бренда, покупатель бизнеса, ИП/ООО, налоговые режимы |
| C04 | ✓ | Продажа vs лицензия vs новая заявка; отсылка L41 |
| O01 | ✓ | Workflow «продать товарный знак» из research |
| O02 | ✓ | Развилка → due diligence → цена → покупатель → договор → налоги → 3.11 → хвосты |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote-workflow |
| R01 | ✓ | Цитируемые нормы и цифры по секциям |
| R02 | ✓ | Consultant ГК/НК, klerk, searchplatform, online.rospatent, GARANT |
| R03 | ✓ | 15 000/13 000 ₽, 68/45 дн., ставки НДС/НДФЛ — research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол коммерции + налоги, юрмеханика — L41 |
| E02 | ✓ | «Делайте / не делайте» в налоговой и подаче |
| E03 | ✓ | CTA `/reg-tz-main` ×2; interlink L41, L47, L30, L19, L40 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 10.11.2026, не юр/налог консультация |
| Ept02 | ✗ | Canonical L50 ещё не на хостинге (до publish) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | WARNING (repo-wide, L50 не в issues) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 18, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-11-10): L47/L19 → `lireate_seo_url` с подчёркиваниями; rospatent dues/state (SSL) → klerk + online.rospatent; fips PDF 403 → GARANT

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3 (одно артефакт таблицы в тексте детектора)
- Flesch RU: 53.3 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (16 extracted, 4 verified in bank, 12 unverified)
- пошлины 3.11, сроки АР 371, ст. 1488–1490 — сверены с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (4 issues между другими L-статьями; L50 не затронут)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 5 битых href (L47/L19 slug, rospatent SSL ×2, fips 403) — правки в `article.html`
- cycle 2: не требовался

## Optional (не blocker)

- inline `<img>` после cover
- после publish: canonical 200 на хостинге

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
