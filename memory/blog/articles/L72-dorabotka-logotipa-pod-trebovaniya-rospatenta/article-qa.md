# QA: L72 dorabotka-logotipa-pod-trebovaniya-rospatenta

date: 2026-11-20
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9 + FAQ 7, ol×5, таблица цвет/ч-б, TL;DR, cover + 2 inline-collage |
| GEO / citability | 25 | 23 | таблица формат/dpi, workflow-blockquote, FAQ с прямым ответом, чек-лист |
| CORE-EEAT lite | 15 | 12 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-clichés; slop WARNING — 6 over-long (таблицы/workflow), не блокер |
| Fact safety | 15 | 12 | fact-check PASS (11 extracted, 3 verified, 8 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS после правки блока «Достоверность данных» |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — доработка под Роспатент, TIFF, 540/591/571 |
| C02 | ✓ | Lead + TL;DR — одна версия, dpi, непрозрачный фон |
| C03 | ✓ | «Материал проверен» — редакция Лирейт |
| C04 | ✓ | п. 27 № 482, ст. 1492, 1483, online.rospatent |
| O01 | ✓ | H2 по research action_outline |
| O02 | ✓ | отстройка L39 → версия → цвет/591 → 8×8 → экспорт → 571 → чек-лист → CTA |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица×2, ol×5, blockquote×3, workflow |
| R01 | ✓ | «Делайте / не делайте», чек-листы, FAQ standalone |
| R02 | ✓ | ConsultantPlus, ИПП, Поисковая платформа, online.rospatent |
| R03 | ✓ | 20.11.2026, 300 dpi, ≤5 МБ, 8×8 — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | отстройка от L39 (смысл) и L54 (смешение) |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA `/reg-tz-main` ×2 |
| Exp01 | ✓ | Режим B (таблицы + checklist) |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop cliché hits |
| Ept01 | ✓ | дисклеймер «не юрконсультация», дата 20.11.2026 |
| Ept02 | ✓ | Wordstat не в тексте |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json (`--timeout 90`) |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | WARNING | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (L72↔L39 secondary 100%; repo L08/L22/L34/L36/L67) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 15, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1 (GEO QA): L54 canonical 404 → live `/graficheskiy_tovarnyy_znak_smeshchenie_do_podachi/`; `rospatent.gov.ru` FAQ/forms → ИПП / `online.rospatent.gov.ru`; consultant 418 на якоре 1497 → якорь `69c22eee…` (п. 8 ст. 1492)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 6 (в т.ч. склейка текста таблиц детектором)
- Flesch RU: 62.5 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (11 extracted, 3 verified, 8 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L72 (контент от L39: техника vs смысл); repo WARN L72↔L39 query overlap — не блокер

## Blockers

— нет

## HTML fixes (GEO QA)

1. Внутренние ссылки L54 → live `seo_url`
2. Внешние ссылки: убран `rospatent.gov.ru` (SSL), заменены на ИПП / online
3. Блок «Достоверность данных»: убраны маркеры Вордстат/«среда подготовки» (linter)