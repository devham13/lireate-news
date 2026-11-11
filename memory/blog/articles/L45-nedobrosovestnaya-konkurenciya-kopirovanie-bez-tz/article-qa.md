# QA: L45 nedobrosovestnaya-konkurenciya-kopirovanie-bez-tz

date: 2026-11-11
score_total: 85/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS
fix_cycles: 1

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ H3×6, 2 таблицы, 3 `<ol>` (21 шаг), TL;DR blockquote |
| GEO / citability | 25 | 23 | Таблица «элемент → основание → канал», развилка 135-ФЗ 14.6 vs КоАП 14.6, workflow blockquote |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 slop-клише; 3 предложения >25 слов (slop PASS) |
| Fact safety | 15 | 11 | fact-check PASS (14 extracted, 3 verified, 11 unverified) |
| Contract HTML | 10 | 10 | html-linter PASS; `char_count` ≈8881 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/troubleshooting: копирование карточки без ТЗ, 14.6, ФАС |
| C02 | ✓ | Lead + TL;DR: 1301, 1253.1, 14.6 135-ФЗ, 14.33 КоАП |
| C03 | ✓ | Селлер WB/Ozon, владелец бренда без свидетельства |
| C04 | ✓ | 135-ФЗ, ГК 1301/1253.1, КоАП 14.33, практика ФАС |
| O01 | ✓ | H2 = research action_outline (фиксация, МП, претензия, УФАС) |
| O02 | ✓ | Диагностика → фиксация → МП → претензия → УФАС → 14.33 → ТЗ/ПО |
| O03 | ✓ | FAQ 6 |
| O04 | ✓ | Таблица×2, blockquote×3, ol×21 |
| R01 | ✓ | «Сделайте / не делайте» по секциям |
| R02 | ✓ | consultant.ru, zhelezno.com, vitvet.com — research-notes |
| R03 | ✓ | Суммы 1301, 14.33, оговорка не консультация; Вордстат не запрашивался |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «без ТЗ» vs L27 (с свидетельством); L37 упаковка; L24 клон |
| E02 | ✓ | Матрица элементов, сравнительная логика допустимого сходства |
| E03 | ✓ | CTA `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti/` |
| Exp01 | ✓ | Режим B (troubleshooting + workflow) |
| Exp02 | ✓ | research-notes в каталоге |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Блок «Материал проверен» |
| Ept02 | ✗ | −1: MAX deep-link 403 в CI → корень max.ru |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo L08↔L21, L22↔L36, L34↔L38; не L45) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 15, failed: 0
- site-base: публичный домен Lireate (`LIREATE_PUBLIC_SITE_URL` при verify)
- fix cycle 1: L37 slug hyphen (404) → live `lireate_seo_url` `/zashchita_dizayna_upakovki_marketpleysy/`; max.ru deep profile (403) → `https://max.ru/`

## GEO QA fixes applied (fix cycle 1)

1. Внутренняя ссылка L37 → SEO URL с подчёркиваниями (200).
2. CTA MAX → корень max.ru (бот-блок deep link).
3. Маркер utility `сделайте`: «Делайте» → «Сделайте» в первой секции (action_markers 8).
4. `meta_ab.title_seo` — ключи primary_query, длина 72 симв.

## Gate

**PASS** — директор может запускать cover || schema.
