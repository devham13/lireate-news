# QA: L47 prodlenie-tovarnogo-znaka-gosposhlina

date: 2026-11-10
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8 (+FAQ), FAQ×7, таблицы×5, ol×4, TL;DR blockquote |
| GEO / citability | 25 | 23 | Миф «ежегодная пошлина» vs факт; таблицы пп. 2.22/2.25; «Делайте / не делайте» |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop; Flesch 65.4 Easy |
| Fact safety | 14 | 11 | fact-check PASS; 6/28 в fact-bank, остальное сверено с research-notes |
| Contract HTML | 10 | 10 | linter PASS, cover img + alt, ~8652 знака |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — продление, ежегодная госпошлина, 10 лет |
| C02 | ✓ | Lead + TL;DR answer-first |
| C03 | ✓ | ИП, ООО, маркетплейс, франшиза |
| C04 | ✓ | ст. 1491, 1514, ПП 941 в первых блоках |
| O01 | ✓ | H2 совпадают с research action_outline |
| O02 | ✓ | Миф → срок → разовые vs продление → окно → расчёт → 1514 → подача |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote, cover |
| R01 | ✓ | Самодостаточные блоки с цифрами |
| R02 | ✓ | КонсультантПлюс, searchplatform, Госуслуги, L30/L40 |
| R03 | ✓ | 22 000 ₽, 3 000 ₽, 10 лет — из research |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «нет ежегодной пошлины» vs SERP |
| E02 | ✓ | «Делайте / не делайте» в теле |
| E03 | ✓ | L30, L40, `/reg-tz-main`, category=9 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes.md |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер «не юрконсультация», дата 10.11.2026 |
| Ept02 | ✗ | L47 slug ещё не live → internal paths только на опубликованные |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| fact-check | PASS | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| lireate privacy | PASS | 0 | (repo-wide `--all-lireate`) |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (L08↔L21, L22↔L36, не L47) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |

## Link verify

- total: 8, failed: 0
- site-base: `$LIREATE_PUBLIC_SITE_URL` (link-verify preflight)
- fix (GEO QA): `rospatent.gov.ru` (SSL fail в CI) → ПП РФ № 941 (КонсультантПлюс) для таблицы пошлин; `stateservices` → карточка продления на Госуслугах

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 0
- Flesch RU: 65.4 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (28 extracted, 6 verified in fact-bank, 22 unverified)
- суммы пп. 2.22/2.25 и сроки сверены с `research-notes.md` и ПП № 941
- see `fact-check-report.json`

## Cannibalization

- repo-wide WARNING на legacy-пары; **L47 primary_query** не в конфликте с другими L*

## Fixes applied (GEO QA)

1. `article.html`: внешние ссылки Роспатента на проверяемые URL (КонсультантПлюс + Госуслуги).
2. `article.meta.json`: `meta_ab.title_seo` — ключи из `primary_query` («госпошлину», «оплачивают»).
