# QA: L57 naricatelnye-brendy-aspirin-obobshchenie

date: 2026-11-13
score_total: 90/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, ol×27, 2 таблицы, режим B, troubleshooting |
| GEO / citability | 25 | 23 | TL;DR 1483/1514/1486, матрица норм, самотест 8 флагов, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; 4 предложения >25 слов |
| Fact safety | 15 | 12 | fact-check PASS (9 extracted, 4 verified, 5 unverified — НПА в research-notes) |
| Contract HTML | 10 | 10 | linter PASS, ~8.7k chars |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | Title/H1 — genericide, 1483, 1514, brand guidelines |
| C02 | ✓ | Lead + TL;DR — п. 1/3 ст. 1483, п. 6 ст. 1514, отличие от 1486 |
| C03 | ✓ | Правообладатель, маркетинг, дилеры, ИП |
| C04 | ✓ | Консультант 1483/1514/1486, методрекомендации ПП, СИП-226/2025 |
| O01 | ✓ | H2 = workflow (самотест → norms → guidelines → дилеры → мониторинг → архив → Роспатент) |
| O02 | ✓ | Таблица 1483/1514/1486, чеклист 8 флагов, 7 шагов в таблице сигналов |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, blockquote×4, нумерованные списки |
| R01 | ✓ | «Делайте / не делайте» в ключевых секциях |
| R02 | ✓ | BBC, Forbes, INTA PDF, palatapp, L01/L40 interlink |
| R03 | ✓ | research-notes / fact-check |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Отстройка от L15 (1486) и L40 (нужна ли регистрация) |
| E02 | ✓ | Самотест и red flags до подачи в Роспатент |
| E03 | ✓ | CTA `/registraciya_tovarnogo_znaka/`; interlink L01, L40 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер 13.11.2026, не юрконсультация |
| Ept02 | ✗ | L15 не на live — interlink на `/dosrochnoe-…` отложен (indexer после публикации L15) |

## Script reports

| Скрипт | Verdict | exit | Файл |
|--------|---------|------|------|
| fact-check | PASS | 0 | fact-check-report.json |
| link-verify | PASS | 0 | link-verify.json |
| html-linter | PASS | 0 | html-linter-report.json |
| slop-detector | PASS (0 clichés) | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo-level; не L57) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 15, failed: 0
- site-base: публичный домен Lireate (`--site-base`, env `LIREATE_PUBLIC_SITE_URL`)

## GEO QA fixes applied (fix cycle 1, 2026-11-13)

1. `patentinfo.ru` (DNS fail в Cloud) → palatapp методрекомендации ПП (×1).
2. `/dosrochnoe-prekrashchenie-tovarnogo-znaka-neispolzovanie` (L15 → 404 на live) → consultant ст. 1486 (×5); дубль «L15» в TL;DR убран.
3. После публикации L15 — indexer может вернуть internal interlink.

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 4
- Flesch RU: 57.2 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: PASS (9 extracted, 4 verified, 5 unverified)
- see `fact-check-report.json`

## Cannibalization

- verdict: WARNING at repo level only; L57 intent уникален (anti-genericide / 1483)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: GEO QA — ссылки L15 + patentinfo
- cycle 2: не требовался

## Optional (не blocker)

- cover `cover/cover.png` — после cover-агента
- Восстановить L15 interlink после live INSERT L15

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | author_id: pending registry
