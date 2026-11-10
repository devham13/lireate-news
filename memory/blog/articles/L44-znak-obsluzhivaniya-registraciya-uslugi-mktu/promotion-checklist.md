# Promotion checklist — L44 znak-obsluzhivaniya-registraciya-uslugi-mktu

Дата публикации: 2026-11-10  
Live URL: `{PUBLIC_SITE_URL}/znak_obsluzhivaniya_registraciya_uslugi_mktu` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/mktu`, L01, L29, L30; CTA `/reg-tz-main`
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
Отдельной «услуги только для знака обслуживания» нет — одна заявка по ст. 1477, классы 35–45 в МКТУ-13.

• салон: 44 (+часто 35), кофейня: 43, онлайн-школа: 41
• с 18.08.2026 — форма заявки по приказу № 386
• пошлины не зависят от слова «услуга», только от классов и позиций

Читать: {PUBLIC_SITE_URL}/znak_obsluzhivaniya_registraciya_uslugi_mktu
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «знак обслуживания регистрация» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-10): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **8** автоматических вставок (50 статей; **1** outbound L44→L06 «Классы МКТУ» в таблице; inbound на L44 — **0**; дополнительно hub L06: L02, L15, L18, L25, L29, L37, L38). Outbound writer на `/mktu`, L01, L29, L30, `/reg-tz-main` уже в `article.html`. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (50 статей, `https://example.com/blog/{slug}/` в репо-индексе); `memory/blog/lireate-site/` — **44** L-статьи с `canonical_path` (добавлен L44); копии `llms.txt` / `llms-full.txt` в каталоге L44 (снимок `memory/blog/lireate-site/`, не полный репо-индекс с Maya-статьями). Live publish не выполнялся.
