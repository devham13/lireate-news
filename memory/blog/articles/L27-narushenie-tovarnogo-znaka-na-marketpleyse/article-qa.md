# QA: L27 narushenie-tovarnogo-znaka-na-marketpleyse

date: 2026-11-01
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×9, FAQ 5, таблица×2, ol×6, TL;DR blockquote |
| GEO / citability | 25 | 22 | таблица площадок, workflow blockquote, «Делайте / не делайте», FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 13 | 0 AI-slop hits; −2 over-long (7) |
| Fact safety | 14 | 11 | fact-check PASS (7 verified, 6 unverified; сверено с research-notes) |
| Contract HTML | 10 | 10 | linter PASS, img+cover alt, ~8.9k ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — жалоба правообладателя на МП |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Правообладатель с свидетельством на WB/Ozon/Маркет |
| C04 | ✓ | ст. 1483/1484/1515/1252 в первых блоках |
| O01 | ✓ | H2 = workflow из research (доказательства → площадки → претензия) |
| O02 | ✓ | признаки → МКТУ → чек-лист → WB → Ozon → таблица → претензия → маршрут → Лирейт |
| O03 | ✓ | FAQ 5 |
| O04 | ✓ | таблица×2, ol×6, blockquote×3, ul чек-лист |
| R01 | ✓ | Standalone блоки в H2-секциях |
| R02 | ✓ | consultant.ru, searchplatform, seller.wildberries, yandex support |
| R03 | ✓ | 10/30 дней WB, 30 дней претензия, 10k–10M ₽ с 04.01.2026 — research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «жалоба площадки ≠ претензия селлеру» vs SERP «как пожаловаться» |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | `/reg-tz-main`, live L03/L02 seo_url |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes, таблица MP-каналов |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, дата 01.11.2026 |
| Ept02 | ✗ | canonical L02/L03 в meta ≠ live seo_url (исправлено в HTML) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| html-linter | PASS | 0 | html-linter-report.json |
| link-verify | PASS | 0 | link-verify.json |
| slop-detector | WARNING | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, не L27) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| fact-check | PASS | 0 | fact-check-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 18, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`

## GEO QA fixes applied (fix cycle 1, 2026-11-01)

1. `<figure>` cover → `<p><img …>` (whitelist linter).
2. `rospatent.gov.ru/opendata` (SSL fail) → только Поисковая платформа.
3. `sreda.rwb.ru` (498) → Garant / zhelezno.com.
4. `brand.ozon.ru` (DNS fail в Cloud) → текст + рабочие ссылки Trusty/onlinepatent/marqatm.
5. Internal 404: L03 → `/kak_zaregistrirovat_brend_na_ozon_i_wildberries_proverka_imeni_i_nuzhen_li_tz`; L02 → `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/`.

## Gate

**PASS** — директор может запускать cover || schema.
