# Promotion checklist — L04 otkazali-v-vydache-patenta-chto-delat

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/otkazali-v-vydache-patenta-chto-delat` (заполнить после publish)  
Рубрика: Патент (`category_id=20`) — `{PUBLIC_SITE_URL}/news?num=2&category=20`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (theme или plugin)
- [ ] Проверить internal links из статьи (200): `/patent`, внешние Consultant / searchplatform / patent-family
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (изобретатели, R&D, стартапы) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
«Если отказали патент» в поиске — это не про ПСН и не про миграцию. Смотрите тип письма ФИПС: 6 месяцев на уведомление о патентоспособности, 7 месяцев на возражение в ППС.

• Пошлина ППС: 3 000 ₽ за независимый пункт (не как у товарного знака)
• Сначала административный порядок (ст. 1248 ГК), потом СИП
• Поисковая платформа — сверка противопоставлений до оплаты

Читать: {PUBLIC_SITE_URL}/otkazali-v-vydache-patenta-chto-delat
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 20), если нет авто
- [ ] Обновить L01 (`/proverka-tovarnogo-znaka-pered-podachey-v-rospatent`) → ссылка на L04 при контексте «патент vs товарный знак» (если уместно)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «если отказали патент что делать дальше» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-19): interlinker `--apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL` — **0** автоматических вставок (9 статей в репо; anchor_variants L01–L04 не матчатся в чужих HTML; CTA `/patent` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (9 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — 4 L-статьи с `canonical_path`; копии `llms.txt` / `llms-full.txt` в каталогах L01–L04.
