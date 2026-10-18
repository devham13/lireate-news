# Promotion checklist — L03 kak-zaregistrirovat-brend-na-ozon-i-wildberries

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/kak-zaregistrirovat-brend-na-ozon-i-wildberries` (заполнить после publish)  
Рубрика: Бренд (`category_id=13`) — `{PUBLIC_SITE_URL}/news?num=2&category=13`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (theme или plugin)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`, `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec`, `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (селлеры, ИП, бренд на маркетплейсах) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
«Бренд в ЛК» WB/Ozon — не то же самое, что товарный знак в Роспатенте. Сначала проверьте имя в Поисковой платформе и при создании бренда в кабинете.

• WB: «Мои бренды»; Ozon: «Товары → Бренды»
• Когда хватит справочника площадки, а когда нужны документы на ТЗ и «Оригинал»
• Календарь 289-ФЗ: сверка карточек с реестром с 01.03.2027

Читать: {PUBLIC_SITE_URL}/kak-zaregistrirovat-brend-na-ozon-i-wildberries
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 13), если нет авто
- [ ] Обновить L01 (`/proverka-tovarnogo-znaka-pered-podachey-v-rospatent`) → ссылка на L03 при публикации (anchor «бренд на маркетплейсе» / «Wildberries и Ozon»)
- [ ] Обновить L02 (`/otvet-na-pretenziyu-pravoobladatelya-tovarnogo-znaka`) → ссылка на L03 при релевантном контексте (претензия из-за чужого бренда в карточке)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как проверить есть ли такой бренд на вайлдберриз» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-18): interlinker `--apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL` — **0** автоматических вставок (8 статей; anchor_variants L01/L02/L03 не матчатся в чужих HTML; outbound на legacy URL L01/L02 и `/reg-tz-main` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (8 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — 3 L-статьи с `canonical_path`; копии `llms.txt` / `llms-full.txt` в каталогах L01–L03.
