# QA: L51 patent-na-poleznuyu-model-rospatent

date: 2026-11-11
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×7 + FAQ 7, таблица пошлин + сравнение ПМ/изобретение, TL;DR, 3 inline-collage + cover |
| GEO / citability | 25 | 23 | workflow blockquote, таблицы, FAQ standalone, 15 000 ₽ и п. 1.2/1.9/1.17 |
| CORE-EEAT lite | 15 | 13 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; −1 за 2 over-long фрагмента |
| Fact safety | 15 | 12 | fact-check PASS (28 extracted, 6 verified, 22 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS; cover `<figure>` + lazy inline |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — полезная модель, ст. 1351, Роспатент |
| C02 | ✓ | Lead + TL;DR — устройство, 15 000 ₽, ст. 1390 |
| C03 | ✓ | изготовитель с прототипом, редакция Лирейт |
| C04 | ✓ | ст. 1351, 1363, 1376, 1390, 1247; Приказ № 701; Положение о пошлинах |
| O01 | ✓ | H2 по research action_outline |
| O02 | ✓ | объект → проверка → маршрут → пакет → пошлины → поверенный → CTA |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблицы×4, blockquote×3, ol-чек-листы, workflow |
| R01 | ✓ | «Делайте / не делайте», FAQ, таблица пошлин |
| R02 | ✓ | ConsultantPlus, Госуслуги, searchplatform, online.rospatent |
| R03 | ✓ | 15 000 ₽, 17 мес. 2 нед., дата 11.11.2026 — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | отстройка от L05 (comparison) и /patent для изобретения |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA patent, L43/L04 interlink |
| Exp01 | ✓ | Режим B (таблица + checklist) |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | дисклеймер «не заменяет поверенного», дата 11.11.2026 |
| Ept02 | ✗ | Wordstat не в материале (MCP недоступен) — не блокер |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo L08↔L21, L22↔L36, L34↔L38; не L51) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 19, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1 (GEO QA): rospatent.gov.ru (SSL) → ConsultantPlus (пошлины) + Госуслуги (ПМ) + online.rospatent; fips.ru (403) → searchplatform / plain text; internal 404 (`/izobretenie/`, `/patentovanie/`, L05 canonical не live) → live `/patent`, `/otkazali_v_*`, `/vozrazhenie_*`; max deep link → `https://max.ru/`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 56.2 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (28 extracted, 6 verified, 22 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L51 (0 issues на L51); repo WARN — не блокер

## Blockers

— нет
