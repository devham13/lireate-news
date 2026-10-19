# Promotion checklist — L06 kak-opredelit-klass-mktu

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/kak-opredelit-klass-mktu` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (6 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (×2), `/reg-tz-main`; inbound из L01/L02/L03 на `/blog/kak-opredelit-klass-mktu/` (или canonical после маппинга)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, маркетплейсы, заявители ТЗ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
МКТУ — 45 классов: в заявке с 2026 года только формулировки из МКТУ-13–2026, не «свои слова». Вареники — класс 30, ковры — 27, «школьный» 27 в поиске — не про ТЗ.

• Алгоритм: ключевые слова → алфавитный перечень → «не относится» → корреспондирующие классы
• Таблица кейсов: вареники / часы / ковры без путаницы
• После черновика перечня — чек-лист проверки знака в выбранных классах

Читать: {PUBLIC_SITE_URL}/kak-opredelit-klass-mktu
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Inbound уже вставлены indexer: L01, L02, L03 → «классы МКТУ» на L06
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «структура мкту» / «как определить класс мкту» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-19): interlinker `--apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL` — **3** вставки (L01, L02, L03 → L06 по keyword «классы мкту»; outbound L06 на legacy чек-лист и `/reg-tz-main` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (11 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — 6 L-статей с `canonical_path`; копии `llms.txt` / `llms-full.txt` в каталогах L01–L06.
