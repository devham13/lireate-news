# QA: L44 znak-obsluzhivaniya-registraciya-uslugi-mktu

date: 2026-11-10
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ H3×7, 2 таблицы, 4 `<ol>`, TL;DR blockquote |
| GEO / citability | 25 | 24 | Сравнительная таблица ТЗ/услуги, ст. 1477, классы 35-45, приказ 386 |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 slop-клише; 5 предложений >25 слов (slop PASS) |
| Fact safety | 15 | 12 | fact-check PASS (21 extracted, 9 verified, 12 unverified) |
| Contract HTML | 10 | 10 | html-linter PASS; `char_count` ≈8700 |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — знак обслуживания, классы МКТУ, отличие от ТЗ |
| C02 | ✓ | Lead + TL;DR — ст. 1477, классы 35-45, МКТУ-13, приказ 386 |
| C03 | ✓ | ИП, салон, кофейня, онлайн-школа |
| C04 | ✓ | ГК РФ, МКТУ-13, госуслуги, реестр |
| O01 | ✓ | H2 = сравнение, классы, проверка, заявка 2026 |
| O02 | ✓ | Модель бизнеса → классы → реестр → подача |
| O03 | ✓ | FAQ 7 пар |
| O04 | ✓ | 2 таблицы, blockquote, 4 нумерованных списка |
| R01 | ✓ | Делайте / не делайте по секциям |
| R02 | ✓ | Consultant, Госуслуги, searchplatform, online.rospatent |
| R03 | ✓ | Пошлины и оговорки «не консультация»; Вордстат не запрашивался |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол L44 vs L06/L30/L01; ссылки на `/mktu`, L30, чек-лист |
| E02 | ✓ | Матрица кейсов ИП, сравнительная таблица |
| E03 | ✓ | CTA `/reg-tz-main`, внутренние гайды |
| Exp01 | ✓ | Режим B (comparison + how-to) |
| Exp02 | ✓ | research-notes в каталоге |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Блок «Материал проверен» |
| Ept02 | ✓ | Внутренний slug L06 заменён на live `/mktu` при link-verify |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo L08↔L21, L22↔L36, не L44) | 0 | cannibalization-report.json |
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 16, failed: 0
- site-base: публичный домен Lireate (переменная окружения при verify)
- fix cycle 1: `/kak-opredelit-klass-mktu` (404) → `/mktu`; rospatent.gov.ru/dues + stateservices (SSL) → Consultant 82755 + Госуслуги; fips.ru MKTU/прайс (403) → open-data classifier + `/rospatent-fips-proverit-...`; law.ru (302) → Consultant ПП 1459

## GEO QA fixes applied (fix cycle 1)

1. Три внутренних href на slug L06 → live `/mktu`.
2. Три ссылки на таблицу пошлин rospatent.gov.ru → приложение № 1 к ПП РФ № 941 (Consultant).
3. Две ссылки на страницу госуслуги rospatent.gov.ru → Госуслуги.
4. Убрана ссылка на fips.ru MKTU static; прайс ФИПС → гайд L29 (live).

## Gate

**PASS** — директор может запускать cover || schema.
