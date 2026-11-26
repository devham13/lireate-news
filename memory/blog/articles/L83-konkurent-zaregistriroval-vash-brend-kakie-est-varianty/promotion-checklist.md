# Promotion checklist — L83 konkurent-zaregistriroval-vash-brend-kakie-est-varianty

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/konkurent_zaregistriroval_vash_brend_kakie_est_varianty/` (ожидаемый `lireate_seo_url`; подтвердить после INSERT и `article.meta.json`)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`  
Статус indexer: **`article.html` ещё не в PR** — перелинковку L83↔L84↔L85 завершить после writer.

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links: `/konkurent_zaregistriroval_pohozhiy_tovarnyy_znak/` (L33, граница «сходство»), `/prodazha_originalnogo_tovara_kogda_sporyat_ob_ischerpanii_prava/` (L84), `/ukrali_fotografii_kak_zafiksirovat_narushenie_i_zashchitit_prava/` (L85)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)

## Соцсети / каналы

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Матрица вариантов A–E (аннулирование / приоритет / переговоры) | ☐ |
| VK / Max | Владельцы бренда без своей регистрации | ☐ |

## Snippet для Telegram (черновик)

```
Конкурент записал ваше имя в реестр? Сначала матрица: оспорить, торговаться или регистрировать свой знак.

• не путать с «похожим знаком» (L33)
• ст. 1512, приоритет использования
• кластер IP-споров L84, L85

Читать: {LIREATE_PUBLIC_SITE_URL}/konkurent_zaregistriroval_vash_brend_kakie_est_varianty/
```

## Перелинковка

- [ ] **L85:** outbound L85→L83 (indexer 2026-11-26); добавить **inbound L83→L85** в writer/indexer после `article.html`
- [ ] **L84:** взаимные ссылки «ТЗ на оригинале» vs «перехват имени»
- [ ] Interlinker `--apply` после появления meta с `anchor_variants`
- [ ] Скопировать `memory/blog/llms.txt` в каталог статьи после publish

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read`
- [ ] Primary query «конкурент зарегистрировал мой товарный знак»

## Notes

Indexer (2026-11-26): promotion-checklist создан на research/schema; cross-link к L85 уже в `article.html` L85. `shared/published-articles.md` не обновлялся.