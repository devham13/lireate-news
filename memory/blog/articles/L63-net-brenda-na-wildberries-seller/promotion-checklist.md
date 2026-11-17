# Promotion checklist — L63 net-brenda-na-wildberries-seller

Дата публикации: 2026-11-17  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/net_brenda_na_wildberries_seller/` (подтвердить после INSERT на хостинге)  
Рубрика: Бренд (`category_id=13`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=13`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L59 (`/kak_dobavit_brend_na_wildberries_seller/`); L03; L18; L06 (`/blog/kak-opredelit-klass-mktu/` — interlinker); CTA `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (селлеры WB, ИП без марки) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
«Нет бренда» в WB — значение справочника для товара без марки; это не товарный знак и не даёт исключительных прав.

• Когда честно выбрать no-name и когда поле после отказа пустое
• Отличие записи в «Мои бренды» от ТЗ и от «Оригинала»
• Мосты к L59 (своё имя), L18 (реестр), L03 (стратегия)

Читать: {LIREATE_PUBLIC_SITE_URL}/net_brenda_na_wildberries_seller/
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 13), если нет авто
- [ ] Outbound L63→L06: interlinker на «классы МКТУ» (при publish привести href к live slug при необходимости)
- [ ] Рассмотреть inbound из L59/L18 на anchor «нет бренда» / «продавать без бренда» (interlinker inbound на L63 — **0**)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как разобраться нет бренда в wildberries» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-17): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **1** автоматическая вставка (L63→L06 по «классы МКТУ»; inbound на L63 — **0**, `anchor_variants` L63 не сматчились в чужих HTML). Outbound writer: L59, L03, L18, `/reg-tz-main` — уже в `article.html`. `memory/blog/interlink-suggestions.json` обновлён (68 статей, 1 opportunity). llms: `memory/blog/llms.txt` + `llms-full.txt` (68 статей, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **63** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L63 `/net_brenda_na_wildberries_seller`); копия `llms.txt` в каталоге L63 (полный `llms-full.txt` — только в `memory/blog/`).

Live publish: **не выполнялся** (`publish:no`; выкладка — CRON REG.RU после merge).