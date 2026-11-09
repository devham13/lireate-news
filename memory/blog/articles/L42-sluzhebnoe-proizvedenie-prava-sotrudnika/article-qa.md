# QA: L42 sluzhebnoe-proizvedenie-prava-sotrudnika

date: 2026-11-09
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×10, FAQ 6, таблица штат/подряд, документы |
| GEO / citability | 25 | 22 | TL;DR, ol×2, 2 таблицы, FAQ answer-first |
| CORE-EEAT lite | 15 | 13 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 девять предложений >25 слов (WARNING) |
| Fact safety | 15 | 12 | fact-check PASS; 6 unverified в bank — сверено с research-notes (ст. 1295, 3 года) |
| Contract HTML | 10 | 8 | linter PASS; cover placeholder в теле (ожидается pipeline collage) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — ст. 1295, права работодателя на контент сотрудника |
| C02 | ✓ | Lead + TL;DR — обязанности, 3 года, должностка |
| C03 | ✓ | HR, собственник, руководитель маркетинга |
| C04 | ✓ | Матрица штат (1295) vs подряд (1288/1234) vs сомнительный кейс |
| O01 | ✓ | H2 по workflow research |
| O02 | ✓ | Определение → сравнение → права → документы → 3 года → вознаграждение → договор → чек-лист |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | Таблицы, ol, blockquote-workflow |
| R01 | ✓ | Секции 40–60 слов, цитируемые нормы ГК |
| R02 | ✓ | Consultant, GARANT, podpisal.ru, advokats.ru |
| R03 | ✓ | 3 года, п. 105 ПП ВС — research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L11 (подряд) и L35 (вознаграждение) |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA `/news?num=2&category=12` и category=10; L35 live |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 09.11.2026, не юрконсультация |
| Ept02 | ✗ | Canonical L42 ещё не на хостинге (до publish) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING | slop-detector-report.json |
| cannibalization | WARNING (repo-wide, L42 не в issues) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 8 unique href, failed: 0
- fix cycle 1 (2026-11-09): L11 `/dogovor-…` и `/dogovor_avtorskij` (404 live) → `/news?num=2&category=10` и `category=12`; bardov.legal (timeout) и dangal.ru (404) → podpisal.ru (200)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 9
- Flesch RU: 50.8 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (8 extracted, 2 verified in bank, 6 unverified)
- ст. 1295, трёхлетнее окно — сверены с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (4 issues между другими L-статьями; L42 не затронут)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 4 битых href (L11, dogovor_avtorskij, bardov, dangal)
- cycle 2: не требовался

## Optional (не blocker)

- сократить 9 длинных предложений (slop WARNING)
- после publish: canonical 200; indexer — seo_url L11/L42 на live

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (6) | HowTo: no | Review: no | author_id: pending registry
