# QA: L30 kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026

date: 2026-11-04
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, ol×5, 3 таблицы, TL;DR + маршрут |
| GEO / citability | 25 | 23 | таблица пошлин 2.1/2.4/2.11, DIY vs бюро, «Делайте / не делайте» |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 три предложения >25 слов |
| Fact safety | 15 | 12 | fact-check PASS (9 verified, 15 unverified; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, char_count 8618 ✓; cover `<img>` без `<figure>` до collage inject |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — DIY регистрация ТЗ 2026, пошлины, сроки |
| C02 | ✓ | Lead + TL;DR — цепочка L01/L29 → МКТУ → заявка → экспертиза |
| C03 | ✓ | ИП, ООО, физлицо без поверенного |
| C04 | ✓ | online.rospatent, УКЭП, 2.1/2.4/2.11, ст. 1492/1499/1483 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Заявитель → проверка → МКТУ → подача → пошлины → экспертиза → уведомление → свидетельство |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 3 таблицы, ol×5, blockquote×3 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | Поисковая платформа, klerk (пошлины), Госуслуги, КонсультантПлюс |
| R03 | ✓ | 35 000 ₽, 18 мес. + 2 нед., 6 мес. на ответ — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол DIY-карта vs L29 (проверка) и L07 (уведомление) |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA reg-tz-main, Telegram/WhatsApp; interlink L01/L29/L19/L25/L03 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 04.11.2026 |
| Ept02 | ✗ | L07 canonical slug ещё 404 на проде → interim `/news?num=2&category=9`; L06 → `/mktu` |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | PASS (WARN других статей) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 18, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 30`
- fix cycle 1: rospatent.gov.ru (SSL Cloud) → klerk.ru + gosuslugi.ru/life/details/registraciya_tovarnogo_znaka; fips МКТУ (403) → классификатор online.rospatent; L06 slug 404 → `/mktu`; L19 → live SEO URL; L07 slug 404 → `/news?num=2&category=9`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3
- Flesch RU: 54.7 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (24 extracted, 9 verified, 15 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L30 (0 issues на L30); repo WARN L08↔L21 — не блокер
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — whitelist HTML (cover `<img>`), link-verify URLs; `article.meta.json` — char_count 8618

## Optional (не blocker)

- После cover-агента: collage-v1 может вернуть `<figure>` — повторный linter после inject или whitelist в gate collage
- После live L07: заменить `/news?num=2&category=9` на canonical `/otkaz-v-registracii-…`

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
