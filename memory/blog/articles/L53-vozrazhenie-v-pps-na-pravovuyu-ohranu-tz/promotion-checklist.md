# Promotion checklist — L53 vozrazhenie-v-pps-na-pravovuyu-ohranu-tz

Дата публикации: 2026-11-12  
Live URL: `{PUBLIC_SITE_URL}/vozrazhenie-v-pps-na-pravovuyu-ohranu-tz` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L21, L08, L07, L01, L06; CTA Telegram/WhatsApp/MAX
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
Чужое свидетельство в реестре? Это не ст. 1500 за 9 000 ₽, а возражение в ППС по ст. 1513 — 14 000 ₽ и срок до 5 лет.

• таблица 1493 / 1500 / 1513 — не перепутать процедуры
• матрица сроков ст. 1512 и заинтересованность
• 9 шагов: пошлина 2.28.4, заседание коллегии, отзыв за 10 дней

Читать: {PUBLIC_SITE_URL}/vozrazhenie-v-pps-na-pravovuyu-ohranu-tz
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 9), если нет авто
- [ ] Рассмотреть inbound из L08/L21 на anchor «возражение в ППС на правовую охрану» (interlinker не сматчил в чужих HTML)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «возражение в ппс на предоставление правовой охраны» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-12): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **2** автоматические вставки **в L53** (якорь «классы МКТУ» → L06; «возражение против предоставления правовой охраны» → L33). Inbound на L53 — **0**. `memory/blog/interlink-suggestions.json` обновлён (58 статей, 2 opportunity). llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (58 статей, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **52** L-статьи с `canonical_path` (добавлен L53 `/vozrazhenie-v-pps-na-pravovuyu-ohranu-tz`); копии `llms.txt` / `llms-full.txt` в каталоге L53. Live publish не выполнялся.
