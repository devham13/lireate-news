# QA: L22 markirovka-importa-chestnyy-znak-i-tovarnyy-znak

date: 2026-10-30
score_total: 88/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, таблицы×2, ol×7, TL;DR blockquote |
| GEO / citability | 25 | 23 | три слоя ЧЗ/ТЗ/импорт, «Делайте / не делайте», FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 четыре предложения >25 слов |
| Fact safety | 15 | 13 | fact-check PASS (4 extracted, 2 verified); −2 2 unverified (сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, объём ~8.7k ✓; −1 нет `<img>` с alt (cover после cover-агента) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — честный знак импорт, чек-лист бренда |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Импортёр с собственным брендом |
| C04 | ✓ | КМ, GTIN, ГИС МТ в первых абзацах |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Разведение слоёв → группа → 7 шагов → ТЗ/НК → таможня → ТРОИС → штрафы → ошибки |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol×7, ul, blockquote |
| R01 | ✓ | Standalone блоки в секциях |
| R02 | ✓ | markirovka.ru, КонсультантПлюс, astral.ru, searchplatform |
| R03 | ✓ | 50 коп./КМ, 15.12 КоАП, даты ПП №656 — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «три независимых слоя» vs SERP |
| E02 | ✓ | «Делайте / не делайте» в H2 |
| E03 | ✓ | reg-tz ×1, L01 чек-лист, рубрика category=15 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не таможенная/патентная консультация, дата 30.10.2026 |
| Ept02 | ✗ | Slug L03 404 на live → WB instruction + seller-edu.ozon.ru; вернуть internal после publish L03 |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | WARNING (acceptable, L08↔L21 repo-wide) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 13, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`
- fix cycle 1 (2026-10-30): удалён `<figure>`; internal L03 slug 404 → `seller.wildberries.ru` instruction + текст Ozon seller-edu

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 66.1 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (4 extracted, 2 verified, 2 unverified)
- unverified сверены с `research-notes.md` (тариф КМ, сроки ЕАЭС)
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING — L08 ↔ L21 overlap 83% (не L22; acceptable repo-wide)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — удаление cover `<figure>`; замена 404 internal L03 на внешние инструкции маркетплейсов
- cycle 2: не требовался

## Optional (не blocker)

- `<img>` с alt после cover-агента
- после publish L03: вернуть interlink `/kak-zaregistrirovat-brend-na-ozon-i-wildberries`

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
