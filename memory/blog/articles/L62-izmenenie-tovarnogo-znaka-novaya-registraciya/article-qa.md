# QA: L62 izmenenie-tovarnogo-znaka-novaya-registraciya

date: 2026-11-17
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×7 (+FAQ), FAQ×6, таблицы×3, ol×2, TL;DR blockquote |
| GEO / citability | 25 | 23 | Три стадии 1497/1505/1486; п. 69 Правил № 482; таблица веток 2.16 vs 2.1–2.11 |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop; Flesch 52.9 Standard; 6 предложений >25 слов (таблицы/TL;DR) |
| Fact safety | 14 | 11 | fact-check PASS; 3/12 в fact-bank, остальное — research-notes / НПА |
| Contract HTML | 12 | 10 | linter PASS, ~8928 знаков; cover — шаг 4 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — новая заявка vs п. 2.16 |
| C02 | ✓ | Lead + TL;DR answer-first |
| C03 | ✓ | Заявитель, правообладатель, селлер, франшиза |
| C04 | ✓ | 1497, 1505, 1486, п. 69, 2.16/2.17 в первых блоках |
| O01 | ✓ | H2: развилка → стадия → существенность → сравнение → алгоритм → ошибки |
| O02 | ✓ | Логичный outline comparison mode B |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | Таблицы×3, ol×2, blockquote |
| R01 | ✓ | Standalone блоки «Делайте / не делайте» |
| R02 | ✓ | Consultant, Гарант СИП, searchplatform, Госуслуги, ПП 941 |
| R03 | ✓ | 3 000 ₽ / 2 000 ₽, 75 раб. дней из research |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «три стадии» vs generic «внести изменения» |
| E02 | ✓ | Практика в каждой H2 |
| E03 | ✓ | CTA `/registraciya_tovarnogo_znaka/`, ≤3 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, не индивидуальная консультация |
| Ept02 | ✗ | L02 live slug underscore (не canonical slug) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | WARNING | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (legacy-пары; не L62) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 15, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix (GEO QA cycle 1): ст. 1505 → consultant hash a8c5…; rospatent dues SSL → ПП 941; госуслуга изменений → gosuslugi.ru; L02 → live underscore slug

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 6
- Flesch RU: 52.9 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (12 extracted, 3 verified, 9 unverified)
- нормы ГК и пошлины сверены с `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (7 legacy cross-topic warnings; L62 primary не в списке)
- see `cannibalization-report.json`