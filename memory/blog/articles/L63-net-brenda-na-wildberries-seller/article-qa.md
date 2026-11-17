# QA: L63 net-brenda-na-wildberries-seller

date: 2026-11-17
score_total: 88/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9 (+FAQ), FAQ×7, таблица×1, ol×7, TL;DR blockquote |
| GEO / citability | 25 | 23 | Таблица ситуаций, схема выбора, развилка WB vs ТЗ, ст. 1483/1484 |
| CORE-EEAT lite | 15 | 14 | 18/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; Flesch 63.8 Easy; 5 предложений >25 слов |
| Fact safety | 14 | 11 | fact-check WARNING; 7/9 в fact-bank, «2 р.д.» и ст. 1484 — research-notes / НПА |
| Contract HTML | 12 | 12 | linter PASS, ~8507 знаков; cover — шаг 4 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — primary «как разобраться нет бренда» |
| C02 | ✓ | Lead + TL;DR answer-first |
| C03 | ✓ | Селлер WB, перекуп, масштабирование |
| C04 | ✓ | ТЗ vs справочник WB в первых блоках |
| O01 | ✓ | H2 по action_outline research |
| O02 | ✓ | От значения → запреты → модерация → ТЗ → шаги |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol×7, blockquote |
| R01 | ✓ | Standalone «Делайте / не делайте» |
| R02 | ✓ | WB seller, Consultant, searchplatform, Garant |
| R03 | ✓ | 46 200 / 15 р.д. из fact-bank + Garant |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «нет бренда» vs generic «заполнить карточку» |
| E02 | ✓ | Практика в каждой H2 |
| E03 | ✓ | CTA `/reg-tz-main`, ≤3 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 17.11.2026 |
| Ept02 | ✓ | L59, L03, L18 |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | WARNING | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (legacy-пары; не L63) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 15, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix (GEO QA cycle 1): reklama.tochka.com (SSL) → ezybrand.ru; fips.ru 403 → base.garant.ru/408182169/; `meta_ab.title_seo` — ключи primary_query

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 63.8 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (9 extracted, 7 verified, 2 unverified: «2 р.» срок модерации WB, п. 1484 в НПА)
- см. `research-notes.md`, Consultant
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (7 legacy cross-topic warnings; L63 primary не в списке)
- see `cannibalization-report.json`

## GEO QA edits

- `article.html`: замена 2 внешних ссылок (link-verify PASS)
- `article.meta.json`: `title_seo` для utility gate