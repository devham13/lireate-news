# Promotion checklist — L42 sluzhebnoe-proizvedenie-prava-sotrudnika

Дата публикации: 2026-11-09  
Live URL: `{PUBLIC_SITE_URL}/sluzhebnoe-proizvedenie-prava-sotrudnika` (заполнить после publish)  
Рубрика: Авторское право (`category_id=17`) — `{PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L11, L35, `/dogovor_avtorskij`, news category 10/12
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
Штатный дизайнер сделал логотип — права компании не из пункта в ТД, а из ст. 1295 и пакета документов.

• служебное произведение: должностная инструкция + акт сдачи
• правило трёх лет на использование, передачу или коммерческую тайну
• подряд и вознаграждение — отдельно: L11 и L35

Читать: {PUBLIC_SITE_URL}/sluzhebnoe-proizvedenie-prava-sotrudnika
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 17), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «служебное произведение исключительные права работодатель» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-09): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (47 статей; `anchor_variants` не сматчились в чужих HTML; outbound writer на L11, L35, `/dogovor_avtorskij` уже в `article.html`). Inbound на L42 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: перегенерация `memory/blog/llms.txt` + `llms-full.txt` (47 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **42** L-статьи с `canonical_path` (добавлен L42); копии `llms.txt` / `llms-full.txt` в каталоге L42. Live publish не выполнялся.
