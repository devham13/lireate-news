# Promotion checklist — L61 tovarnyj-znak-anime-personazh

Дата публикации: 2026-11-17  
Live URL: `{PUBLIC_SITE_URL}/tovarnyj-znak-anime-personazh/` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L06 (`/kak-opredelit-klass-mktu` или live slug); L11 (legacy `/news?num=2&category=10`); L09, L17, L60, CTA `/registraciya_tovarnogo_znaka/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (селлеры мерча, стримеры) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Мерч с аниме-героем: свидетельство на свой ТЗ не заменяет лицензию и согласие по п. 9 ст. 1483.

• © на персонажа, лицензия на товар и регистрация своего знака — три отдельных слоя
• Поиск в реестре Роспатента до заявки и до партии
• ~35 000 ₽ за первый класс МКТУ (ПП № 941, без скидки 30%)

Читать: {PUBLIC_SITE_URL}/tovarnyj-znak-anime-personazh/
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 9), если нет авто
- [ ] Рассмотреть inbound из L09/L17 на anchor «мерч с персонажами» / «п. 9 ст. 1483» (interlinker не сматчил)
- [ ] Outbound L61→L06: interlinker на «классы МКТУ» (`/blog/kak-opredelit-klass-mktu/`); при publish привести href к live `canonical_path` при необходимости
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «товарный знак на аниме персонажа» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-17): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **3** автоматические вставки (L54→L06, L61→L06, L53→L06 по «классы МКТУ»; inbound на L61 — **0**, `anchor_variants` L61 не сматчились в чужих HTML). Outbound writer: L11, L17, L60, L09, `/registraciya_tovarnogo_znaka`, legacy URL — уже в `article.html`. `memory/blog/interlink-suggestions.json` обновлён (66 статей, 3 opportunities). llms: `memory/blog/llms.txt` + `llms-full.txt` (66 статей, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **61** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L61 `/tovarnyj-znak-anime-personazh`); копии `llms.txt` / `llms-full.txt` в каталоге L61. Live publish не выполнялся.