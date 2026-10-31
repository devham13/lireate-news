# QA: L24 sajt-klon-zashchita-brenda-v-internete

date: 2026-10-31
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×10, FAQ 7, таблица×2, ol×9, TL;DR blockquote |
| GEO / citability | 25 | 22 | «Делайте / не делайте», миф РКН, workflow blockquote, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 over-long (7, часть — парсер таблиц) |
| Fact safety | 14 | 11 | fact-check WARNING (9 unverified; сверено с research-notes) |
| Contract HTML | 10 | 10 | linter PASS, cover img×1 с alt, ~8.5k ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — сайт-клон, защита бренда, ТЗ |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Правообладатель с зарегистрированным ТЗ |
| C04 | ✓ | ТЗ, МКТУ, смешение, WHOIS в первых блоках |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Клон vs конкурент → ТЗ → фиксация → адресат → претензия → суд → РКН → workflow |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы×2, ol×9, blockquote×4 |
| R01 | ✓ | Standalone блоки в секциях |
| R02 | ✓ | consultant.ru, cctld.ru, intelight.pro, СИП в research-notes |
| R03 | ✓ | 10 000–5 000 000 ₽, 30 дн., 10 лет — из notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Workflow правообладателя vs DRP/SEO SERP |
| E02 | ✓ | «Делайте / не делайте» в H2 |
| E03 | ✓ | CTA защиты знака, рубрика category=13 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes, угол cctld.ru |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, дата 31.10.2026, миф РКН |
| Ept02 | ✗ | L09/L10 slug 404 на live → plain text + 2 live internal (рубрика, CTA) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING (acceptable, 0 cliches) | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, не L24) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 8, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1 (2026-10-31): убраны href на unpublished slug L09/L10/L02; e.law.ru (302 loop) → текстовая отсылка; удалён `<figure>`, один cover `<p><img>`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 7
- Flesch RU: 51.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (14 extracted, 5 verified, 9 unverified)
- unverified сверены с `research-notes.md` (1515 диапазон, обзор ВС № 4, практика РКН)
- see `fact-check-report.json`

## Cannibalization

- WARNING L08↔L21 (83%) — repo-wide overlap, primary L24 «защита бренда в интернете» не затронут

## GEO QA fixes applied

1. HTML whitelist: без `<figure>`; cover только `<p><img>`.
2. Links: unpublished blog slugs → plain text; e.law.ru без href до стабильного HTTP.

## Gate

**PASS** — директор может запускать cover || schema.
