# QA: L21 osparivanie-tovarnogo-znaka-v-rospatente

date: 2026-10-30
score_total: 91/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, 2 таблицы, ol×7, угол «карта стадий vs L08 how-to» |
| GEO / citability | 25 | 23 | TL;DR, матрица стадий, FAQ answer-first, blockquote-схема |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 AI-slop hits; −1 один over-long hit (артефакт парсера blockquote+ol) |
| Fact safety | 15 | 12 | fact-check WARNING (14 unverified; сверено с research-notes) |
| Contract HTML | 10 | 10 | linter PASS, объём ~8.5k ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — оспаривание в Роспатенте, возражение |
| C02 | ✓ | Lead + TL;DR — 1493 vs 1512–1513 |
| C03 | ✓ | Заинтересованный правообладатель / конкурент |
| C04 | ✓ | ППС, МКТУ, заинтересованное лицо |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | Термины → матрица → основания → admin vs court |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | Таблицы, ol, blockquote |
| R01 | ✓ | Standalone блоки 40–60 слов |
| R02 | ✓ | КонсультантПлюс, ГАРАНТ 644/261, klerk 2.28.4 |
| R03 | ✓ | 14 000 ₽, 9 000 ₽, 5 лет — из research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Карта оспаривания, не клон L08 |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | CTA reg-tz-main ×1 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes / brief |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, admin vs суд |
| Ept02 | ✗ | L08 interlink plain text до live slug; L19 + L01 live |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | WARNING (acceptable) | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS (acceptable) | slop-detector-report.json |
| cannibalization | WARN L08↔L21 (expected) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify

- total: 15, failed: 0
- site-base: публичный домен Lireate (`--site-base`)
- fix cycle 1 (2026-10-30): L08 internal 404 → plain text до publish; L19 slug → `/chto_delat_esli_tovarnyy_znak_zanyat`; rospatent.gov.ru (SSL) → klerk 2.28.4; stateservices → gosuslugi.ru; fips 403 → licensingrussia; opendata → plain text

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 1 (парсер)
- Flesch RU: 57.3 (Standard)
- see `slop-detector-report.json`

## Fact-check

- verdict: WARNING (18 extracted, 4 verified, 14 unverified)
- факты сверены с `research-notes.md` (ст. 1493/1499/1512–1513, 14 000 ₽, 5 лет, 2.28.2)
- see `fact-check-report.json`

## Cannibalization

- WARNING: L08 primary ↔ L21 secondary (83%) — задокументировано в research-notes как SEO-разведение
- CRITICAL L03/L18 duplicate primary — вне scope L21, не блокирует публикацию L21

## Utility gate

- PASS: 7 FAQ, 2 tables, 10 action markers
- see `utility-gate-report.json`

## Fix log

- cycle 1 (GEO QA): `article.html` — link-verify fixes (см. выше); без cover/schema
