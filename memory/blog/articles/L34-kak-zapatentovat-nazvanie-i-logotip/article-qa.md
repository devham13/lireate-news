# QA: L34 kak-zapatentovat-nazvanie-i-logotip

date: 2026-11-05
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, ol×6, таблица патент/©/ТЗ, TL;DR + workflow blockquote |
| GEO / citability | 25 | 23 | таблица инструментов, 6 шагов проверки, «Делайте / не делайте», FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 slop (4 предложения >25 слов, в т.ч. таблица) |
| Fact safety | 15 | 12 | fact-check PASS (14 extracted, 3 verified); нормы сверены с research-notes |
| Contract HTML | 10 | 7 | linter PASS; `<img>` без `<figure>` до collage inject; объём ~8.7k ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — запатентовать логотип и название |
| C02 | ✓ | Lead + TL;DR — ст. 1350, 1259, 1477, 35 000 ₽ |
| C03 | ✓ | ИП и малый бизнес, дизайнер, ЕГРЮЛ |
| C04 | ✓ | патент, ©, ТЗ, МКТУ, комбинированный знак |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | патент vs ТЗ → таблица → название → логотип → комбо → проверка → бюджет → решение |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица, ol×6, blockquote×4, ul×1 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | consultant.ru, searchplatform, klerk/patent24, research-notes |
| R03 | ✓ | 35 000 ₽ с п. 2.1/2.4/2.11; без «регистрация 0 ₽» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | «патент» в поиске ≠ ТЗ; © не на слово; миф «бесплатно» |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA `/reg-tz-main`; ≤3 commercial |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, дата 05.11.2026, нет гарантии экспертизы |
| Ept02 | ✓ | L01, L29, L30, L06 (`/mktu`) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (L08↔L21, не L34) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 14, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1: `/kak-opredelit-klass-mktu` 404 → `/mktu`; rospatent.gov.ru SSL → klerk.ru/patent24; fips registers-web 403 → internal L29; FAQ rospatent → L29

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 54.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (14 extracted, 3 verified, 11 unverified)
- сверка: ст. 1259, 1350, 1477, 1483, 1486, 1491, 1515, пошлины 35 000 ₽ — `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L34 (0 issues на L34); repo WARN L08↔L21 — не блокер
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — whitelist HTML (`figure`→`<p><img></p>`), URL link-verify (L06 `/mktu`, klerk, L29 вместо fips/rospatent.gov.ru)

## Optional (не blocker)

- После cover-агента: collage inject может вернуть `<figure>` — повторный linter при необходимости

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
