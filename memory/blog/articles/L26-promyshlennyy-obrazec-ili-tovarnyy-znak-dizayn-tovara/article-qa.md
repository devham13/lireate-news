# QA: L26 promyshlennyy-obrazec-ili-tovarnyy-znak-dizayn-tovara

date: 2026-11-01
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, таблица×1, ol×8, TL;DR blockquote |
| GEO / citability | 25 | 23 | таблица ПО vs ТЗ, workflow blockquote, «Делайте / не делайте», FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 over-long (4) |
| Fact safety | 14 | 11 | fact-check PASS (6 verified, 15 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, ~9.2k ✓; −1 нет `<img>` с alt (cover после cover-агента) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — защита дизайна, ПО vs ТЗ |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Селлер/бренд с уникальной формой упаковки |
| C04 | ✓ | ПО, объёмный ТЗ, ст. 1352/1483 в первых блоках |
| O01 | ✓ | H2 = comparison + маршрут из research |
| O02 | ✓ | форма vs знак → ст. 1352 → п. 4 1483 → таблица → сценарии → маршрут → бюджет → next steps |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица×1, ol×8, blockquote×4 |
| R01 | ✓ | Standalone блоки в H2-секциях |
| R02 | ✓ | consultant.ru, gosuslugi, pravo.ppt.ru, gorodissky |
| R03 | ✓ | 15 000 ₽, 25/10 лет, 12 мес. — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «форма ≠ логотип» + dual-track заявок vs SERP «что выбрать» |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | `/patent`, `/reg-tz-main`, L01/L25/L03 live slug |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes, SERP-пробел MP до заявки |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не патентная консультация, дата 01.11.2026 |
| Ept02 | ✗ | L05 slug на live 404 → `/patent` (услуга патентования); после publish L05 вернуть canonical |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| html-linter | PASS | 0 | html-linter-report.json |
| link-verify | PASS | 0 | link-verify.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, не L26) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| fact-check | PASS | 0 | fact-check-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 19, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`

## GEO QA fixes applied (fix cycle 1, 2026-11-01)

1. `rospatent.gov.ru` (SSL fail в Cloud) → `gosuslugi.ru` (ГУ ПО), `pravo.ppt.ru` (таблица пошлин), `gosuslugi.ru` (инструкция ТЗ).
2. Internal 404: `/sposoby-zashchity-izobreteniya` → `/patent`; `/kak-zaregistrirovat-brend-na-ozon-i-wildberries` → live slug L03 с подчёркиваниями.

## Gate

**PASS** — директор может запускать cover || schema.
