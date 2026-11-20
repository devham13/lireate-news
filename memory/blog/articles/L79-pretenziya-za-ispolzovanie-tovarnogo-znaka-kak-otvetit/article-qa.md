# QA: L79 pretenziya-za-ispolzovanie-tovarnogo-znaka-kak-otvetit

date: 2026-11-20
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×7, FAQ 7, 2 таблицы, шаблон ответа, TL;DR |
| GEO / citability | 25 | 23 | поэтапный ответ, матрицы проверки, L75/L76 cross-links |
| CORE-EEAT lite | 15 | 14 | 17/20 |
| Human voice | 15 | 13 | 0 slop; 2 длинных предложения |
| Fact safety | 15 | 12 | fact-check PASS (21 stats, 3 verified) |
| Contract HTML | 10 | 8 | linter PASS |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| excalibur_blog_fact_checker.py | PASS | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | link-verify.json |
| excalibur_blog_html_linter.py | PASS | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | slop-detector-report.json |
| excalibur_blog_utility_gate.py | PASS | utility-gate-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo) | memory/blog/cannibalization-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | — |

## Link verify

- total: 18, failed: 0
- fix cycle 1: fips/opendata/ssl → платформа; vsrf 333 → zakonrf; п. 157 ППВС → LAW_329754; egrul → pb.nalog.ru

## FIX applied (GEO QA)

- article.html: только проверенные внешние URL.