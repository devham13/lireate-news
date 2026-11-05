# QA: L35 avtorskoe-voznagrazhdenie-po-gk-rf

date: 2026-11-05
score_total: 84/100
core_eeat_lite: 17/20
link_verify: pass
utility_gate: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 18 | H2×10 (+FAQ), FAQ 7, таблица×2, ol×8+8, TL;DR blockquote |
| GEO / citability | 25 | 22 | таблицы основание/форма, workflow blockquote, «Делайте / не делайте», 1301 ≠ гонорар |
| CORE-EEAT lite | 15 | 14 | 17/20 (см. ниже) |
| Human voice | 15 | 12 | 0 AI-slop hits; −3 over-long (4) |
| Fact safety | 14 | 10 | fact-check WARNING (1 verified, 17 unverified; сверено с research-notes) |
| Contract HTML | 10 | 8 | linter PASS, `<img>` cover alt, ~9.0k ✓; `<figure>` убран до collage inject |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass, utility gate PASS — **выполнен**.

## CORE-EEAT lite: 17/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/title — авторское вознаграждение по ГК, workflow |
| C02 | ✓ | Lead + TL;DR без «в этой статье» |
| C03 | ✓ | Заказчик контента, HR, бухгалтерия |
| C04 | ✓ | 1234/1235/1286/1288/1295/1301 в первых блоках |
| O01 | ✓ | H2 = research action_outline |
| O02 | ✓ | основание → форма → ol workflow → служебное → отчёт → сроки → НДФЛ → 1301 → патенты → чек-лист |
| O03 | ✓ | FAQ 7 |
| O04 | ✓ | таблица×2, ol×16, blockquote×3 |
| R01 | ✓ | Standalone блоки в H2-секциях |
| R02 | ✓ | consultant.ru, garant, ppt.ru — research-notes |
| R03 | ✓ | НДФЛ 13/15%, компенсация 1301 — с источниками; без выдуманных «минимальных %» |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол workflow выплат vs шаблоны и «1301 как гонорар» |
| E02 | ✓ | «Делайте / не делайте» по секциям |
| E03 | ✓ | CTA рубрика AP (category=12), перелинк logotip (category=10); ≤3 commercial |
| Exp01 | ✓ | Режим B |
| Exp02 | ✓ | research-notes, таблицы основание/форма |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Не юрконсультация, дата 05.11.2026 |
| Ept02 | ✗ | −1: canonical L11/dogovor-avtorskij ещё не live — interim rubric URLs |

## Script reports

| Скрипт | Verdict | Exit | Файл |
|--------|---------|------|------|
| html-linter | PASS | 0 | html-linter-report.json |
| link-verify | PASS | 0 | link-verify.json |
| slop-detector | PASS | 0 | slop-detector-report.json |
| cannibalization | WARNING (repo L08↔L21, не L35) | 0 | cannibalization-report.json |
| utility gate | PASS | 0 | utility-gate-report.json |
| fact-check | WARNING | 0 | fact-check-report.json |
| lireate privacy | PASS | 0 | (`--all-lireate`) |

## Link verify

- total: 15, failed: 0
- site-base: `LIREATE_PUBLIC_SITE_URL`

## GEO QA fixes applied (fix cycle 1, 2026-11-05)

1. `<figure class="lx-article-cover">` → `<p><img …></p>` (whitelist linter; cover-агент вернёт figure при collage inject).
2. `/dogovor_avtorskij`, `/dogovor-na-razrabotku-logotipa-prava-ot-dizajnera` (HTTP 404 на live) → `/news?num=2&category=12` и `/news?num=2&category=10` (200); после публикации L11/indexer — canonical seo_url.

## Gate

**PASS** — директор может запускать cover || schema.
