# QA: L53 vozrazhenie-v-pps-na-pravovuyu-ohranu-tz

date: 2026-11-12
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×7, FAQ 7, 3 таблицы, ol×9, узкий угол ППС / ст. 1513 |
| GEO / citability | 25 | 23 | TL;DR, blockquote-схема, матрица ст. 1512, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 15 | 0 AI-slop hits, 0 длинных предложений (>25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (19 unverified; сверено с research-notes) |
| Contract HTML | 10 | 7 | linter PASS, объём ~9k ✓; −3 нет `<img>` с alt (cover после QA) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — возражение в ППС, правовая охрана, сроки |
| C02 | ✓ | Lead + TL;DR — 1493 / 1500 / 1513 |
| C03 | ✓ | Заинтересованное лицо, третье лицо |
| C04 | ✓ | ст. 1512–1513, 1483, 14 000 ₽, 5 лет, 2.28.4 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Реестр → основание → заинтересованность → подача → коллегия |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 3 таблицы, ol×9, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | КонсультантПлюс, ГАРАНТ, Поисковая платформа, klerk |
| R03 | ✓ | Суммы и сроки из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L08 (1493), L07 (1500), L21 (карта) |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA Telegram/WhatsApp/MAX; interlink L01 чек-лист, L21, legacy L08 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, без обещаний исхода ППС |
| Ept02 | ✗ | Interlink на kebab-slug L07/L08 отложен до publish; live legacy URL |

## Script reports

| Скрипт | Verdict | exit | Файл |
|--------|---------|------|------|
| fact-check | WARNING (acceptable) | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo; L53↔L08 secondary 83%, ожидаемо) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 16, failed: 0
- site-base: публичный домен Lireate (`--site-base`, `LIREATE_PUBLIC_SITE_URL`)

## GEO QA fixes applied (fix cycle 1, 2026-11-12)

1. Internal L08/L07 kebab-slug (404) → live legacy `/vozrazhenie_protiv_registracii_chuzhogo_tovarnogo_znaka_sroki_i_poryadok/`, `/otnositelnyie_osnovaniya_otkaza_v_registracii_tz_otvet_ekspertize/`.
2. `fips.ru` (403) → ГАРАНТ п. 4 + licensingrussia (реестры).
3. `rospatent.gov.ru/dues` (SSL fail в Cloud) → klerk.ru (2.28.4).
4. `max.ru` deep link (403) → `https://max.ru/`.

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 0
- Flesch RU: 58.6 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (22 extracted, 3 verified, 19 unverified)
- факты сверены с `research-notes.md` (ст. 1493/1500/1512–1513, 14 000 ₽, 5 лет, 10 раб. дн.)
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING at repo level; **L53 primary** «возражение в ппс на предоставление правовой охраны» не дублирует L08/L21 (узкий ППС/1513) — зафиксировано в research-notes
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — правки href в `article.html`
- cycle 2: не требовался

## Optional (не blocker)

- `<img>` с alt — cover-агент после QA
- после publish L07/L08: вернуть interlink на канонические slug из `article.meta.json`

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry

## Gate

**PASS** — директор может запускать cover || schema.
