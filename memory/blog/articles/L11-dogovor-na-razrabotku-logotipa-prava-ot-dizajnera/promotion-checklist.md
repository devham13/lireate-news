# Promotion checklist — L11 dogovor-na-razrabotku-logotipa-prava-ot-dizajnera

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/dogovor-na-razrabotku-logotipa-prava-ot-dizajnera` (заполнить после publish)  
Рубрика: Логотип (`category_id=10`) — `{PUBLIC_SITE_URL}/news?num=2&category=10`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`, `/blog/kak-opredelit-klass-mktu/` (или live-ЧПУ L06), `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (маркетинг, стартапы, дизайн-заказчики) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Оплатили логотип, а права остались у дизайнера? Без письменного отчуждения (ст. 1234) или лицензии (ст. 1286) Роспатент не спасёт от п. 9 ст. 1483.

• Фрилансер — договор авторского заказа (ст. 1288); студия — проверьте ст. 1296
• Отчуждение vs лицензия: таблица в статье + цена за права обязательна
• Акт, исходники AI/EPS и папка документов перед чек-листом L01 и заявкой на ТЗ

Читать: {PUBLIC_SITE_URL}/dogovor-na-razrabotku-logotipa-prava-ot-dizajnera
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 10), если нет авто
- [ ] После publish — рассмотреть inbound из L06/L01 на anchor «договор с дизайнером» / «права на логотип перед ТЗ» (ручная вставка, если interlinker не сматчит)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «авторские права на логотип» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-21): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** вставка (L11 → L06 по «классы МКТУ»; outbound на legacy чек-лист L01, `/reg-tz-main` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (16 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **11** L-статей с `canonical_path` (добавлен L11); копии `llms.txt` / `llms-full.txt` в каталоге L11.
