# QA: L77 patentnyy-trolling-kak-proverit-pretenziyu-i-zashchititsya

date: 2026-11-20
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×6, FAQ 6, таблицы, blockquote TL;DR, inline-схема |
| GEO / citability | 25 | 22 | матрица истца, маршрут 1486/1512–1513, чек-лист доказательств |
| CORE-EEAT lite | 15 | 14 | 17/20 |
| Human voice | 15 | 13 | 0 slop; 2 предложения >25 слов |
| Fact safety | 15 | 13 | fact-check PASS (20 stats, 4 verified) |
| Contract HTML | 10 | 8 | linter PASS, объём ~8.5k; cover refs в HTML |

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

- total: 21, failed: 0
- fix cycle 1: consultant §1486/1512/1513/1301 → zakonrf.info; fips.ru → текст; egrul → pb.nalog.ru; Обзор ВС 2023 → PDF storage.consultant.ru; bare garant → kad

## FIX applied (GEO QA)

- article.html: стабильные URL норм ГК и обзора ВС; без ссылок на 403/404 endpoints.