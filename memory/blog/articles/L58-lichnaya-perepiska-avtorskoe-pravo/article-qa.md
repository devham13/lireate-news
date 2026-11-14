# QA: L58 lichnaya-perepiska-avtorskoe-pravo

date: 2026-11-14
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, ol×9, 2 таблицы, режим B, troubleshooting |
| GEO / citability | 25 | 23 | TL;DR три контура, матрица типов сообщений, 9 шагов, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; 4 предложения >25 слов |
| Fact safety | 15 | 12 | fact-check PASS (13 extracted, 2 verified, 11 unverified — НПА в research-notes) |
| Contract HTML | 10 | 9 | linter PASS, ~9k chars |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | Title/H1 — авторское право на переписку, 1259/1270, 152.2, 10.1 |
| C02 | ✓ | Lead + TL;DR — три контура, ст. 1301 с 04.01.2026 |
| C03 | ✓ | Блогеры, бизнес, SMM, бывшие партнёры |
| C04 | ✓ | Consultant ГК, 152-ФЗ, ГПК, Пленум ВС №10, zakonrf GPK |
| O01 | ✓ | H2 = workflow (охрана → контуры → матрица → согласие → анонимизация → суд → КТ → чек-лист → ущерб) |
| O02 | ✓ | Матрица 6×5, ol 9 шагов, blockquote-схема |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, blockquote×3 |
| R01 | ✓ | «Делайте / не делайте» в ключевых секциях |
| R02 | ✓ | consultant, garant 98-ФЗ, kremlin, zakonrf, live legacy interlink |
| R03 | ✓ | research-notes / fact-check |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от legacy обзора `/rasprostranyaetsya_li_avtorskoe_pravo_na_perepisku/` |
| E02 | ✓ | Три контура до публикации, суд вместо ленты |
| E03 | ✓ | CTA мессенджеры; interlink претензия (legacy L02 URL) |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 14.11.2026, не юруслуга |
| Ept02 | ✗ | Slug L14/L13/L02 ещё 404 на live — interlink на Garant/zakonrf/legacy; после publish indexer вернёт slug |

## Script reports

| Скрипт | Verdict | exit | Файл |
|--------|---------|------|------|
| fact-check | PASS | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | PASS (0 clichés) | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo-level; не L58) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 18, failed: 0
- site-base: env `LIREATE_PUBLIC_SITE_URL` (публичный домен Lireate)

## GEO QA fixes applied (fix cycle 1, 2026-11-14)

1. `/rezhim-kommercheskoj-tajny-kak-vvesti/` (L14 → 404) → Garant ст. 10 98-ФЗ (×3).
2. `/mozhno-li-publikovat-foto-kartin-hudozhnika/` (L13 → 404) → zakonrf ст. 1270 (×1).
3. `/otvet-na-pretenziyu-pravoobladatelya-tovarnogo-znaka/` (slug L02 → 404) → legacy `/otvet_na_pretenziyu_…` (×2).

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 57.1 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (13 extracted, 2 verified, 11 unverified)
- unverified: нормы и суммы сверены вручную по consultant/garant в research-notes

## Cannibalization

- WARNING на уровне репозитория (пересечения L03/L59, L08/L21 и др.); primary L58 не в списке конфликтов.

## Post-publish

- Indexer: вернуть interlink на slug L14, L13, L02 после live-публикации материалов.