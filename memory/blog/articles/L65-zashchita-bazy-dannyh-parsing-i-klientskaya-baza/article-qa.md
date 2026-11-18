# QA: L65 zashchita-bazy-dannyh-parsing-i-klientskaya-baza

date: 2026-11-18
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, таблица×1, ol×8, TL;DR blockquote |
| GEO / citability | 25 | 23 | Три контура БД/КТ/ПДн, чек-лист 72 ч, схема профилактики, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; Flesch 57.1; 2 предложения >25 слов |
| Fact safety | 14 | 12 | fact-check PASS; 3/16 verified; цифры сверены с research-notes |
| Contract HTML | 12 | 12 | linter PASS, img×3+inline, char_count 9136 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — клиентская база, парсинг, ст. 1334 |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Владелец CRM/сайта до утечки |
| C04 | ✓ | ст. 1260, 1333–1334, 1335.1, 98-ФЗ, 152-ФЗ в первых блоках |
| O01 | ✓ | H2 по research action_outline |
| O02 | ✓ | Активы → изготовитель → ToS/1334 → КТ → техмеры → Роспатент → 72 ч → CTA |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol×8, blockquote×3, inline-collage×2 |
| R01 | ✓ | «Делайте / не делайте» в секциях |
| R02 | ✓ | Consultant, ГАРАНТ, Gardium, internal L23/L14/L32 |
| R03 | ✓ | 5 000 ₽, 62 дня, 10 000 элементов, 1311 — research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «клиентская база + парсинг» vs L23 generic БД |
| E02 | ✓ | Чек-лист и профилактика в каждом блоке |
| E03 | ✓ | Telegram CTA; L23/L14 backlinks |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 18.11.2026 |
| Ept02 | ✗ | primary «защита клиентской базы» близко к L23 — разведение через H1 и отсылки |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (legacy-пары; L65 не в списке) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 17, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix (GEO QA cycle 1): rospatent.gov.ru (SSL) → gosuslugi.ru/ЕПГУ; retry consultant 1262 после transient timeout

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 57.1 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (16 extracted, 3 verified, 13 unverified)
- unverified: статьи ГК, 72 ч, А56-128791/2022 — сверено с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (7 cross-topic warnings в репо; primary L65 «защита клиентской базы данных» не конфликтует с L23 primary в отчёте)
- **L65-specific:** acceptable (отсылки на L23/L14 в тексте)
- see `cannibalization-report.json`

## GEO QA edits

- `article.html`: rospatent.gov.ru → `https://www.gosuslugi.ru/` (ЕПГУ)
- `article.meta.json`: `char_count` 9136 (strip)