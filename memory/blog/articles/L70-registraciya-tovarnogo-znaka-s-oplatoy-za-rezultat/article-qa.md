# QA: L70 registraciya-tovarnogo-znaka-s-oplatoy-za-rezultat

date: 2026-11-19
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, ol×2 (15+8 пунктов), 1 таблица, blockquote TL;DR + схема «три кошелька» |
| GEO / citability | 25 | 22 | 35 000 ₽ пошлины, таблица моделей, чек-лист 15 п., «Делайте / не делайте», сравнение success fee |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 slop (5 предложений >25 слов) |
| Fact safety | 15 | 11 | fact-check WARNING (11 extracted, 2 verified); сверка с research-notes |
| Contract HTML | 10 | 6 | linter PASS, ~8.8k знаков ✓; −4 нет `<img>` с alt (cover pending) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — оплата за результат, договор, чек-лист |
| C02 | ✓ | Lead + TL;DR — гонорар, госпошлины, ст. 1499 |
| C03 | ✓ | Предприниматель, заявитель, выбор патентного бюро |
| C04 | ✓ | МКТУ, поверенный, 316-ФЗ, ст. 1483/1499/1500 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Определение → пошлины → результат → модели → договор → риски → шаги |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица, ol×2, ul, blockquote×4 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | Госуслуги, ГАРАНТ, Консультант, research-notes |
| R03 | ✓ | Цифры пошлин с пунктами 2.1/2.4/2.11; без выдуманных гарантий % |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «три кошелька» и нейтральный чек-лист vs маркетинг бюро |
| E02 | ✓ | «Делайте / не делайте» в каждой H2 |
| E03 | ✓ | CTA услуга + сопровождение; ≤3 commercial блока |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, дата 19.11.2026, без 100% гарантии |
| Ept02 | ✓ | Internal: L01 canonical, L48, category=9 (L08 — текст) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | WARNING | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 10, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1: live L01 path; vozrazhenie L08 → текст; rospatent/consultant таймауты → Госуслуги, ГАРАНТ, zakonrf 1483; patent72/patenta → RBC

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 48.2 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (11 extracted, 2 verified, 9 unverified)
- сверка: пошлины 35 000 ₽, ст. 1483/1499/1500, 316-ФЗ — `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING (9 issues repo-wide, L70 не в списке конфликтов)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — канонические internal URL, устойчивые внешние зеркала, удалён мёртвый patent72

## Optional (не blocker)

- `<img>` с alt после cover-агента
- interlink на L08 после live slug

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry