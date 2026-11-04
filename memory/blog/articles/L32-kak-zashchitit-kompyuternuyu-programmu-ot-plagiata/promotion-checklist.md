# Promotion checklist — L32 kak-zashchitit-kompyuternuyu-programmu-ot-plagiata

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/kak-zashchitit-kompyuternuyu-programmu-ot-plagiata` (заполнить после publish)  
Рубрика: Программа ЭВМ (`category_id=19`) — `{PUBLIC_SITE_URL}/news?num=2&category=19`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/zaschita_kompyuternoy_programmyi_i_bazyi_dannyix_pravovyie_metodyi`; `/registraciya_mobilnogo_prilozheniya_programma_dlya_evm_ili_tovarnyy_znak` (L20); `/news?num=2&category=19`; `/politika_konfidencialnosti`; `/private_data`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (founders SaaS, in-house юристы, подрядчики dev) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Скопировали ваш код, а не «похожий сервис»? По ст. 1261 ГК РФ охраняется текст программы, не идея интерфейса.

• git + отчуждение прав у подрядчика до претензии
• депонирование в Роспатенте: 5 000 ₽, 62 раб. дня — дата, не «запрет клонов»
• претензия 30 дн. и ст. 1301 — доказательства фрагментов кода

Читать: {PUBLIC_SITE_URL}/kak-zashchitit-kompyuternuyu-programmu-ot-plagiata
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 19), если нет авто
- [ ] Рассмотреть inbound из L20/L23 на «депонирование ПО» / «защита базы данных» (ручная вставка, если `anchor_variants` L32 не сматчатся в чужих HTML)
- [ ] Outbound в L32: writer — legacy «правовые методы ПО/БД», L20 (мобилка vs десктоп), рубрика 19; interlinker inbound на L32 — **0**; interlinker hub — **0**
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как защитить компьютерную программу от плагиата» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-04): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (37 статей в индексе; `anchor_variants` L32 не сматчились в чужих HTML; outbound writer уже в `article.html`). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (37 статей, `/blog/{slug}/`, site-base Lireate); `memory/blog/lireate-site/` и копии в каталоге L32 — **32** L-статьи с `canonical_path` (добавлен L32). Live publish не выполнялся.
