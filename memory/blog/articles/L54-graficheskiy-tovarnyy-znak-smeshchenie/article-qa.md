# QA: L54 graficheskiy-tovarnyy-znak-smeshchenie

date: 2026-11-12
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, таблицы матрицы п. 43 и решений, режим B |
| GEO / citability | 25 | 23 | TL;DR, blockquote, матрица 5 признаков, answer-first FAQ |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; 3 предложения >25 слов (некритично) |
| Fact safety | 15 | 13 | fact-check PASS (4 verified, 2 unverified в отчёте) |
| Contract HTML | 10 | 8 | linter PASS, объём ~8.8k; `<img>` — cover после QA |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — графический знак, смешение, до подачи |
| C02 | ✓ | Lead + TL;DR — п. 43, Поисковая платформа, ст. 1497 |
| C03 | ✓ | Владелец макета, дизайнер, правообладатель |
| C04 | ✓ | п. 43–46, 1483, 1497, 46 200 ₽, 11.12.2023 |
| O01 | ✓ | H2 = troubleshooting-цепочка research |
| O02 | ✓ | файлы → поиск → п. 43 → однородность → правки → решение |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблицы, ol, blockquote |
| R01 | ✓ | Standalone блоки в секциях |
| R02 | ✓ | КонсультантПлюс, ГАРАНТ, searchplatform |
| R03 | ✓ | research-notes / fact-check |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка L01 / L39 / L38 / L07 |
| E02 | ✓ | «Делайте / не делайте» в правках макета |
| E03 | ✓ | CTA Telegram/WhatsApp/MAX; interlink L01, L39, L38, L07 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, без гарантии регистрации |
| Ept02 | ✗ | utility gate WARN: «роспатент» не в title_seo (есть в title_aeo/primary) |

## Script reports

| Скрипт | Verdict | exit | Файл |
|--------|---------|------|------|
| fact-check | PASS | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo-level; L54 не в списке) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 15, failed: 0
- site-base: публичный домен Lireate (`LIREATE_PUBLIC_SITE_URL`)

## GEO QA fixes applied (fix cycle 1, 2026-11-12)

1. Удалена служебная оговорка Wordstat/MCP из блока «Достоверность данных» (html-linter).
2. `www1.fips.ru` / дублирующий path (403) → КонсультантПлюс [Правила № 482](https://www.consultant.ru/document/cons_doc_LAW_184868/354796ff2127929e8ba2ec52fa49605433f56508/).
3. `rospatent.gov.ru` FAQ (SSL fail в Cloud) → garant.ru/news/1664018 (Вена + платформа).
4. `www.fips.ru` прейскурант (403) → base.garant.ru/408182169.

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3
- Flesch RU: 54.5 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (6 extracted, 4 verified, 2 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING at repo level only; primary L54 не пересекается с L01/L39 по intent (research-notes)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — правки `article.html`
- cycle 2: не требовался

## Optional (не blocker)

- `<img>` с alt — cover-агент после QA
- meta_ab.title_seo: при желании добавить «Роспатент» до publish (utility WARN)

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry

## Gate

**PASS** — директор может запускать cover || schema.
