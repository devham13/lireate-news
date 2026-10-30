# Promotion checklist — L21 osparivanie-tovarnogo-znaka-v-rospatente

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/osparivanie_tovarnogo_znaka_v_rospatente` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/chto_delat_esli_tovarnyy_znak_zanyat`, `/reg-tz-main`, `/news?num=2&category=9`, `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, правообладатели, селлеры) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Чужой знак в реестре? Карта административного оспаривания: обращение по ст. 1493 на заявке или возражение в ППС по ст. 1512–1513 — 14 000 ₽, срок 5 лет.

• Таблица: 1493 vs 1513 vs ответ по своей заявке (ст. 1500)
• Заинтересованное лицо, основания ст. 1512, куда подавать в Роспатент
• Отличие от суда (ст. 1514) и от пошагового гайда L08

Читать: {PUBLIC_SITE_URL}/osparivanie_tovarnogo_znaka_v_rospatente
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — рассмотреть inbound из L08 на anchor «карта стадий» / «1493 vs 1513» (ручная вставка: interlinker не сматчил фразы в L21)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «оспаривание товарного знака в роспатенте» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-30): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок в L21 (26 статей; **6** вставок в L03/L17/L18/L19 по hub L06/L11/L18; outbound на legacy чек-лист, `/reg-tz-main`, рубрика 9, «если знак занят» уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (26 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L21 — **21** L-статья с `canonical_path` (добавлен L21). Live publish не выполнялся.
