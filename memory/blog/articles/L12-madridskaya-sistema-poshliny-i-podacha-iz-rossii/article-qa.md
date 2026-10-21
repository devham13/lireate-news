# QA: L12 madridskaya-sistema-poshliny-i-podacha-iz-rossii

date: 2026-10-21
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, 4 таблицы, blockquote TL;DR + вердикт |
| GEO / citability | 25 | 23 | Таблицы пошлин/сроков, пример Китай+CHF, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 slop (2 предложения >25 слов, таблица) |
| Fact safety | 15 | 12 | fact-check PASS (7 verified / 5 unverified; сверено с research-notes) |
| Contract HTML | 10 | 6 | linter PASS, объём ~8.8k ✓; −4 нет `<img>` с alt (cover pending) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — Мадрид, подача из России, пошлины |
| C02 | ✓ | Lead + TL;DR — п. 4.14, CHF, дизайнации |
| C03 | ✓ | Владелец бренда с базой в РФ, экспорт |
| C04 | ✓ | ММ2, базовый знак, центральная атака, ст. 5 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Сравнение → база → документы → пошлины → оплата → сроки → риски → CTA |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 4 таблицы, blockquote×3 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | WIPO, приказ № 161, Notice 9/2026 |
| R03 | ✓ | Суммы с датой 21.10.2026, курс CHF не выдуман |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от рефератов — две кассы, пример Китая |
| E02 | ✓ | «Делайте / не делайте» в H2 |
| E03 | ✓ | CTA Китай + reg-tz, interlink L01/L06, ≤3 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата проверки норм |
| Ept02 | ✓ | Internal: L01, reg-tz, Китай; МКТУ — классификатор Роспатента (L06 slug для indexer) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | PASS | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 14, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 60`
- fix cycle 1: п. 4.14 → `pravo.ppt.ru` (SSL rospatent.gov.ru); L06 interlink → классификатор Роспатент (slug L06 ещё 404 на проде)

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 66.1 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (12 extracted, 7 verified, 5 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: правки `article.html` (п. 4.14 URL, классы МКТУ — online.rospatent)

## Optional (не blocker)

- `<img>` с alt после cover-агента
- meta_ab.title_seo WARN utility gate (ключи primary_query частично в title_aeo)

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
