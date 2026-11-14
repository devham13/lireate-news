# Promotion checklist — L58 lichnaya-perepiska-avtorskoe-pravo

Дата публикации: 2026-11-14  
Live URL: `{PUBLIC_SITE_URL}/lichnaya-perepiska-avtorskoe-pravo` (заполнить после publish)  
Рубрика: Авторское право (`category_id=17`) — `{PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): legacy `/rasprostranyaetsya_li_avtorskoe_pravo_na_perepisku/`, L02 `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/` (×2), consultant/Garant внешние
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
Согласие на переписку ≠ согласие на скрин в ленте: три контура до публикации.

• ©: творческий текст vs «ок» по п. 6 ст. 1259; скрин = ст. 1270
• тайна переписки (ст. 152.2) и отдельное согласие на ПДн (ст. 10.1)
• для обмана — суд/полиция, не пост

Читать: {PUBLIC_SITE_URL}/lichnaya-perepiska-avtorskoe-pravo
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 17), если нет авто
- [ ] Inbound автолинков на L58 — **0** (`anchor_variants` L58 не сматчились в чужих HTML на этом прогоне)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «является ли личная переписка объектом авторского права» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-14): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base https://example.com` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (64 статьи в индексе; `anchor_variants` L58 не сматчились в чужих HTML; outbound writer на legacy обзор переписки, L02 (претензия) уже в `article.html`). Inbound на L58 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (64 статьи, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` с `LIREATE_PUBLIC_SITE_URL=https://example.invalid` → **59** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L58); копия `llms.txt` в каталоге L58. Live publish **не** выполнялся.