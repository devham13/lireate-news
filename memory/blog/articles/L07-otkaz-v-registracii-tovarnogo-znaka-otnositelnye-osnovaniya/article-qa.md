# QA: L07 otkaz-v-registracii-tovarnogo-znaka-otnositelnye-osnovaniya

date: 2026-10-20
score_total: 91/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×7, FAQ 7, 2 таблицы, матрица п. 6–10, угол «три документа — три срока» |
| GEO / citability | 25 | 24 | TL;DR, blockquote-workflow, ol×5, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 18/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 два длинных предложения (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (10 unverified — сроки/пошлины; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, объём ~9355 ✓; −1 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title закрывают относительные основания и ответ экспертизе |
| C02 | ✓ | Lead — direct answer (уведомление vs отказ, п. 6–10) |
| C03 | ✓ | Заявитель на стадии экспертизы Роспатента |
| C04 | ✓ | Уведомление, ППС, однородность, письмо-согласие |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Основания → документы/сроки → календарь → реестры → согласие → перечень → ППС |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | КонсультантПлюс (ГК), klerk/Patent24, palatapp, Поисковая платформа |
| R03 | ✓ | 9 000 ₽, 6/4 мес. — из research-notes, без «% успеха ППС» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «три документа — три срока», не дубль L02 (претензия) |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA `/reg-tz-main` ×1, interlink L01 ×2 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | Brief/research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения согласия, не юрконсультация |
| Ept02 | ✗ | Canonical `/otkaz-v-registracii-…` ещё не на хостинге (до publish) |

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

- total: 8, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-10-20): consultant deep links (GET timeout) → корень ГК РФ; rospatent.gov.ru/dues (SSL) → klerk.ru; fips.ru/registers-web (403) → licensingrussia.ru + plain text fips.ru

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 46.3 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (12 extracted, 2 verified, 10 unverified в fact-bank)
- факты сверены с `research-notes.md` (ст. 1499/1500, 9 000 ₽, 6 мес.)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 5 внешних href (consultant/klerk/licensingrussia)
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish: canonical на хостинге

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
