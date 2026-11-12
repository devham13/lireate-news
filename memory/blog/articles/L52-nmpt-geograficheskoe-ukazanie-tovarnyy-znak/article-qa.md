# QA: L52 nmpt-geograficheskoe-ukazanie-tovarnyy-znak

date: 2026-11-12
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×6 + FAQ 7, 3 таблицы, TL;DR, collage-v1 cover + 3 inline |
| GEO / citability | 25 | 23 | workflow blockquote, таблица ТЗ/ГУ/НМПТ, п. 7 и пошлины 2.3–2.13 |
| CORE-EEAT lite | 15 | 13 | 17/20 |
| Human voice | 15 | 14 | 0 AI-slop; 2 over-long sentences |
| Fact safety | 15 | 12 | fact-check PASS (research-notes, без номеров дел по Иван-чаю) |
| Contract HTML | 10 | 9 | linter PASS; white cover #ffffff |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| excalibur_blog_html_linter.py | PASS | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | slop-detector-report.json |
| excalibur_blog_fact_checker.py | PASS | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | repo-wide |
| lireate_collage_publish_gate.py | PASS | cover/cover-collage-qa.md |
| lireate_seo_url_publish_guard.py | PASS | uniq nmpt_geograficheskoe_ukazanie_i_tovarnyy_znak |

## Link verify

- total: 21, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- internal L07/L08 → live underscore paths; fips 403 → searchplatform / licensingrussia

## Blockers

— нет
