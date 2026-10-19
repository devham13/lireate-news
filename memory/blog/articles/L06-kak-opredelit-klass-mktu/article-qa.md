# QA: L06 kak-opredelit-klass-mktu

date: 2026-10-19
score_total: 88/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×6, FAQ 6, сравнительная таблица, отсечение «школьного» класса 27 в lead |
| GEO / citability | 25 | 23 | TL;DR, workflow blockquote, 6-шаговый `<ol>`, 6 FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 18/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 пять длинных предложений (>25 слов) |
| Fact safety | 15 | 13 | fact-check PASS (6 extracted, 5 verified, 1 unverified «3–5 лет») |
| Contract HTML | 10 | 8 | linter PASS, объём ~9078 ✓; −2 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title закрывают подбор класса МКТУ для ТЗ |
| C02 | ✓ | Lead — direct answer про риск неверного класса |
| C03 | ✓ | ИП, маркетплейс, линейка товаров/услуг |
| C04 | ✓ | МКТУ-13–2026, п. 6 ст. 1483, корреспондирующие классы |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Структура → входные данные → поиск → кейсы → корреспонденция → ошибки |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | Таблица, ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | ФИПС/классификатор Роспатента, РГ, КонсультантПлюс, Поисковая платформа |
| R03 | ✓ | 46 200 ₽ предоценка, 45 классов, кейсы 14/27/30/9 |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол how-to МКТУ, не дубль L01 (проверка знака) |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA `/reg-tz-main`, interlink на live L01 path |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | Brief/research-notes, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения DIY, не юрконсультация |
| Ept02 | ✗ | Canonical `/kak-opredelit-klass-mktu` ещё не на хостинге (ожидаемо до publish) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS (acceptable) | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 7, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-10-19): fips.ru (403) → классификатор Роспатента; rospatent.gov.ru/dues (SSL) → klerk.ru; internal slug из meta (404) → live `/proverka_tovarnogo_znaka_…`, `/reg-tz-main`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 43.7 (Hard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (6 extracted, 5 verified, 1 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 4 href (external + internal live paths)
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish: canonical `/kak-opredelit-klass-mktu` на хостинге

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (6) | HowTo: no | Review: no | author_id: pending registry
