# Promotion checklist — L47 prodlenie-tovarnogo-znaka-gosposhlina

Дата публикации: 2026-11-10  
Live URL: `{PUBLIC_SITE_URL}/prodlenie-tovarnogo-znaka-gosposhlina` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L30 (`/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026`); L40 (`/nuzhno-li-registrirovat-tovarnyy-znak`); CTA `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Ежегодной госпошлины за товарный знак нет — охрана 10 лет с даты заявки по ст. 1491.

• продление раз в 10 лет: п. 2.22 (22 000 ₽ база)
• опоздание: + п. 2.25 (3 000 ₽), возможен разрыв охраны
• без продления — прекращение по ст. 1514

Читать: {PUBLIC_SITE_URL}/prodlenie-tovarnogo-znaka-gosposhlina
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «госпошлину на товарный знак оплачивают каждый год» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-10): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (49 статей в индексе; `anchor_variants` L47 не сматчились в чужих HTML; outbound writer на L30, L40, `/reg-tz-main` уже в `article.html`). Inbound на L47 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (49 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **44** L-статьи с `canonical_path` (добавлен L47); копии `llms.txt` / `llms-full.txt` в каталоге L47. Live publish не выполнялся.
