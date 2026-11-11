# QA: L46 licenzionnyy-dogovor-na-tovarnyy-znak

date: 2026-11-11
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS
fix_cycles: 1

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ H3×7, таблицы×3, `<ol>`×2 (11 шагов), TL;DR blockquote |
| GEO / citability | 25 | 22 | Сравнение лицензия/отчуждение, простая vs исключительная, workflow blockquote |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 slop-клише; 3 предложения >25 слов (slop PASS) |
| Fact safety | 15 | 11 | fact-check PASS (14 extracted, 2 verified, 12 unverified) |
| Contract HTML | 10 | 10 | html-linter PASS; `char_count` ≈8620 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/workflow: лицензия, франшиза, регистрация предоставления права |
| C02 | ✓ | Lead + TL;DR: ст. 1236, 1490, 1232 п. 6, пошлина 3.10 |
| C03 | ✓ | Франчайзи, дилер, селлер WB/Ozon, правообладатель ТЗ |
| C04 | ✓ | ГК 1232–1238, 1489–1490, Пленум № 10 п. 37, таблица пошлин |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Вид лицензии → договор → пошлина → подача → запись в реестре |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблица×3, blockquote×3, ol×11 |
| R01 | ✓ | «Делайте / не делайте» по секциям |
| R02 | ✓ | Consultant, klerk/patent24, searchplatform, licensingrussia |
| R03 | ✓ | Суммы 15 000/13 000 ₽, оговорка не консультация; Вордстат не запрашивался |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от отчуждения (L41), занятого знака (L19), МП (L03) |
| E02 | ✓ | Таблицы вида лицензии и лицензия vs отчуждение |
| E03 | ✓ | CTA `/registraciya_tovarnogo_znaka/` |
| Exp01 | ✓ | Режим B (workflow + troubleshooting) |
| Exp02 | ✓ | research-notes в каталоге |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Блок «Материал проверен» |
| Ept02 | ✗ | −1: канон rospatent.gov.ru в тексте, href — зеркала (klerk/online) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo L08↔L21, L22↔L36, L34↔L38; не L46) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 19, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`

## GEO QA fixes applied (fix cycle 1)

1. L19 → live `lireate_seo_url` `/chto_delat_esli_tovarnyiy_znak_zanyat/`.
2. L03 → `/kak_zaregistrirovat_brend_na_ozon_i_wildberries_proverka_imeni_i_nuzhen_li_tz/`.
3. rospatent.gov.ru (SSL) → klerk (п. 3.10), online.rospatent (подача), searchplatform + licensingrussia (реестр).
4. CTA MAX → `https://max.ru/`.

## Gate

**PASS** — директор может запускать cover || schema.
