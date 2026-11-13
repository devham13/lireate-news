# QA: L55 logotipy-kompaniy-v-video-soglasie

date: 2026-11-13
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, матрица форматов, ol×9, режим B |
| GEO / citability | 25 | 23 | TL;DR три контура, blockquote workflow, таблица рисков, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; 3 предложения >25 слов (артефакт таблиц в slop) |
| Fact safety | 15 | 12 | fact-check PASS (1 verified, 11 unverified — статьи ГК/дело в research-notes) |
| Contract HTML | 10 | 9 | linter PASS, ~8.6k; cover `<img>` placeholder |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — логотипы в видео, ТЗ, дизайн, добросовестность |
| C02 | ✓ | Lead + TL;DR — 1484, 1270, ФЗ о рекламе, 14.3, L17 |
| C03 | ✓ | Монтажёр, продакшн, корпоративное видео |
| C04 | ✓ | 1484, 1487, 1489, 1270, 1515 с 04.01.2026, дело А40-64050/2019 |
| O01 | ✓ | H2 = research action_outline (3 контура, матрица, чек-лист) |
| O02 | ✓ | Классификация → ТЗ → © → матрица → 9 шагов → согласие → правки → претензия |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, ol, blockquote |
| R01 | ✓ | Standalone «Делайте / не делайте» в секциях |
| R02 | ✓ | КонсультантПлюс, Поисковая платформа, kremlin.ru, it-lex, rb.ru |
| R03 | ✓ | research-notes / fact-check |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка L17 (превью), L09 (реклама), L02 (претензия) |
| E02 | ✓ | «Делайте / не делайте» по контурам |
| E03 | ✓ | CTA TG/WA/MAX; interlink L09, L17, L01, L02, L27 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 13.11.2026, не юрконсультация |
| Ept02 | ✗ | utility gate WARN: «можно»/«использовать» не в title_seo (есть в title_aeo/lead) |

## Script reports

| Скрипт | Verdict | exit | Файл |
|--------|---------|------|------|
| fact-check | PASS | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, L22↔L36, L34↔L38; не L55) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 22, failed: 0
- site-base: публичный домен Lireate (`LIREATE_PUBLIC_SITE_URL`)

## GEO QA fixes applied (fix cycle 1, 2026-11-13)

1. CTA MAX: deep-link `max.ru/u/…` (403 в Cloud) → `https://max.ru/` (как L45/L46).

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3
- Flesch RU: 59.8 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (12 extracted, 1 verified, 11 unverified)
- нормы ГК и кейс А40-64050/2019 сверены с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING at repo level only; L55 vs L17 — разные intent (чек-лист монтажа vs превью/обложки)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — max.ru CTA
- cycle 2: не требовался

## Optional (не blocker)

- `meta_ab.title_seo`: добавить «можно использовать» для parity с primary_query
- cover `cover/cover.png` — после cover-агента

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
