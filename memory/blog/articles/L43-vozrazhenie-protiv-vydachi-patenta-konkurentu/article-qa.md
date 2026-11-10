# QA: L43 vozrazhenie-protiv-vydachi-patenta-konkurentu

date: 2026-11-10
score_total: 85/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8 + FAQ, таблица×2, ol×6+, TL;DR blockquote |
| GEO / citability | 25 | 22 | развилка заявка/ППС, workflow blockquote, «Делайте / не делайте», пошлины 7k/3k/14k |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 12 | 0 AI-slop hits; −3 over-long (3) |
| Fact safety | 14 | 10 | fact-check WARNING (6 verified, 17 unverified; research-notes) |
| Contract HTML | 10 | 9 | linter PASS, collage figure, ~8.6k ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — возражение против выдачи патента, ППС vs замечания |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Производитель устройств, конкурент на рынке |
| C04 | ✓ | 1350, 1385–1387, 1398, 1248, Правила ППС в первых блоках |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | стадия → мониторинг → уровень техники → замечания → ППС → заседание → после отказа |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица×2, ol×16+, blockquote×4 |
| R01 | ✓ | Standalone блоки в H2-секциях |
| R02 | ✓ | consultant.ru, garant.ru, patent-family.ru — research-notes |
| R03 | ✓ | 7 000 / 3 000 / 14 000 ₽, сроки 18 мес., 7 мес. — с источниками |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол third party vs L04 (отказ вам), L08 (ТЗ), L31 (таможня) |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA `/patent` (×2), рубрика category=20; ≤3 commercial |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes, таблица сценариев |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, дата 10.11.2026 |
| Ept02 | ✗ | −1: interim `/news?num=2&category=*` до live slug L04/L05/L08/L31 |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| html-linter | PASS | 0 | html-linter-report.json |
| link-verify | PASS | 0 | link-verify.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, L22↔L36, не L43) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| fact-check | WARNING | 0 | fact-check-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 17 → 15 unique href after fixes, failed: 0
- site-base: публичный домен Lireate (`LIREATE_PUBLIC_SITE_URL`)
- fix cycle 1 (2026-11-10): internal slug 404 (L04/L05/L08/L31) → `/news?num=2&category=20|9`; rospatent.gov.ru/dues (SSL) → КонсультантПлюс (Положение о пошлинах); fips.ru (403) → searchplatform.rospatent.gov.ru/patents + patent-family.ru (ППС)

## GEO QA fixes applied (fix cycle 1)

1. Четыре внутренних canonical slug (ещё не live) → рубрики новостей 200.
2. Три ссылки на `rospatent.gov.ru/ru/activities/dues/table` → consultant Положение о пошлинах.
3. Три ссылки на правила ППС fips.ru → patent-family.ru; `registers-web` → Поисковая платформа.

## Gate

**PASS** — директор может запускать cover || schema.
