# Promotion checklist — L25 registraciya-brenda-odezhdy-mktu

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/registraciya-brenda-odezhdy-mktu` (заполнить после publish)  
Рубрика: Бренд (`category_id=13`) — `{PUBLIC_SITE_URL}/news?num=2&category=13`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/blog/kak-opredelit-klass-mktu/` (interlink L25→L06); `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`; `/reg-tz-main` (≤3); рубрика `/news?num=2&category=13`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (швейные бренды, селлеры WB/Ozon, D2C) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Бренд в кабинете маркетплейса ≠ свидетельство ТЗ: для одежды минимум класс 25, при своих продажах — 35; бирка через 25, а не путать с 24 (240102).

• Пошлины: 35 000 ₽ за класс; сценарий 25+35 — 38 500 ₽ (до 10 поз./класс)
• Слово и лого — часто две заявки (п. 2 ст. 1492)
• Проверка в Поисковой платформе до оплаты пошлин

Читать: {PUBLIC_SITE_URL}/registraciya-brenda-odezhdy-mktu
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 13), если нет авто
- [ ] Рассмотреть inbound из L03/L17/L18 на «бренд одежды» / «Wildberries» / «классы МКТУ» (ручная вставка, если `anchor_variants` L25 не сматчатся в чужих HTML)
- [ ] Outbound в L25: interlink на L06 «классы МКТУ»; чек-лист L01 и CTA `/reg-tz-main` уже в `article.html`
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как зарегистрировать бренд одежды» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-31): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** вставка в L25 (L25 → L06 по «классы МКТУ»); повторная **1** вставка L24 → L06 (slug ещё не был в HTML на ветке). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (30 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L25 — **25** L-статей с `canonical_path` (добавлен L25). Live publish не выполнялся.
