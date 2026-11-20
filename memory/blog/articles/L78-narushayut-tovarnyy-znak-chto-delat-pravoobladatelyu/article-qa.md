# QA: L78 narushayut-tovarnyy-znak-chto-delat-pravoobladatelyu

date: 2026-11-20
score_total: 83/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×6, FAQ 7, 2 таблицы, TL;DR, blockquote-схема |
| GEO / citability | 25 | 22 | способы использования, матрица претензии, 7 шагов |
| CORE-EEAT lite | 15 | 14 | 17/20 |
| Human voice | 15 | 12 | 0 slop; 3 длинных предложения (таблицы) |
| Fact safety | 15 | 13 | fact-check PASS (13 stats, 2 verified) |
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

- total: 14, failed: 0
- fix cycle 1: fips.ru → текст; egrul → pb.nalog.ru; consultant root (1491/1250/1253.1) → hash/zakonrf

## FIX applied (GEO QA)

- article.html + article.meta.json (description_seo ≤180).