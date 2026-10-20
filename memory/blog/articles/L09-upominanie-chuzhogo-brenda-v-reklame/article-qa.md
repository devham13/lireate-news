# QA: L09 upominanie-chuzhogo-brenda-v-reklame

date: 2026-10-20
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, 2 таблицы, ol×9, матрица форматов |
| GEO / citability | 25 | 23 | TL;DR, blockquote workflow, таблица рисков, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 пять предложений >25 слов |
| Fact safety | 15 | 12 | fact-check WARNING (17 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, объём ~8.5k ✓; −1 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — чужой бренд в рекламе, форматы |
| C02 | ✓ | Lead + TL;DR — 1484, исчерпание, ст. 5, соцреклама |
| C03 | ✓ | Обращение к рекламодателю / маркетологу |
| C04 | ✓ | ст. 1484, 1487, 1515, ст. 5 и 10 ФЗ о рекламе, 14.3/14.6 ЗоК |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Цель → матрица → сравнение → исчерпание → Директ → сайт → чек-лист → претензия |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | КонсультантПлюс, ГАРАНТ, Роспатент, arbitr.ru, письмо ФАС |
| R03 | ✓ | Компенсация 10k–10M, дела СИП — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L02 (претензия) и L01 (реестр) |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA защита знака ×1, interlink L01/L02 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, без «безрискового» креатива |
| Ept02 | ✗ | L02 interlink через `/news?num=2&category=9` (canonical 404 до publish) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS (acceptable) | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 10, failed: 0
- site-base: публичный домен Lireate (`--site-base`, timeout 25s)
- fix cycle 1 (2026-10-20): consultant deep links → корни LAW_64629/58968/61763; L02 `/otvet-na-pretenziyu-…` 404 → `/news?num=2&category=9`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 57.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (19 extracted, 2 verified, 17 unverified)
- факты сверены с `research-notes.md` (1484/1487, ст. 5, письмо ФАС 2019, дела СИП)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 17 правок href в `article.html`
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish L02: вернуть interlink на `/otvet-na-pretenziyu-pravoobladatelya-tovarnogo-znaka`

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
