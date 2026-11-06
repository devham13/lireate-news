# QA: L36 chestnyy-znak-import-snippet-dokumenty

date: 2026-11-06
score_total: 85/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×7, FAQ H3×7, `<ol>` 7 шагов, 1 таблица, TL;DR blockquote |
| GEO / citability | 25 | 23 | Таблица узлов, markirovka.ru / docs.crpt.ru / поддержка crpt; внутренний URL L22 на проде 404 → заменён на официальный гайд markirovka.ru |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 slop-клише; slop-detector WARNING из‑за 15 предложений >25 слов |
| Fact safety | 15 | 12 | fact-check PASS (6 extracted, 1 verified, 5 unverified — лимиты СУЗ/объёмы ввода без строки в fact-bank; дисклеймер в теле) |
| Contract HTML | 10 | 9 | html-linter PASS; `char_count` = 9364 (8500–9500) после сокращения одного абзаца |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — сниппет импорта ЧЗ, документы, ошибки |
| C02 | ✓ | Lead + TL;DR — маршрут импорта и attachment |
| C03 | ✓ | Импортёр, склад, брокер, поддержка crpt |
| C04 | ✓ | ЕРВК, ФТС, графа 31, заказ КМ, XML/ID |
| O01 | ✓ | H2 = пошаговые блоки (ЕРВК, НК, документы, графа 31, ввод, сниппет) |
| O02 | ✓ | Цепочка: каталог → заказ → нанесение → ДТ → выпуск → ввод |
| O03 | ✓ | FAQ 7 пар |
| O04 | ✓ | Таблица узлов, blockquote (пример ошибки, цепочка), `<ol>`×7 |
| R01 | ✓ | Секции с «Делайте / не делайте» и таблицей |
| R02 | ✓ | markirovka.ru, docs.crpt.ru, kv-ai.ru (курс), t.me |
| R03 | ✓ | Лимиты СУЗ и объёмы ввода помечены как справка сообщества / сверка по ТГ |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол L36 (сбои/сниппеты) vs L22 (общий чеклист импорта); ссылка на официальный раздел markirovka.ru |
| E02 | ✓ | «Делайте / не делайте», таблица ошибок |
| E03 | ✓ | CTA Make, Telegram; официальные ссылки |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes в каталоге статьи |
| Exp03 | ✓ | 0 slop hits (клише) |
| Ept01 | ✓ | Блок «Материал проверен» + оговорка по Вордстату |
| Ept02 | ✓ | Внутренний slug L22 не проверялся как live (404) → в тексте только внешний проверенный URL |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | WARNING (допустимо) | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (L22↔L36 overlap) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 4, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 30`
- fix: относительная ссылка на L22 давала **404** на проде → заменена на **HTTPS markirovka.ru** (раздел про импорт), дубликат того же URL в FAQ сохранён проверенным

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 14 → verdict WARNING (не блокер при 0 клише)
- Flesch RU: 72.6 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (6 extracted, 1 verified, 5 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (L22 primary vs L36 secondary ~75% Jaccard) — ожидаемо по тематике; не fail
- see `cannibalization-report.json`

## Utility gate

- article: PASS (7 шагов `<ol>`, 7 практических H2, action markers 14, таблица + blockquote)
- see `utility-gate-report.json`
