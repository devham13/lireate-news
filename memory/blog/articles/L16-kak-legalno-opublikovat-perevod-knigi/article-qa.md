# QA: L16 kak-legalno-opublikovat-perevod-knigi

date: 2026-10-23
score_total: 83/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 17 | H2×9, FAQ 7, ol×7, таблица слоёв прав, blockquote TL;DR + маршрут + шаблон письма |
| GEO / citability | 25 | 22 | три слоя прав, чек-лист, 7 шагов, «Делайте / не делайте», шаблон лицензии |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 slop (4 предложения >25 слов) |
| Fact safety | 15 | 12 | fact-check WARNING (14 extracted, 1 verified); нормы сверены с research-notes |
| Contract HTML | 10 | 6 | linter PASS, объём ~8.5k ✓; −4 нет `<img>` с alt (cover pending) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — легальная публикация перевода книги |
| C02 | ✓ | Lead + TL;DR — ст. 1260, 1270, 1229, 1273 |
| C03 | ✓ | Переводчик, издатель, правообладатель |
| C04 | ✓ | ст. 1260–1270, 1281–1282, 1286, 1301 ГК РФ |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Слои → срок → лицензия → шаги → риски сети → ТЗ vs текст → чек-лист |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица, ol×7, blockquote×4 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | zakonrf, garant, avtoram, id.hse, habr |
| R03 | ✓ | Компенсация ст. 1301 с диапазоном; без выдуманных сервисов |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Разведение литперевода и финансовой «перевод»-выдачи |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA Лирейт, legacy L02; ≤3 commercial |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 23.10.2026 |
| Ept02 | ✓ | Internal: legacy претензия; внешние L11/L13 через рабочие URL |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | WARNING | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | PASS | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 24, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 20`
- fix cycle 1: consultant.ru → zakonrf.info; ficbook/AO3/institutperevoda → habr/temofeev; internal slug → legacy L02 URL; L11/L13 → art.etopravo / id.hse

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 47.7 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (14 extracted, 1 verified, 13 unverified)
- сверка: ст. 1260, 1270, 1229, 1273, 1281–1282, 1286, 1301 — `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — whitelist HTML (шаблон письма в `<blockquote>`+`<p>`), ссылки НПА и внешние/внутренние URL для Cloud link-verify, +1 знак объёма

## Optional (не blocker)

- `<img>` с alt после cover-агента
- canonical interlink L11/L13 после live-публикации slug

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
