# QA: L13 mozhno-li-publikovat-foto-kartin-hudozhnika

date: 2026-10-22
score_total: 85/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, ol×8, 3 таблицы, blockquote TL;DR + маршрут + вердикт |
| GEO / citability | 25 | 23 | Два слоя прав, таблица цель/1274/1276, чек-лист, шаблон подписи |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 slop (3 предложения >25 слов) |
| Fact safety | 15 | 11 | fact-check WARNING (17 extracted, 2 verified); нормы ГК и музеи сверены с research-notes |
| Contract HTML | 10 | 6 | linter PASS, объём ~8.9k ✓; −4 нет `<img>` с alt (cover pending) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — фото картин, AP, чек-лист |
| C02 | ✓ | Lead + TL;DR — 1259, 1281, 1282, обзор ВС |
| C03 | ✓ | Блогер, SMM, куратор выставки |
| C04 | ✓ | 1274/1276, PD 70 лет, музейный copyright, ст. 1291 |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Слои → срок → источник → нормы → музеи → миф → чек-лист → CTA |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 3 таблицы, ol×8, blockquote×5 |
| R01 | ✓ | Standalone блоки в секциях и FAQ |
| R02 | ✓ | zakonrf.info, vsrf.ru, музеи, garant, ppt.ru |
| R03 | ✓ | Компенсация ст. 1301 с датой ред.; без выдуманных «чекеров» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от «проверь любую картинку» — живопись + файл |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA reg-tz, legacy L02, рубрика AP; ≤3 commercial |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юруслуга», дата 22.10.2026 |
| Ept02 | ✓ | Internal: legacy претензия, category=17, reg-tz |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | WARNING (acceptable) | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | PASS | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 19, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`, `--timeout 30`
- fix cycle 1: consultant.ru → zakonrf.info (таймауты/418 в Cloud); hermitage → ppt.ru; L02/L11 → live legacy slug и `/news?num=2&category=17`; `<pre><code>` → blockquote

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3
- Flesch RU: 61.0 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (17 extracted, 2 verified, 15 unverified)
- сверка: сроки PD, ст. 1274/1276, обзор ВС п. 7, условия Третьяковки/Пушкина — `research-notes.md`
- see `fact-check-report.json`

## Cannibalization

- verdict: PASS (0 issues)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1 (GEO QA): `article.html` — linter (`pre`/`code`), utility gate (+1 action marker), ссылки; `article.meta.json` — `title_seo`, `char_count`

## Optional (не blocker)

- `<img>` с alt после cover-агента
- canonical interlink L02/L11 после live-публикации slug

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
