# QA: L64 nejming-i-logotip-soglasovanie

date: 2026-11-18
score_total: 91/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ×7, таблица×1, ol×7, TL;DR blockquote |
| GEO / citability | 25 | 24 | Таблица стратегий заявок, схема согласования, 1492/1483, матрица комбо vs раздельные |
| CORE-EEAT lite | 15 | 14 | 18/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; Flesch 39.2 (сложная юрид. тема); 5 предложений >25 слов |
| Fact safety | 14 | 12 | fact-check PASS; 5/8 verified; «3–5 лет», 46 200 ₽ — research-notes / ГАРАНТ |
| Contract HTML | 12 | 12 | linter PASS, ~8668 знаков; cover — шаг 4 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/meta — primary «нейминг и логотип» |
| C02 | ✓ | Lead + TL;DR answer-first |
| C03 | ✓ | Основатель, маркетинг, продукт до подачи |
| C04 | ✓ | МКТУ, комбинированное обозначение, графа 571 |
| O01 | ✓ | H2 по action_outline research |
| O02 | ✓ | Имя → поиск → бриф → макет → стратегия заявок |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol×7, blockquote×4 |
| R01 | ✓ | Делайте / не делайте в каждом блоке |
| R02 | ✓ | Consultant, ГАРАНТ, searchplatform |
| R03 | ✓ | 46 200 ₽, 11.12.2023 — fact-bank / ГАРАНТ |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «согласование до дизайна», не generic «как зарегистрировать» |
| E02 | ✓ | Практика в каждой H2 |
| E03 | ✓ | CTA `/reg-tz-main`, 1× |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 18.11.2026 |
| Ept02 | ✓ | L01, L06, L11, L38, L39, L48 |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | WARNING | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (legacy-пары; не L64) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 14, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix (GEO QA cycle 1): внутренние L06/L11 на live seo_url; rospatent.gov.ru/fips → gosuslugi, licensingrussia, base.garant.ru/408182169/

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 39.2 (Hard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (8 extracted, 5 verified, 3 contextual: горизонт планирования, тариф)
- see `research-notes.md`, `fact-check-report.json`

## Cannibalization

- verdict: WARNING (7 legacy cross-topic warnings; L64 primary не в списке)
- see `cannibalization-report.json`

## GEO QA edits

- `article.html`: замена 7 внешних/внутренних ссылок (link-verify PASS)