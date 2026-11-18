# QA: L67 chestnyy-znak-import-prostymi-slovami

date: 2026-11-18
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×10, FAQ 7, 2 таблицы, ol×8, TL;DR blockquote |
| GEO / citability | 25 | 23 | разделение ЧЗ/ТЗ, маршрут blockquote, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 slop-клише; slop WARNING — 9 предложений >25 слов |
| Fact safety | 14 | 12 | fact-check PASS (3 extracted, 2 verified); −2 префиксы 460-469 без строки в fact-bank |
| Contract HTML | 10 | 10 | html-linter PASS, char_count ~8628 ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/primary — как пройти ЧЗ при импорте |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Импортёр-новичок |
| C04 | ✓ | ТН ВЭД, GTIN, КМ в первых блоках |
| O01 | ✓ | H2 = how-to цепочка |
| O02 | ✓ | От разведения ЧЗ/ТЗ → 8 шагов → ФТС → бренд |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, ol×8, blockquote |
| R01 | ✓ | Standalone секции |
| R02 | ✓ | markirovka.crpt.ru, markirovka.ru, КонсультантПлюс |
| R03 | ✓ | 50 коп./КМ, дата 18.11.2026 в lead |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «простыми словами» vs L22/L36 |
| E02 | ✓ | «Делайте / не делайте» |
| E03 | ✓ | reg-tz, Telegram, внешние гайды |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер таможня/патент |
| Ept02 | ✗ | Internal L22/L03/L36 на проде 404 → заменены на проверенные HTTPS URL |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | WARNING (допустимо) | slop-detector-report.json |
| cannibalization | WARNING (L67↔L22/L36 overlap) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify (fix cycle 1, 2026-11-18)

- total: 12, failed: 0
- IDN `честныйзнак.рф` → `markirovka.crpt.ru` (+ checking_codes)
- internal slug L22/L36/L03 (404 на проде) → markirovka.ru импорт, docs.crpt.ru, seller.wildberries.ru

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 9
- Flesch RU: 63.4 (Easy)

## Fact-check

- verdict: PASS (3 extracted, 2 verified, 1 unverified — 460-469 в FAQ, справочно)

## Cannibalization

- repo-wide WARNING L67 secondary ↔ L36/L22 (ожидаемо для кластера импорта)
- угол L67: базовый how-to без troubleshooting L36

## GEO QA FIX

- `article.html`: только ссылки (не рерайт текста)