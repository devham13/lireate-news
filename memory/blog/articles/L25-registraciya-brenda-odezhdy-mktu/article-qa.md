# QA: L25 registraciya-brenda-odezhdy-mktu

date: 2026-10-31
score_total: 85/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, таблицы×3, ol×8, TL;DR blockquote |
| GEO / citability | 25 | 22 | матрица 25/35/24, «Делайте / не делайте», маршрут blockquote, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 over-long (7) |
| Fact safety | 14 | 11 | fact-check PASS (5 verified, 10 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, ~9.4k ✓; −1 нет `<img>` с alt (cover после cover-агента) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — бренд одежды, МКТУ, маркетплейсы |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Селлер/бренд одежды с собственной маркой |
| C04 | ✓ | МКТУ 25/35, ТЗ, бирка в первых блоках |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Кабинет vs Роспатент → классы → тип знака → ПО → поиск → перечень → маршрут → WB → next steps |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы×3, ol×8, blockquote×3 |
| R01 | ✓ | Standalone блоки в секциях |
| R02 | ✓ | consultant.ru, searchplatform, pravo.ppt.ru, klerk.ru |
| R03 | ✓ | 35 000 / 38 500 ₽, 10 лет, 10 дн. WB — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «матрица для одежды» vs SERP «запуск бренда» |
| E02 | ✓ | «Делайте / не делайте» в H2 |
| E03 | ✓ | reg-tz-main ×1, L01 чек-лист, рубрика category=13 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes, SERP-пробел |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не патентная консультация, дата 31.10.2026 |
| Ept02 | ✗ | Slug L03/L06 404 на live → WB instruction + классификатор МКТУ (вернуть internal после publish) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING (acceptable, 0 cliches) | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, не L25) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 13, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1 (2026-10-31): rospatent.gov.ru (SSL/403) → pravo.ppt.ru, klerk.ru, gosuslugi.ru, online.rospatent; internal L03/L06 404 → seller.wildberries + seller-edu.ozon.ru; pro.wildberries → seller instruction

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 7
- Flesch RU: 54.6 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (15 extracted, 5 verified, 10 unverified)
- unverified сверены с `research-notes.md` (пошлины, классы, этапы)
- see `fact-check-report.json`

## Cannibalization

- WARNING L08↔L21 (83%) — repo-wide overlap, primary L25 «бренд одежды МКТУ» не затронут

## GEO QA fixes applied

1. Links: unpublished slug L03/L06 → внешние инструкции маркетплейсов и классификатор МКТУ-13.
2. Links: rospatent.gov.ru / fips MKTU / pro.wildberries → рабочие зеркала и seller.wildberries.

## Gate

**PASS** — директор может запускать cover || schema.
