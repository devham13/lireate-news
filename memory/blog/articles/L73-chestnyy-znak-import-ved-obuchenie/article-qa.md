# QA: L73 chestnyy-znak-import-ved-obuchenie

date: 2026-11-20
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ H3×6, 3 таблицы, TL;DR blockquote, ol×4 |
| GEO / citability | 25 | 22 | RACI-таблица, workflow blockquote, CMR↔КМ, markirovka.ru / docs.crpt.ru |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 slop-клише; slop-detector WARNING — 10 предложений >25 слов |
| Fact safety | 15 | 12 | fact-check WARNING (7 extracted, 3 verified); штрафы 50–100 тыс. и «72 ч» без строки в fact-bank — дисклеймер + КоАП ссылка |
| Contract HTML | 10 | 10 | html-linter PASS; char_count 8827 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1 — обучение ВЭД до подачи документов |
| C02 | ✓ | Lead + TL;DR, дата 20.11.2026 |
| C03 | ✓ | Менеджер ВЭД, брокер, юрист, бренд |
| C04 | ✓ | ТН ВЭД, CMR, гр. 31, КМ «Ввезен в РФ» |
| O01 | ✓ | H2 = модули / how-to |
| O02 | ✓ | Модуль 0 → пакет брокеру → ввод с ФТС |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | 3 таблицы, blockquote workflow, ol×4 |
| R01 | ✓ | «Делайте / не делайте» в секциях |
| R02 | ✓ | markirovka.ru, markirovka.crpt.ru, КонсультантПлюс, lireate CTA |
| R03 | ✓ | Штрафы по КоАП; 72 ч ПК — как типовой срок рынка |
| R04 | ✓ | FAQ answer-first |
| E01 | ✓ | Угол L73 (syllabus ВЭД) vs L67/L22/L36 |
| E02 | ✓ | RACI, таблица обучения vs ПК |
| E03 | ✓ | registraciya_tovarnogo_znaka, chek_list маркировки |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Блок «Материал проверен» |
| Ept02 | ✗ | Slug L67/L36 на проде 404 → HTTPS markirovka.ru + docs.crpt.ru + CMS chek_list |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | WARNING (допустимо) | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | WARNING (допустимо) | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (L73↔L22/L67 кластер) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify (fix cycle 1, 2026-11-20)

- total: 10, failed: 0
- internal slug L67/L22/L36 (404/таймаут на проде) → markirovka.ru импорт, docs.crpt.ru (импорт с ФТС), `/chek_list_markirovka_importa_chestnyiy_znak_i_tovarnyiy_znak_brenda/`
- `markirovka.crpt.ru` → trailing slash; CTA `/reg-tz-main` → `/registraciya_tovarnogo_znaka/`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 10
- Flesch RU: 74.5 (Easy)

## Fact-check

- verdict: WARNING (7 extracted, 3 verified, 4 unverified — штрафы и «72 ч»)
- see `fact-check-report.json`

## Cannibalization

- repo-wide WARNING; для L73 ожидаемо пересечение secondary с L22/L67 импорт-кластер
- see `cannibalization-report.json`

## Utility gate

- article: PASS
- see `utility-gate-report.json`

## Fix cycle

- GEO QA правки в `article.html`: ссылки и meta `title_seo` (VED); verdict **PASS**, cover||schema разрешены.