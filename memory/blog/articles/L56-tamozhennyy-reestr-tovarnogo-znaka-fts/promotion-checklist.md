# Promotion checklist — L56 tamozhennyy-reestr-tovarnogo-znaka-fts

Дата публикации: 2026-11-13  
Live URL: `{PUBLIC_SITE_URL}/tamozhennyy_reestr_tovarnogo_znaka_fts_vklyuchenie` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L01, L30, L31, L27, L22; CTA Telegram/WhatsApp/MAX; interlink L31→L56 (inbound), L56→L31 (FAQ «параллельный импорт»)
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
Контрафакт на границе? Без ТРОИС таможня не обязана приостанавливать выпуск по вашему знаку.

• ТРОИС ФТС: заявление по Приказу № 131, страховка от 500 000 ₽, срок до 3 лет
• не путайте 2 года (реестр ЕАЭС) и 3 года (национальный ТРОИС)
• приостановление 10+10 раб. дней по ст. 124 ТК ЕАЭС

Читать: {PUBLIC_SITE_URL}/tamozhennyy_reestr_tovarnogo_znaka_fts_vklyuchenie
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 9), если нет авто
- [ ] Inbound L31 на якорь «таможенный реестр объектов интеллектуальной собственности» — проверить после publish
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «включение товарного знака в таможенный реестр ФТС» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-13): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **3** автоматические вставки (2× в L56, 1× inbound в L31). Автолинк в TL;DR L56 на L31 (определение ТРОИС) **снят**; FAQ «параллельный импорт» → L31 с live slug `mozhno_li_zapretit_vvoz_analoga_zapatentovannogo_tovara`; inbound L31 → `tamozhennyy_reestr_tovarnogo_znaka_fts_vklyuchenie`. `memory/blog/interlink-suggestions.json` обновлён (61 статья, 3 opportunity). llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (61 статей, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **56** L-статей (добавлен L56); копии `llms.txt` / `llms-full.txt` в каталоге L56. Live publish **не** выполнялся.
