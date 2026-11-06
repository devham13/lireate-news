# QA: L37 zashchita-dizayna-upakovki-marketpleysy

date: 2026-11-06
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, TL;DR + workflow, таблица |
| GEO / citability | 25 | 23 | «Делайте / не делайте», ссылки на ГК РФ и сервисы Роспатента |
| CORE-EEAT lite | 15 | 14 | 17/20 |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 из‑за 6 предложений >25 слов (slop WARNING) |
| Fact safety | 15 | 12 | fact-check PASS; часть метрик в unverified |
| Contract HTML | 10 | 9 | linter PASS; char_count 8752 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — выполнен.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — защита дизайна упаковки на МП: ©, ПО, ТЗ |
| C02 | ✓ | Lead + TL;DR — три слоя прав |
| C03 | ✓ | Селлер / бренд на WB |
| C04 | ✓ | ст. 1259/1352/1354/1363/1483 + платформы Роспатента |
| O01 | ✓ | H2 по research action_outline |
| O02 | ✓ | Макет → реестры → ПО → ТЗ → ЛК → жалоба |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol, blockquote |
| R01 | ✓ | Секции самодостаточны |
| R02 | ✓ | Consultant, zakonrf, searchplatform, online.rospatent, WB, klerk |
| R03 | ✓ | 5/25 лет, 12 мес. льготы — из норм |
| R04 | ✓ | FAQ: ответ в первом абзаце |
| E01 | ✓ | Угол vs L26/L18 |
| E02 | ✓ | «Делайте / не делайте» |
| E03 | ✓ | CTA рубрика /news category=12; interlink /mktu, L18, L26 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop keyword hits |
| Ept01 | ✓ | Дисклеймер, дата 06.11.2026 |
| Ept02 | ✗ | L06 slug на проде 404 → внутренняя ссылка `/mktu` (как в L30) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| excalibur_blog_html_linter.py | PASS | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | link-verify.json |
| excalibur_blog_slop_detector.py | WARNING | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (другие статьи) | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | repo-wide |

## Link verify (fix cycle GEO QA директора)

- rospatent FAQ (SSL в Cloud) → ст. 1354 zakonrf.info
- fips.ru (403) → searchplatform industrial + online.rospatent.gov.ru
- Внутренние: L06 → `/mktu`; L18 → `lireate_seo_url` подчёркивания

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 6 — не блокер при score ≥80
