# QA: L48 ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu

date: 2026-11-11
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8 (+FAQ), FAQ×7, таблицы×2, ol×4, TL;DR blockquote |
| GEO / citability | 25 | 23 | Две ступени 1498/1499; календарь сроков; таблица отказов по стадии |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; Flesch 51.0 Standard |
| Fact safety | 14 | 11 | fact-check PASS; 5/20 в fact-bank, остальное сверено с research-notes |
| Contract HTML | 10 | 10 | linter PASS, ~9353 знака (cover — шаг 4) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — формальная и по существу, сроки |
| C02 | ✓ | Lead + TL;DR answer-first |
| C03 | ✓ | ИП, ООО, заявитель после подачи |
| C04 | ✓ | ст. 1498–1500, Правила ПТ в первых блоках |
| O01 | ✓ | H2 совпадают с research action_outline |
| O02 | ✓ | Ступени → формальная → принятие → существ → письма → отказы → календарь |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote |
| R01 | ✓ | Самодостаточные блоки с дедлайнами |
| R02 | ✓ | Госуслуги, КонсультантПлюс, searchplatform, L30/L07/L08 |
| R03 | ✓ | 1 / 3 / 6 / 12 мес., 18 мес. 2 нед. — из research |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол workflow vs чек-лист подачи (L30) |
| E02 | ✓ | «Делайте / не делайте» в теле |
| E03 | ✓ | L30, L07, live URL L08, `/registraciya_tovarnogo_znaka/` |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не гарантия регистрации», дата 11.11.2026 |
| Ept02 | ✗ | L48 slug ещё не live → Ept02 по internal self-link |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| fact-check | PASS | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| lireate privacy | PASS | 0 | (repo-wide `--all-lireate`) |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (legacy-пары; не L48) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 15, failed: 0
- site-base: `$LIREATE_PUBLIC_SITE_URL` (link-verify preflight)
- fix (GEO QA): rospatent.gov.ru (SSL в CI) → Госуслуги + ПП № 941; fips 403 → online.rospatent + searchplatform; L08 repo slug → live SEO URL

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 2
- Flesch RU: 51.0 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (20 extracted, 5 verified in fact-bank, 15 unverified)
- сроки и стадии сверены с `research-notes.md` и госуслугой
- see `fact-check-report.json`

## Cannibalization

- repo-wide WARNING на legacy-пары; **L48 primary_query** не в конфликте с другими L*

## Fixes applied (GEO QA)

1. `article.html`: внешние ссылки на проверяемые URL (Госуслуги, ПП 941, online.rospatent, searchplatform).
2. `article.html`: внутренние ссылки L08 на live slug `vozrazhenie_protiv_registracii_chuzhogo_tovarnogo_znaka_sroki_i_poryadok`.
