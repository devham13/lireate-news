# QA: L68 domennoe-imya-nematerialnyy-aktiv

date: 2026-11-19
score_total: 86/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8, FAQ 7, 2 таблицы, ol×9, TL;DR blockquote |
| GEO / citability | 25 | 23 | три слоя (админ/учёт/ТЗ), маршрут blockquote, FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 14 | 0 slop-клише; 3 предложения >25 слов (таблицы) |
| Fact safety | 14 | 11 | fact-check PASS (10 extracted, 3 verified); −3 справочные даты/НУ вне fact-bank |
| Contract HTML | 10 | 10 | html-linter PASS, char_count ~8533 ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/primary — доменное имя как нематериальный актив |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Владелец бренда / главбух |
| C04 | ✓ | ФСБУ, 149-ФЗ, 08/26 в первых блоках |
| O01 | ✓ | H2 = how-to цепочка |
| O02 | ✓ | Разведение слоёв → 9 шагов → спор |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | 2 таблицы, ol×9, blockquote |
| R01 | ✓ | Standalone секции |
| R02 | ✓ | Консультант+, ГАРАНТ, Поисковая платформа |
| R03 | ✓ | Дата 19.11.2026 в lead |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «сквозной гайд» vs L10 (чек-лист НМА) |
| E02 | ✓ | «Делайте / не делайте» |
| E03 | ✓ | findtz, reg-tz, Telegram, L10/L38/L24 |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Дисклеймер аудит/юруслуга |
| Ept02 | ✗ | Canonical slug L10/L17 на проде — legacy SEO URL (fix cycle 1) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | WARNING (repo-wide) | cannibalization-report.json |
| utility gate | PASS | utility-gate-report.json |
| lireate privacy | PASS | (repo-wide `--all-lireate`) |

## Link verify (fix cycle 1, 2026-11-19)

- total: 19, failed: 0
- minfin.gov.ru (503) → `consultant.ru` ФСБУ 14/2022
- new.fips.ru (403) → 149-ФЗ + licensingrussia (реестры)
- internal L10 `/domennoe-imya-nma-ili-net/` (404) → `/domennoe_imya_nma_ili_net_uchet_i_zaschita_domena_po_fsbu_14_2022/`
- internal L17 slug (404) → `/mozhno_li_pokazyivat_chuzhie_logotipyi_i_emblemyi_v_video_i_na_oblozhkax/`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 3 (артефакт таблиц в plain-text)
- Flesch RU: 50.8 (Standard)

## Fact-check

- verdict: PASS (10 extracted, 3 verified, 7 unverified — даты/НУ справочно)

## Cannibalization

- repo-wide WARNING (другие пары L*), L68↔L10 overlap ожидаем (кластер домен/ФСБУ; L68 — связка с ТЗ и уступкой)

## GEO QA FIX

- `article.html`: только ссылки и уточнение абзаца про 149-ФЗ (не полный рерайт)