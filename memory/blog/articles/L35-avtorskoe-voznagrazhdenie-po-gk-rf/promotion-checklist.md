# Promotion checklist — L35 avtorskoe-voznagrazhdenie-po-gk-rf

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/avtorskoe-voznagrazhdenie-po-gk-rf` (заполнить после publish)  
Рубрика: Авторское право (`category_id=12`) — `{PUBLIC_SITE_URL}/news?num=2&category=12`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/news?num=2&category=10` (гайд L11); `/news?num=2&category=12`; `/dogovor_avtorskij` (CTA); `/politika_konfidencialnosti`; `/private_data` (если есть в футере/CTA)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (HR, заказчики контента, фриланс) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Заплатили дизайнеру, а «авторское вознаграждение» в договоре пустое? Гонорар по сделке ≠ компенсация по ст. 1301.

• паушаль или роялти — обязательно в возмездной лицензии (п. 5 ст. 1235)
• служебное произведение — отдельная выплата, не оклад (ст. 1295)
• отчёт лицензиату и календарь сроков — до акта и НДФЛ

Читать: {PUBLIC_SITE_URL}/avtorskoe-voznagrazhdenie-po-gk-rf
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 12), если нет авто
- [ ] Inbound interlinker: L11 → L35 по «договор авторского заказа» (`/blog/avtorskoe-voznagrazhdenie-po-gk-rf/`)
- [ ] Outbound в L35: writer — `/news?num=2&category=10`, `/news?num=2&category=12`, `/dogovor_avtorskij`
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «авторское вознаграждение гк» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-05): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** inbound (L11 → L35 по «договор авторского заказа»). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (40 статей репо, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L35 — **35** L-статей с `canonical_path` (добавлен L35). Live publish не выполнялся.
