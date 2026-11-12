# QA: L49 registraciya-tovarnogo-znaka-na-fizicheskoe-lico

date: 2026-11-12
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, таблица ФЛ/ИП/ООО, 3×ol, режим B |
| GEO / citability | 25 | 23 | TL;DR, дерево решений, таблица, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop; −2 пять длинных предложений (>25 слов) |
| Fact safety | 15 | 13 | fact-check PASS (3/15 auto-verified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, ~8583 знаков; cover `<img>` placeholder (cover-агент) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — ФЛ vs ИП vs ООО, правообладатель |
| C02 | ✓ | Lead + TL;DR — 193-ФЗ, 35 000 ₽, передача в ООО |
| C03 | ✓ | Второе лицо, предприниматель/самозанятый/учредитель |
| C04 | ✓ | 193-ФЗ, ст. 1491–1514, 35 000 ₽, 15 000 ₽ п. 3.11 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Матрица → сценарии → подача → передача → чек-лист |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, blockquote, ol×3 |
| R01 | ✓ | Standalone блоки в FAQ и таблице |
| R02 | ✓ | Госуслуги, Consultant, kremlin.ru, searchplatform |
| R03 | ✓ | Даты/суммы из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L30 (подача) и L41 (отчуждение) |
| E02 | ✓ | «Делайте / не делайте» в теле |
| E03 | ✓ | CTA `/registraciya_tovarnogo_znaka/` ×2, interlink L30/L41 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, без гарантий регистрации |
| Ept02 | ✗ | L19 interlink → legacy URL до publish slug L19 |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS (acceptable) | slop-detector-report.json |
| cannibalization | PASS (L49 не в issues) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 13, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-11-12): rospatent.gov.ru SSL ×7 → gosuslugi.ru; L19 slug 404 → legacy `/chto_delat_esli_tovarnyiy_znak_zanyat/`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 57.1 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (15 extracted, 3 verified, 12 unverified)
- факты сверены с `research-notes.md` (193-ФЗ, 35 000 ₽, 15 000 ₽, 10 лет)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues с участием L49)
- repo-wide WARNING (L34/L38, L08/L21, L22/L36) — не blocker
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 8 правок href в `article.html`
- cycle 2: не требовался

## Optional (не blocker)

- после publish L19: canonical `/chto-delat-esli-tovarnyy-znak-zanyat/`
- cover `cover.png` — excalibur-blog-cover

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
