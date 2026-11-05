# QA: L33 konkurent-zaregistriroval-pohozhiy-tovarnyy-znak

date: 2026-11-05
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×6, FAQ 7, ol×3 (15 шагов), 2 таблицы, TL;DR + workflow blockquote |
| GEO / citability | 25 | 23 | таблица целей ППС vs претензия, маршрут →, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 за 2 предложения >25 слов |
| Fact safety | 15 | 11 | fact-check PASS (17 extracted, 3 verified, 14 unverified; сверено с research-notes) |
| Contract HTML | 10 | 8 | linter PASS; `<img>` без `<figure>` до collage inject |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — конкурент зарегистрировал похожий ТЗ, ППС и претензия |
| C02 | ✓ | Lead + TL;DR — 1512/1513, 14 000 ₽, 30 дней, L08/L21 |
| C03 | ✓ | владелец бренда, in-house юрист |
| C04 | ✓ | ППС, МКТУ, свидетельство, ст. 1483–1515 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | цель → реестр → 1512 → ППС → претензия → суд/СИП |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, ol×3, blockquote×4 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | ConsultantPlus, klerk 2.28.4, ГАРАНТ Правила ППС, searchplatform |
| R03 | ✓ | 14 000 ₽, 5 лет, 30 дней, 3 месяца СИП — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «свидетельство уже в реестре» vs L19 «знак занят до подачи» |
| E02 | ✓ | «Сделайте / не делайте» по секциям |
| E03 | ✓ | CTA Telegram/WhatsApp; interlink L08, L21, L19 |
| Exp01 | ✓ | Режим B (workflow) |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 05.11.2026 |
| Ept02 | ✗ | slug L19 в meta с дефисами; live canonical с подчёркиваниями (исправлено в HTML) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (L08↔L21, не L33) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 17, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1: L19 `/chto-delat-…` 404 → `/chto_delat_esli_tovarnyy_znak_zanyat`; rospatent dues SSL → klerk.ru; fips ППС 403 → base.garant.ru Правила 644/261

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 54.7 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (17 extracted, 3 verified, 14 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L33 (0 issues на L33); repo WARN L08↔L21 — не блокер
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — whitelist HTML (`figure`→`img`+`p`), URL link-verify, marker «Сделайте» для utility gate (8 markers)

## Optional (не blocker)

- После cover-агента: collage inject может вернуть `<figure>` — повторный linter при необходимости

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
