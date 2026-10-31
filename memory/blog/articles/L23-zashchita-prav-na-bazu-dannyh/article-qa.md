# QA: L23 zashchita-prav-na-bazu-dannyh

date: 2026-10-31
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×10, FAQ 7, таблица×1, ol×7, TL;DR blockquote |
| GEO / citability | 25 | 22 | БД vs ПДн vs КТ, «Делайте / не делайте», FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 шесть over-long (часть — артефакт парсера таблицы) |
| Fact safety | 14 | 12 | fact-check WARNING (12 unverified; сверено с research-notes) |
| Contract HTML | 10 | 10 | linter PASS, img×4 с alt, ~9.4k ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — защита прав на БД, изготовитель, нарушение |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Владелец каталога / SaaS с подрядчиком |
| C04 | ✓ | ст. 1260, 1333–1334, 152-ФЗ, 1311 в первых блоках |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Три режима → слои → изготовитель → затраты → 7 шагов → регистрация → enforcement → КТ |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol×7, blockquote, img placeholders |
| R01 | ✓ | Standalone блоки в секциях |
| R02 | ✓ | КонсультантПлюс, kremlin.ru, klerk 333.30, ЕПГУ |
| R03 | ✓ | 5 000 ₽, 62 дн., 10 000 элементов — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «ИС на БД vs 152-ФЗ» vs SERP |
| E02 | ✓ | «Делайте / не делайте» в H2 |
| E03 | ✓ | L14 plain text, рубрика category=17 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, дата 31.10.2026 |
| Ept02 | ✗ | Slug L14 404 на live → plain text до publish |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING (acceptable, 0 cliches) | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, не L23) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 10, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL` (флаг `--site-base` при verify)
- fix cycle 1 (2026-10-31): rospatent.gov.ru (SSL) → `gosuslugi.ru`; internal L14 404 → plain text; `<figure>`/`<figcaption>` → `<p><img>` + `<p><i>` caption

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 6
- Flesch RU: 47.3 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (15 extracted, 3 verified, 12 unverified)
- unverified сверены с `research-notes.md` (1311 диапазон, 1 300 ₽ дубликат, 62 дн.)
- see `fact-check-report.json`

## Cannibalization

- WARNING L08↔L21 (83%) — известный repo-wide overlap, L23 primary «защита прав на базу данных» не затронут

## GEO QA fixes applied

1. HTML whitelist: cover + inline collage без `<figure>`.
2. Links: ЕПГУ вместо rospatent.gov.ru; L14 без href до live slug.

## Gate

**PASS** — директор может запускать cover || schema.
