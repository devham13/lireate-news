# QA: L38 proverit-brend-onlayn-unikalnost

date: 2026-11-07
score_total: 85/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 6, TL;DR + workflow, таблица рисков |
| GEO / citability | 25 | 22 | 4 слоя следа, «Делайте / не делайте», официальные источники |
| CORE-EEAT lite | 15 | 14 | 17/20 |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 за 3 предложения >25 слов |
| Fact safety | 15 | 13 | fact-check PASS (5/5 verified) |
| Contract HTML | 10 | 10 | linter PASS; char_count 9231 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — выполнен.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — онлайн-уникальность бренда: реестр, домен, соцсети |
| C02 | ✓ | Lead + TL;DR — домен ≠ ТЗ, четыре слоя |
| C03 | ✓ | Предприниматель до заявки и сайта |
| C04 | ✓ | searchplatform, ЕГРЮЛ, whois, ст. 1483 |
| O01 | ✓ | H2 по research action_outline |
| O02 | ✓ | Варианты → платформа → ФИПС → ЕГРЮЛ → whois → соцсети → сводка |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | Таблица, ol, blockquote |
| R01 | ✓ | Секции самодостаточны |
| R02 | ✓ | Consultant, egrul, reg.ru, online.rospatent, wipo |
| R03 | ✓ | 11.12.2023, 46 200 руб. — из источников |
| R04 | ✓ | FAQ: ответ в первом абзаце |
| E01 | ✓ | Угол vs L01/L29 (цифровой след, не глубина реестров) |
| E02 | ✓ | «Делайте / не делайте» |
| E03 | ✓ | CTA /reg-tz-main; interlink L01, L29, L18 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop keyword hits |
| Ept01 | ✓ | Дисклеймер, дата 07.11.2026 |
| Ept02 | ✗ | L10 на проде 404 → ссылка на рубрику category=12 |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| excalibur_blog_fact_checker.py | PASS | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | link-verify.json |
| excalibur_blog_html_linter.py | PASS | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | repo-wide |

## Link verify (fix cycle GEO QA)

- fips.ru/registers-web (403) → внутренняя ссылка L29 + plaintext registers-web
- rospatent FAQ (SSL) → online.rospatent.gov.ru
- fips.ru тарифы (403) → plaintext fips.ru
- TMview FAQ → WIPO Brand Database
- L10 `/domennoe-imya-nma-ili-net` (404) → `/news?num=2&category=12`

## Cannibalization

- WARNING: primary L38 совпадает со secondary L34 (100%) — у L38 фокус на 4-слойном онлайн-следе; не блокер.

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3 — не блокер при score ≥80
