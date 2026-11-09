# QA: L41 otchuzhdenie-tovarnogo-znaka-dogovor-reestr

date: 2026-11-09
score_total: 88/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, таблица отчуждение/лицензия/изменения, workflow blockquote |
| GEO / citability | 25 | 23 | TL;DR, ol×2, таблица пошлин, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 18/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 два предложения >25 слов |
| Fact safety | 15 | 12 | fact-check PASS; 10 unverified в bank — сверено с research-notes |
| Contract HTML | 10 | 9 | linter PASS, ~8558 символов; −1 нет `<img>` с alt (ожидается после cover) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — договор отчуждения, регистрация в Роспатенте |
| C02 | ✓ | Lead + TL;DR — ст. 1234 п. 4, пошлина 3.11 |
| C03 | ✓ | Продавец/покупатель бренда, M&A, ИП→ООО |
| C04 | ✓ | Отчуждение vs лицензия vs смена адреса |
| O01 | ✓ | H2 по workflow research |
| O02 | ✓ | Нужен ли договор → сравнение → реестр → цена → пошлина → сроки → контрагенты |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol, blockquote-workflow |
| R01 | ✓ | Секции 40–60 слов, цитируемые цифры |
| R02 | ✓ | Consultant (ГК), klerk, searchplatform, online.rospatent, GARANT |
| R03 | ✓ | 15 000/13 000 ₽, 68/45/5 дн. — research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «продажа бренда = запись в реестре», не дубль лицензии L02 |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA `/reg-tz-main` ×2; interlink L40, L19 (live slug) |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 09.11.2026, не юрконсультация |
| Ept02 | ✗ | Canonical L41 ещё не на хостинге (до publish) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | WARNING (repo-wide, L41 не в issues) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 16, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-11-09): L19 → `lireate_seo_url` с подчёркиваниями; rospatent.gov.ru (SSL) → klerk + online.rospatent; fips PDF/opendata → GARANT + licensingrussia

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 49.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (12 extracted, 2 verified in bank, 10 unverified)
- пошлины 3.10–3.11, сроки АР 371 — сверены с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (4 issues между другими L-статьями; L41 не затронут)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 6 битых href (внутренний L19, rospatent SSL, fips 403)
- cycle 2: не требовался

## Optional (не blocker)

- inline `<img>` после cover
- после publish: canonical 200 на хостинге

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
