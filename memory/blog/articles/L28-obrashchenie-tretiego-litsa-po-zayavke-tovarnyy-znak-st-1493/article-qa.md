# QA: L28 obrashchenie-tretiego-litsa-po-zayavke-tovarnyy-znak-st-1493

date: 2026-11-02
score_total: 83/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×8 (+FAQ), FAQ 7, таблица×2, ol×5, TL;DR blockquote |
| GEO / citability | 25 | 21 | таблица 1493 vs ППС, workflow blockquote, «Делайте / не делайте», FAQ answer-first |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 12 | 0 AI-slop hits; −3 over-long (4) |
| Fact safety | 14 | 11 | fact-check WARNING (2 verified, 11 unverified; сверено с research-notes) |
| Contract HTML | 10 | 10 | linter PASS, img+cover alt, ~9.2k ✓ |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — обращение по ст. 1493 до регистрации |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Третье лицо / любое лицо после бюллетеня |
| C04 | ✓ | ст. 1493/1499/1477/1483/1512 в первых блоках |
| O01 | ✓ | H2 = action_outline из research (1493 vs ППС → окно → доводы → подача) |
| O02 | ✓ | таблица → чек-лист → ol реквизитов → маршрут → L08/L21 |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица×2, ol×5, blockquote×3, ul×2 |
| R01 | ✓ | Standalone блоки в H2-секциях |
| R02 | ✓ | consultant.ru, searchplatform, klerk 2.28.4, garant ППС |
| R03 | ✓ | 15 раб. дней бюллетень, 5 лет 1512, 14 000 ₽ 2.28.4 — research-notes |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол «1493 на заявке» vs L08/L21 и SERP «возражение на заявку» |
| E02 | ✓ | «Делайте / не делайте» в секциях |
| E03 | ✓ | `/reg-tz-main`, live L08/L21 seo_url |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes, сравнительная таблица стадий |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, дата 02.11.2026 |
| Ept02 | ✗ | −1: часть цифр не в fact-bank (ожидаемо для L-серии) |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| html-linter | PASS | 0 | html-linter-report.json |
| link-verify | PASS | 0 | link-verify.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, не L28) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| fact-check | WARNING | 0 | fact-check-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 17, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`

## GEO QA fixes applied (fix cycle 1, 2026-11-02)

1. `<figure>`/`<figcaption>` → `<p><img …></p>` + `<p><i>…</i></p>` (whitelist linter).
2. `rospatent.gov.ru` (SSL fail в Cloud) → consultant / klerk.ru (2.28.4) / plain address из Правил № 482.
3. `fips.ru` (403) → Garant Правила ППС 644/261.
4. Internal L08/L21 — HTTP 200 на live seo_url (без правок).

## Gate

**PASS** — директор может запускать cover || schema.
