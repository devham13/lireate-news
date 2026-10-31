# Promotion checklist — L24 sajt-klon-zashchita-brenda-v-internete

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/sajt-klon-zashchita-brenda-v-internete` (заполнить после publish)  
Рубрика: Бренд (`category_id=13`) — `{PUBLIC_SITE_URL}/news?num=2&category=13`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/news?num=2&category=13`; `/blog/kak-opredelit-klass-mktu/` (interlink L24→L06); внешние cctld.ru, consultant.ru
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (владельцы бренда, e-commerce, SaaS) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Нашли сайт-клон с вашим знаком в домене? РКН не закроет его только из-за ТЗ — нужны претензия администратору домена/хостингу и иск по ст. 1515.

• Свидетельство ТЗ + классы МКТУ в Поисковой платформе
• Нотариальный осмотр URL и 30 дней на ответ по претензии
• cctld.ru: домен vs хостинг — разные адресаты

Читать: {PUBLIC_SITE_URL}/sajt-klon-zashchita-brenda-v-internete
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 13), если нет авто
- [ ] Рассмотреть inbound из L10/L02/L01 на «защита бренда в интернете» / «домен и ТЗ» / «ответ на претензию» (ручная вставка: `anchor_variants` L24 не сматчились в чужих HTML)
- [ ] Outbound в L24: interlink на L06 «классы МКТУ»; текстовые отсылки L09/L10/L02 (без href до live slug) — уже в `article.html`
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «защита бренда в интернете» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-31): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** вставка (L24 → L06 по «классы МКТУ»). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (29 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L24 — **24** L-статьи с `canonical_path` (добавлен L24). Live publish не выполнялся.
