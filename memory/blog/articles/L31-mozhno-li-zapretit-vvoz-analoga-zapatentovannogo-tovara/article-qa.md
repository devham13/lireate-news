# QA: L31 mozhno-li-zapretit-vvoz-analoga-zapatentovannogo-tovara

date: 2026-11-04
score_total: 84/100
core_eeat_lite: 18/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×7, FAQ 6, ol×2 (чек-лист + маршрут), 2 таблицы, TL;DR + итоговый blockquote |
| GEO / citability | 25 | 22 | таблица «патент vs ТРОИС vs суд», чек-лист 6 шагов, FAQ с первым ответом |
| CORE-EEAT lite | 15 | 13 | 18/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 за 5 предложений >25 слов (таблица в plain-text slop) |
| Fact safety | 15 | 11 | fact-check PASS (13 extracted, 3 verified, 10 unverified; сверено с research-notes) |
| Contract HTML | 10 | 8 | linter PASS, char_count 8872 ✓; cover `<img>` без `<figure>` до collage inject |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 18/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — ввоз аналога, таможня, патент vs ТРОИС |
| C02 | ✓ | Lead + TL;DR — 1358, ТРОИС не для патента, 7–10 дней по знаку |
| C03 | ✓ | патентообладатель, импортёр, юрист компании |
| C04 | ✓ | ГК 1358/1359/1477, 289-ФЗ, Поисковая платформа, ТКС |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | классификация → патент/перечень → ТРОИС → суд + чек-лист |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | 2 таблицы, ol, blockquote×4 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | ConsultantPlus, ipbot, patent-family, searchplatform, azalesov |
| R03 | ✓ | 8000+ в ТРОИС, 7–10 дн., ~300 000 ₽ страхование — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «патент не на таможне» vs SERP про параллельный импорт |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA `/patent`, Telegram/WhatsApp; interlink L05 (interim) |
| Exp01 | ✓ | Режим B (comparison) |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 04.11.2026 |
| Ept02 | ✗ | L05 canonical `/sposoby-zashchity-izobreteniya` → 404 на проде; interim `/news?num=2&category=20` |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (L08↔L21, не L31) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 17, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 30`
- fix cycle 1: zhelezno.com (500) → ipbot.ru; customs.gov.ru (SSL timeout) → tks.ru/db/ois; fips registers-web (403) → searchplatform.rospatent.gov.ru/patents; L05 slug 404 → `/news?num=2&category=20` (interim до live L05)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 47.7 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (13 extracted, 3 verified, 10 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L31 (0 issues на L31); repo WARN L08↔L21 — не блокер
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — замена недоступных external/internal URL для link-verify PASS

## Optional (не blocker)

- После live L05: заменить `/news?num=2&category=20` на `/sposoby-zashchity-izobreteniya`
- После cover-агента: повторный linter после collage inject при необходимости

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (6) | HowTo: no | Review: no | author_id: pending registry
