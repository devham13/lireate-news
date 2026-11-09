# Promotion checklist — L41 otchuzhdenie-tovarnogo-znaka-dogovor-reestr

Дата публикации: 2026-11-09  
Live URL: `{PUBLIC_SITE_URL}/otchuzhdenie-tovarnogo-znaka-dogovor-reestr` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L40, L19, `/reg-tz-main`, `/blog/kak-opredelit-klass-mktu/`
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
Продали бренд? Подпись на договоре не делает покупателя правообладателем — нужна запись отчуждения в Роспатенте.

• отчуждение vs лицензия: право после госрегистрации
• пошлина п. 3.11: 15 000 ₽ + 13 000 ₽ за каждый доп. ТЗ
• сроки АР: 68 / 45 рабочих дней

Читать: {PUBLIC_SITE_URL}/otchuzhdenie-tovarnogo-znaka-dogovor-reestr
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «договор отчуждения товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-09): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles` (--article-dir в CLI не поддерживается) — **1** автоматическая вставка **L41→L06** («классы МКТУ» → `/blog/kak-opredelit-klass-mktu/` в `article.html`). Inbound на L41 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (46 статей в индексе репозитория, `/blog/{slug}/`); `memory/blog/lireate-site/` — **41** L-статья с `canonical_path` (добавлены L40, L41); копии `llms.txt` / `llms-full.txt` в каталоге L41. Live publish не выполнялся.
