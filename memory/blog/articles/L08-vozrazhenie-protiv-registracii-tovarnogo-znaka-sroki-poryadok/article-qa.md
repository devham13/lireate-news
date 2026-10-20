# QA: L08 vozrazhenie-protiv-registracii-tovarnogo-znaka-sroki-poryadok

date: 2026-10-20
score_total: 90/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×7, FAQ 7, 2 таблицы, ol×8, угол «две дороги — 1493 vs 1512» |
| GEO / citability | 25 | 23 | TL;DR, workflow blockquote, таблица стадий, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 два длинных предложения (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (18 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, объём ~9k ✓; −1 нет `<img>` с alt |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — возражение против чужой регистрации, сроки |
| C02 | ✓ | Lead + TL;DR — обращение vs ППС |
| C03 | ✓ | Третье лицо / заинтересованный правообладатель |
| C04 | ✓ | ст. 1493, 1512–1513, 1483 п. 6, 14 000 ₽ |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Стадия → обращение → ППС → пошлина → доказательства → коллегия |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | КонсультантПлюс, ГАРАНТ, Поисковая платформа, klerk |
| R03 | ✓ | 14 000 ₽, 5 лет, 10 раб. дн. отзыва — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от ст. 1500 (своя заявка) и L02 (претензия) |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA защита знака ×1, interlink L01 чек-лист ×2 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, без обещаний исхода ППС |
| Ept02 | ✗ | Interlink на L07 отложен до publish (canonical 404); ст. 1500 — consultant |

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
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-10-20): L07 internal 404 → ст. 1500 consultant; fips 403 → licensingrussia; rospatent dues SSL → klerk; consultant deep links (timeout) → корень ГК РФ

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 52.4 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (21 extracted, 3 verified, 18 unverified)
- факты сверены с `research-notes.md` (ст. 1493/1499/1512–1513, 14 000 ₽, 5 лет)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — 8 правок href в `article.html`
- cycle 2: не требовался

## Optional (не blocker)

- добавить `<img>` с alt по контракту
- после publish L07: вернуть interlink на `/otkaz-v-registracii-tovarnogo-znaka-otnositelnye-osnovaniya`

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
