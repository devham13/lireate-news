# QA: L11 dogovor-na-razrabotku-logotipa-prava-ot-dizajnera

date: 2026-10-21
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, 3 таблицы, ol×12, blockquote workflow |
| GEO / citability | 25 | 23 | TL;DR с нормами ГК, таблицы отчуждение/лицензия, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 12 | 0 AI-slop hits; −3 slop WARNING (8 предложений >25 слов, часть из таблиц) |
| Fact safety | 15 | 12 | fact-check PASS (10 unverified stats; сверено с research-notes) |
| Contract HTML | 10 | 8 | linter PASS, объём ~9.5k ✓; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — договор, права от дизайнера, primary query |
| C02 | ✓ | Lead + TL;DR — ст. 1259, 1288, 1234, 1286 |
| C03 | ✓ | Заказчик бренда / владелец бизнеса перед ТЗ |
| C04 | ✓ | AP vs ТЗ, отчуждение, авторский заказ, п. 9 ст. 1483 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Владелец → AP/ТЗ → исполнитель → модель прав → договор → акт → папка → чек-лист → FAQ |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol×2, blockquote |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | Consultant, T-Ж, cyberrlaw, art.etopravo |
| R03 | ✓ | Нет выдуманных процентов/цен |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от шаблонов DOCX — алгоритм + чек-листы |
| E02 | ✓ | «Делайте / не делайте» в H2 |
| E03 | ✓ | CTA reg-tz + L01 чек-лист, ≤3 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата проверки норм |
| Ept02 | ✓ | Internal: L01 chek-list, reg-tz-main |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | WARNING (acceptable) | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | PASS | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 14, failed: 0
- site-base: публичный домен Lireate (`--site-base`, `--timeout 60` для медленных consultant.ru)
- fix cycle: не требовался (flaky timeout на 15–45s; повтор с 60s — pass)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 8 (часть — артефакт разбора таблиц)
- Flesch RU: 48.3 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (13 extracted, 3 verified, 10 unverified)
- нормы ГК и практика сверены с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: только повтор link-verify с увеличенным timeout; `article.html` без правок

## Optional (не blocker)

- добавить `<img>` с alt по контракту

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
