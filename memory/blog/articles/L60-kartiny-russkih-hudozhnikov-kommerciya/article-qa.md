# QA: L60 kartiny-russkih-hudozhnikov-kommerciya

date: 2026-11-14
score_total: 87/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 7, 2 таблицы, режим B, 9 шагов ol |
| GEO / citability | 25 | 23 | TL;DR два слоя + 54-ФЗ, таблица сценариев, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; 5 предложений >25 слов |
| Fact safety | 15 | 12 | fact-check PASS (14 extracted, 1 verified, 13 unverified — НПА/музеи в research-notes) |
| Contract HTML | 10 | 7 | linter PASS, ~8.5k chars; −3 нет `<img>` с alt (cover pending) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — коммерция, русские художники, 70 лет, музей |
| C02 | ✓ | Lead + TL;DR — ст. 1281, 1274, ст. 36 54-ФЗ |
| C03 | ✓ | Маркетолог, селлер, дизайнер |
| C04 | ✓ | Consultant ГК/54-ФЗ, Garant, ГТГ, Пушкинский, ppt.ru |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Коммерция → срок → ОД → 1274 → музей → файл → лицензия → риски → чек-лист |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, blockquote×3 |
| R01 | ✓ | «Делайте / не делайте» в секциях |
| R02 | ✓ | Consultant, pravo.ppt.ru, tretyakovgallery, pushkinmuseum |
| R03 | ✓ | Дата проверки 14.11.2026 в дисклеймере |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L13 (некоммерция) и generic «картина = бесплатно» |
| E02 | ✓ | Три слоя прав, ст. 1314 не для живописи |
| E03 | ✓ | CTA мессенджеры; interlink L35 (live) |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер, не юруслуга |
| Ept02 | ✗ | Slug L13 ещё 404 на live — GEO QA заменил на ст. 1276/1274 ppt.ru; indexer вернёт L13 после publish |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| excalibur_blog_fact_checker.py | PASS | 0 | fact-check-report.json |
| excalibur_blog_link_verify.py | PASS | 0 | link-verify.json |
| excalibur_blog_html_linter.py | PASS | 0 | html-linter-report.json |
| excalibur_blog_slop_detector.py | PASS | 0 | slop-detector-report.json |
| excalibur_blog_cannibalization_guard.py | WARNING (repo) | 0 | cannibalization-report.json |
| excalibur_blog_utility_gate.py | PASS | 0 | utility-gate-report.json |
| lireate_privacy_link_policy.py --all-lireate | PASS | 0 | (repo-wide) |

## Link verify

- total: 21, failed: 0
- site-base: env `LIREATE_PUBLIC_SITE_URL`, `--timeout 60`

## GEO QA fixes applied (fix cycle 1, 2026-11-14)

1. Удалена служебная оговорка про Вордстат (html-linter FAIL → PASS).
2. `max.ru/u/...` (403) → `https://max.ru/` (как L58).
3. Met Museum (429) → Wikimedia Commons reusing policy.
4. `/mozhno-li-publikovat-foto-kartin-hudozhnika/` (L13 → 404 на live) → `pravo.ppt.ru` ст. 1276/1274 (×3).

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5
- Flesch RU: 58.4 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (14 extracted, 1 verified, 13 unverified)
- unverified: сроки, политики музеев, суммы — сверено по research-notes

## Cannibalization

- WARNING на уровне репозитория (L03/L59, L08/L21 и др.); primary L60 не в списке конфликтов.

## Post-publish

- Indexer: вернуть interlink на slug L13 после live-публикации L13.