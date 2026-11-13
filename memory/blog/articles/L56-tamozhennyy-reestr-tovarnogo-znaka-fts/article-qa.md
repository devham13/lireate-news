# QA: L56 tamozhennyy-reestr-tovarnogo-znaka-fts

date: 2026-11-13
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, ol×18 (пакет+workflow), 3 таблицы, режим B |
| GEO / citability | 25 | 23 | TL;DR сроки 2/3 года, blockquote контуры, матрица реестров, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; 7 предложений >25 слов (артефакт таблиц в slop) |
| Fact safety | 15 | 12 | fact-check PASS (2 verified, 14 unverified — НПА в research-notes) |
| Contract HTML | 10 | 9 | linter PASS, ~8.7k chars; cover `<img>` placeholder |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | Title/H1 — ТРОИС, включение ТЗ, контрафакт, страховка |
| C02 | ✓ | Lead + TL;DR — ст. 124 ТК ЕАЭС, 328/334 289-ФЗ, 1487 ГК |
| C03 | ✓ | Правообладатель ТЗ, импортёр, ВЭД |
| C04 | ✓ | 289-ФЗ 328–334, 112, ТК ЕАЭС 124, ГК 1252/1487, Приказ № 131 |
| O01 | ✓ | H2 = workflow research (проверка → контур → пакет → подача → страховка → срок → меры) |
| O02 | ✓ | Двухконтурная таблица, этапы ФТС, 9 шагов workflow |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 3 таблицы, ol×2, blockquote×3 |
| R01 | ✓ | «Делайте / не делайте» в секциях |
| R02 | ✓ | consultant.ru, gosuslugi, tks.ru (реестр), L31/L27 interlink |
| R03 | ✓ | research-notes / fact-check |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка L31 (патент vs ТЗ), L22 (маркировка), L27 (МП) |
| E02 | ✓ | «Делайте / не делайте» по контурам и срокам |
| E03 | ✓ | CTA TG/WA/MAX; interlink L01, L30, L31, L27, L22 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 13.11.2026, не юрконсультация |
| Ept02 | ✗ | utility gate OK; primary_query полнее в meta_ab.title_aeo, чем title_seo |

## Script reports

| Скрипт | Verdict | exit | Файл |
|--------|---------|------|------|
| fact-check | PASS | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | WARNING (0 clichés) | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, L22↔L36, L34↔L38; не L56) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 17, failed: 0
- site-base: публичный домен Lireate (`--site-base`, `LIREATE_PUBLIC_SITE_URL`)

## GEO QA fixes applied (fix cycle 1, 2026-11-13)

1. L31: hyphen-slug → live underscore path `/mozhno_li_zapretit_vvoz_analoga_zapatentovannogo_tovara/` (×2).
2. Реестр ФТС: `customs.gov.ru` (SSL timeout в Cloud) → `https://www.tks.ru/db/ois/` (как L31; ×2).

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 7
- Flesch RU: 64.4 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (16 extracted, 2 verified, 14 unverified)
- сроки 3 года (ТРОИС) vs 2 года (ЕАЭС), страховка 500 000 ₽ — в research-notes
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING at repo level only; L56 vs L31 — разные intent (workflow ТЗ в ТРОИС vs патент/параллельный импорт)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — L31 slug + TKS reestr links
- cycle 2: не требовался

## Optional (не blocker)

- `meta_ab.title_seo`: добавить «включение» для parity с primary_query
- cover `cover/cover.png` — после cover-агента

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
