# QA: L39 dorabotka-logotipa-pered-registraciey-tovarnogo-znaka

date: 2026-11-09
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9 + FAQ 7, ol×5, таблица мотивов, TL;DR, 4 inline-collage |
| GEO / citability | 25 | 23 | таблица п. 1–3 ст. 1483, ol-чек-листы, FAQ с прямым ответом, blockquote workflow |
| CORE-EEAT lite | 15 | 12 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; −1 за 1 over-long фрагмент в таблице |
| Fact safety | 15 | 12 | fact-check PASS (7 extracted, 4 verified, 3 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS; cover `<figure>` + lazy inline |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — доработка логотипа, ст. 1483, экспертиза |
| C02 | ✓ | Lead + TL;DR — различительность, 6 мес., ст. 1497/1499 |
| C03 | ✓ | владелец бренда, маркетолог, редакция Лирейт |
| C04 | ✓ | ст. 1483, 1497, 1499, Руководство ФИПС 7.1.2.x, 2.9 |
| O01 | ✓ | H2 по research action_outline |
| O02 | ✓ | доминанта → мотивы → силуэт → файлы → 1497 → уведомление → CTA |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица, ol×5, blockquote×3, workflow-схема |
| R01 | ✓ | «Делайте / не делайте», чек-листы, FAQ standalone |
| R02 | ✓ | ConsultantPlus, ГАРАНТ, Поисковая платформа, online.rospatent |
| R03 | ✓ | 6 месяцев, 46 200 руб., дата 09.11.2026 — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | отстройка от L34/L38 (патент vs доработка), legacy-гайд |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA reg-tz-main, рубрика «Логотип» |
| Exp01 | ✓ | Режим B (таблица + checklist) |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | дисклеймер «не юруслуга», дата 09.11.2026 |
| Ept02 | ✗ | Wordstat не в материале (AUTH на research) — не блокер |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo L08↔L21, L22↔L36, L34↔L38; не L39) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 15, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1 (GEO QA): L07 canonical 404 на live → live legacy `/otnositelnyie_osnovaniya_otkaza_v_registracii_tz_otvet_ekspertize` (3 ссылки); rospatent.gov.ru documentforms (SSL) → `online.rospatent.gov.ru`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 1
- Flesch RU: 50.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (7 extracted, 4 verified, 3 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L39 (0 issues на L39); repo WARN — не блокер

## Blockers

— нет
