# QA: L59 kak-dobavit-brend-na-wildberries-seller

date: 2026-11-13
score_total: 89/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, 2 таблицы, ol×2, угол «справочник WB vs ТЗ» |
| GEO / citability | 25 | 23 | TL;DR, blockquote-workflow, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 семь предложений >25 слов (часть — таблица/списки) |
| Fact safety | 15 | 12 | fact-check WARNING (3 unverified: «2 р.д.» и др.; сверено с research-notes) |
| Contract HTML | 10 | 9 | linter PASS, объём ~8928 ✓; −1 placeholder cover в теле (cover-агент) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — добавление бренда WB и ТЗ |
| C02 | ✓ | Lead — direct answer (ЛК, без ТЗ на старте) |
| C03 | ✓ | Селлер Wildberries |
| C04 | ✓ | Мои бренды, 120×50, модерация, представитель |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Проверка → создание → карточка → логотип → без ТЗ → представитель → календарь |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | seller.wildberries.ru, КонсультантПлюс, Поисковая платформа |
| R03 | ✓ | 46 200 ₽, 2/30 р.д. — research-notes; без «% успеха» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Фокус «только WB», отсылки L03/L18 без дубля |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA `/reg-tz-main` ×1, interlink L01 ×2, L03/L18/L27 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | Brief/research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, два слоя WB/Роспатент |
| Ept02 | ✗ | Canonical `/kak-dobavit-brend-na-wildberries-seller` ещё не на хостинге (до publish) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING (acceptable) | slop-detector-report.json |
| cannibalization | WARNING (acceptable) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 12, failed: 0
- fix cycle 1 (GEO QA): canonical_path L03/L18 → live `lireate_seo_url` (underscore); fips.ru 403 → base.garant.ru/408182169/

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 7
- Flesch RU: 61.4 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (11 extracted, 8 verified, 3 unverified)
- сроки модерации WB и представителя сверены с `research-notes.md` и seller.wildberries.ru
- see `fact-check-report.json`

## Cannibalization

- repo-wide WARNING (7); для L59 ожидаемо пересечение secondary с L03 («как проверить… вайлдберриз») и primary с L18 (75%) — дифференциация в тексте (только добавление в ЛК)
- see `cannibalization-report.json`

## FIX (GEO QA, 1 цикл)

1. Удалена служебная оговорка Wordstat/MCP (html-linter FAIL → PASS).
2. Internal L03/L18 → опубликованные slug на хостинге (link-verify FAIL → PASS).
3. Тариф ФИПС: ссылка на ГАРАНТ вместо fips.ru (403).

## Verdict

**PASS** — cover||schema разрешены.
