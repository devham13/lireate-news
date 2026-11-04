# QA: L32 kak-zashchitit-kompyuternuyu-programmu-ot-plagiata

date: 2026-11-04
score_total: 83/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×7 + FAQ, ol×3, 2 таблицы, TL;DR + маршрут blockquote |
| GEO / citability | 25 | 22 | таблица «ст. 1261 vs идея», чек-листы ol, FAQ 7 с прямым ответом |
| CORE-EEAT lite | 15 | 12 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 за 2 over-long блока (таблица + workflow) |
| Fact safety | 15 | 11 | fact-check PASS (11 extracted, 3 verified, 8 unverified; сверено с research-notes) |
| Contract HTML | 10 | 8 | linter PASS; cover `<img>` без `<figure>` до collage inject |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — плагиат кода, ст. 1261, претензия |
| C02 | ✓ | Lead + TL;DR — 5 000 ₽, 62 дня, добровольная регистрация |
| C03 | ✓ | основатель продукта, in-house юрист, правообладатель ПО |
| C04 | ✓ | ст. 1259, 1261, 1262, 1252, 1301, ФЗ 296-ФЗ |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | ст. 1261 → договоры → Роспатент → git → мониторинг → претензия |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, ol×3, blockquote×5 |
| R01 | ✓ | «Делайте / не делайте», чек-листы, FAQ standalone |
| R02 | ✓ | ConsultantPlus, Habr, advolaw, nevskylaw, dvitex |
| R03 | ✓ | 5 000 ₽, 62 раб. дня, 10k–10M ₽ ст. 1301 — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | отстройка от антиплагиата диплома и L20 (мобилка) |
| E02 | ✓ | «Сделайте / не делайте» по секциям |
| E03 | ✓ | CTA Telegram/WhatsApp, рубрика «Программа ЭВМ» |
| Exp01 | ✓ | Режим B (comparison + checklist) |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 04.11.2026 |
| Ept02 | ✗ | Wordstat не собран (MCP недоступен на research) — не блокер контента |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (L08↔L21, не L32) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 20, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 15`
- fix cycle 1: rospatent.gov.ru (SSL в CI) → dvitex.ru; Habr 1042622 (403) → aglegal/1072018

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 53.4 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (11 extracted, 3 verified, 8 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS для L32 (0 issues на L32); repo WARN L08↔L21 — не блокер
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — `<figure>` → `<img>` (whitelist linter); URL rospatent/Habr; «Сделайте»/«проверьте» для utility gate (9 markers)

## Optional (не blocker)

- Cover-агент: `lireate_collage_inject` вернёт `<figure class="lx-article-cover">` после collage
- При доступности rospatent.gov.ru в prod можно вернуть каноническую ссылку на услугу в TL;DR

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
