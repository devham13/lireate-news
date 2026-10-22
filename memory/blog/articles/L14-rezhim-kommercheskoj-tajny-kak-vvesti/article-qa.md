# QA: L14 rezhim-kommercheskoj-tajny-kak-vvesti

date: 2026-10-22
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×10, FAQ 7, ol×7, 3 таблицы, blockquote TL;DR + маршрут + цепочка доказывания |
| GEO / citability | 25 | 23 | 5 мер ст. 10, таблица ответственности, чек-листы режима/инцидента, «Делайте / не делайте» |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 slop (5 предложений >25 слов) |
| Fact safety | 15 | 12 | fact-check PASS (12 extracted, 2 verified); нормы сверены с research-notes |
| Contract HTML | 10 | 6 | linter PASS, объём ~9.2k ✓; −4 нет `<img>` с alt (cover pending) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — режим КТ, 5 мер, доказательства |
| C02 | ✓ | Lead + TL;DR — ст. 3, 10, цепочка спора |
| C03 | ✓ | Собственник, HR, руководитель |
| C04 | ✓ | 98-ФЗ, ТК 193, КоАП 13.14, УК 183 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Критерии КТ → 5 мер → внедрение → передача vs разглашение → комиссия → суд → ответственность |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 3 таблицы, ol×7, blockquote×4 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | garant, zakonrf, ppt.ru, delo-press, freshdoc |
| R03 | ✓ | Штрафы КоАП с диапазонами; без выдуманных «чекеров» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Две линии: внедрение + доказывание (не только NDA) |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA legacy L02, рубрика category=15; ≤3 commercial |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 22.10.2026 |
| Ept02 | ✓ | Internal: legacy претензия ТЗ, /news?category=15 |

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

- total: 15, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 25`
- fix cycle 1: consultant.ru → base.garant.ru / zakonrf.info (таймауты в Cloud); kdelo.ru 302 → delo-press.ru

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 55.6 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (12 extracted, 2 verified, 10 unverified)
- сверка: 5 мер ст. 10, ст. 5, п. 6/9 ст. 3, ст. 193 ТК, штрафы 13.14 — `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — внешние ссылки НПА и delo-press вместо consultant/kdelo

## Optional (не blocker)

- `<img>` с alt после cover-агента
- canonical interlink L02 после live-публикации slug

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
