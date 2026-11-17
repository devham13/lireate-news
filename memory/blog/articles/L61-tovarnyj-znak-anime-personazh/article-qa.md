# QA: L61 tovarnyj-znak-anime-personazh

date: 2026-11-17
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9 (+FAQ), FAQ×7, таблицы×3, ol 9 шагов, TL;DR blockquote |
| GEO / citability | 25 | 23 | Три слоя ©/лицензия/ТЗ; п. 9 ст. 1483; таблица сценариев |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; Flesch 56.5 Standard; 4 предложения >25 слов (таблицы) |
| Fact safety | 14 | 11 | fact-check PASS; 2/11 в fact-bank, остальное — research-notes / НПА |
| Contract HTML | 12 | 10 | linter PASS, ~8879 знаков; cover — шаг 4 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — аниме-персонаж, чек-лист, мерч |
| C02 | ✓ | Lead + TL;DR answer-first |
| C03 | ✓ | Селлер мерча, заявитель ТЗ |
| C04 | ✓ | п. 9/6 ст. 1483, 1259, ПП 941 в первых блоках |
| O01 | ✓ | H2 по сценариям → © → мерч → лицензия → реестр → отказ → пошлина → чек-лист |
| O02 | ✓ | Логичный outline checklist |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы×3, ol, blockquote |
| R01 | ✓ | Standalone блоки с «Делайте / не делайте» |
| R02 | ✓ | Consultant, Kodansha licensing FAQ, РБК, searchplatform |
| R03 | ✓ | 35 000 ₽ и дата 05.10.2024 из research |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «три слоя» vs generic «запатентовать аниме» |
| E02 | ✓ | Практика в каждой H2 |
| E03 | ✓ | CTA `/registraciya_tovarnogo_znaka/`, ≤3 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, не гарантия регистрации |
| Ept02 | ✗ | L11/L09 → рубрики news (slug 404 на live до publish) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (legacy-пары; не L61) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 16, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix (GEO QA cycle 1): L60 → live `chek_list_kartinyi_…`; L17 → live underscore slug; L11/L09 → `/news?num=2&category=10|9`; rospatent dues SSL → ПП 941; max.ru profile 403 → `https://max.ru/`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 56.5 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (11 extracted, 2 verified, 9 unverified)
- нормы ГК и пошлины сверены с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- repo-wide WARNING (7 legacy-пар); **L61 primary_query** не в конфликте с другими L*

## Fixes applied (GEO QA)

1. `article.html`: internal href на live/рубрики; rospatent dues → consultant ПП 941; MAX → корень домена.
2. `article.meta.json`: `char_count` 8879.