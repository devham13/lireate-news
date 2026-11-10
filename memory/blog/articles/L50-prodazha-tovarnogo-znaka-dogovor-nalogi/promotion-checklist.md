# Promotion checklist — L50 prodazha-tovarnogo-znaka-dogovor-nalogi

Дата публикации: 2026-11-10  
Live URL: `{PUBLIC_SITE_URL}/prodazha-tovarnogo-znaka-dogovor-nalogi` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L41 (`/otchuzhdenie-tovarnogo-znaka-dogovor-reestr`); L47 (`/prodlenie_tovarnogo_znaka_gosposhlina`); CTA `/reg-tz-main`
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
Продали бренд, а покупатель ещё не в реестре? До записи в Роспатенте право не переходит.

• отчуждение ≠ лицензия; п. 3.11 — 15 000 ₽
• налоги: НДС, прибыль, НДФЛ по режиму
• право у покупателя только после госрегистрации

Читать: {PUBLIC_SITE_URL}/prodazha-tovarnogo-znaka-dogovor-nalogi
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Рассмотреть inbound из L41 на anchor «продать товарный знак» (interlinker не сматчил)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «продать товарный знак» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-10): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (51 статья в индексе; `anchor_variants` L50 не сматчились в чужих HTML; outbound writer на L41, L47, `/reg-tz-main` уже в `article.html`). Inbound на L50 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (51 статья, `/blog/{slug}/`); `memory/blog/lireate-site/` — **46** L-статей с `canonical_path` (добавлен L50); копии `llms.txt` / `llms-full.txt` в каталоге L50. Live publish не выполнялся.
