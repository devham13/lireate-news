# Promotion checklist — L39 dorabotka-logotipa-pered-registraciey-tovarnogo-znaka

Дата публикации: 2026-11-09  
Live URL: `{PUBLIC_SITE_URL}/dorabotka-logotipa-pered-registraciey-tovarnogo-znaka` (заполнить после publish)  
Рубрика: Логотип (`category_id=10`) — `{PUBLIC_SITE_URL}/news?num=2&category=10`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L01, L11, L07, L30, legacy-гайд; `/reg-tz-main`; `/blog/kak-opredelit-klass-mktu/`
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
Логотип уже в брендбуке, а экспертиза пишет про ст. 1483? Сначала правка макета, потом ответ по ст. 1497.

• чек-лист доминанты и ч/б вектора
• граница правки и новой заявки
• 6 месяцев на ответ после уведомления

Читать: {PUBLIC_SITE_URL}/dorabotka-logotipa-pered-registraciey-tovarnogo-znaka
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 10), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «доработка логотипа перед регистрацией товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-09): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base https://example.com` — **1** автоматическая вставка **L39→L06** («классы МКТУ» → `/blog/kak-opredelit-klass-mktu/`). Inbound на L39 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (44 статьи, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **39** L-статей с `canonical_path` (добавлен L39 `/dorabotka-logotipa-pered-registraciey-tovarnogo-znaka`); копии `llms.txt` / `llms-full.txt` в каталоге L39. `blog-topics.md` L39 — `status: written`. Live publish не выполнялся.
