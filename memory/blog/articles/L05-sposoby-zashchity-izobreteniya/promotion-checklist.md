# Promotion checklist — L05 sposoby-zashchity-izobreteniya

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/sposoby-zashchity-izobreteniya` (заполнить после publish)  
Рубрика: Патент (`category_id=20`) — `{PUBLIC_SITE_URL}/news?num=2&category=20`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/patent` (×2), внешние Consultant / searchplatform
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (R&D, стартапы, производство) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Патент на изобретение — не то же самое, что патент для ИП: три режима охраны — монополия до 20 лет, ноу-хау по 98-ФЗ или осознанная публикация с льготой 12 месяцев (п. 3 ст. 1350 ГК РФ).

• Базовая пошлина заявки — от 28 000 ₽ за один независимый пункт
• Часто выигрывает комбо: патент на каркас, параметры процесса — в секрете
• Таблица сравнения и план на 7 дней в материале

Читать: {PUBLIC_SITE_URL}/sposoby-zashchity-izobreteniya
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 20), если нет авто
- [ ] Обновить L04 (`/otkazali-v-vydache-patenta-chto-delat`) → ссылка на L05 при контексте «стратегия до подачи / после отказа»
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «способы защиты изобретения» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-19): interlinker `--apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL` — **0** автоматических вставок (10 статей в репо; anchor_variants не матчатся в чужих HTML; CTA `/patent` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (10 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — 5 L-статей с `canonical_path`; копии `llms.txt` / `llms-full.txt` в каталогах L01–L05.
