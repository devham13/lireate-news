# Promotion checklist — L59 kak-dobavit-brend-na-wildberries-seller

Дата публикации: 2026-11-13  
Live URL: `{PUBLIC_SITE_URL}/kak_dobavit_brend_na_wildberries_seller` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L03, L18, L01, L27, L06 (MKTU); CTA Telegram/WhatsApp; `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (селлеры WB, ИП) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Бренд в WB Partners — не то же самое, что товарный знак в Роспатенте. Добавить можно через «Мои бренды», но проверка имени — в двух слоях.

• Мои бренды / карточка: логотип JPG 120×50 до 100 Кб, модерация до 2 р.д.
• Справочник WB не требует свидетельство ТЗ; «Оригинал» и 289-ФЗ с 01.03.2027 — другое
• Параллельно — Поисковая платформа и чек-лист L18

Читать: {PUBLIC_SITE_URL}/kak_dobavit_brend_na_wildberries_seller
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 9), если нет авто
- [ ] Inbound L18 → L59 на якорь «бренд на вайлдберриз как добавить» (interlinker)
- [ ] Обновить L03 при необходимости обратной ссылки на L59 (WB-only гайд)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env); поправить `/blog/*` на live `lireate_seo_url` при необходимости

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «бренд на вайлдберриз как добавить» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-13): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **4** автоматические вставки (inbound L18→L59, L59→L03 keyword, L59→L06, L56→L31); ссылки `/blog/*` приведены к live slug: L59↔L03/L06, L18→L59, L56→L31. `memory/blog/interlink-suggestions.json` (62 статьи, 4 opportunity). llms: `memory/blog/llms.txt` + `llms-full.txt`; `lireate_llms_site_generate.py` → **57** L-записей в `memory/blog/lireate-site/llms.txt`; копии llms в каталоге L59.
