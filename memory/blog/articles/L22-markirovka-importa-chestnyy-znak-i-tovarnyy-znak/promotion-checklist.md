# Promotion checklist — L22 markirovka-importa-chestnyy-znak-i-tovarnyy-znak

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/markirovka-importa-chestnyy-znak-i-tovarnyy-znak` (заполнить после publish)  
Рубрика: Бизнес (`category_id=15`) — `{PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`, `/reg-tz-main`, `/news?num=2&category=15`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (импортёры, владельцы бренда, маркетплейсы) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Импорт под своим брендом? Data Matrix в «Честном знаке» не заменяет товарный знак в Роспатенте — это три разных слоя до ФТС.

• GTIN в НК, КМ по 50 коп., нанесение до выпуска или границы ЕАЭС
• Таблица ЧЗ vs ТЗ vs ТРОИС и 7 шагов до ввода в оборот
• Штрафы 15.12 и автоштрафы с 01.09.2026 по 120-ФЗ

Читать: {PUBLIC_SITE_URL}/markirovka-importa-chestnyy-znak-i-tovarnyy-znak
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 15), если нет авто
- [ ] Рассмотреть inbound из L03/L18 на «честный знак импорт» / «бренд на маркетплейсе» (interlinker не сматчил `anchor_variants` L22)
- [ ] Outbound в L22: legacy чек-лист L01, CTA `/reg-tz-main`, рубрика «Бизнес», WB/Ozon edu — уже в `article.html`
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «честный знак импорт» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-30): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (27 статей в индексе; `anchor_variants` L22 не матчатся в чужих HTML). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (27 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L22 — **22** L-статьи с `canonical_path` (добавлен L22). Live publish не выполнялся.
