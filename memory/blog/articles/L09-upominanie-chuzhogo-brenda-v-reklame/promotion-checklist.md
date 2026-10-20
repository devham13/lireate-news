# Promotion checklist — L09 upominanie-chuzhogo-brenda-v-reklame

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/upominanie-chuzhogo-brenda-v-reklame` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`, `/news?num=2&category=9` (×2), `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (маркетинг, селлеры, ИП) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Назвали конкурента в баннере или ключах Директа? Матрица: сравнение, оригинал в обороте, ключ без знака на лендинге, логотип — отдельное согласие.

• ст. 1484 / 1487 / 1515 ГК и ст. 5, 10 ФЗ о рекламе — что в зелёной зоне
• Чек-лист из 9 шагов до запуска кампании
• При письме от бренда — маршрут ответа (L02)

Читать: {PUBLIC_SITE_URL}/upominanie-chuzhogo-brenda-v-reklame
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — рассмотреть inbound из L02/L07 на anchor «чужой бренд в рекламе» / «сравнительная реклама» (ручная вставка: interlinker не сматчил фразы)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «можно ли в рекламе упоминать чужие бренды — сравнение допустимых форматов» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-20): interlinker `--apply --blog-dir memory/blog/articles` — **0** автоматических вставок (14 статей; anchor_variants L09 не матчатся в чужих HTML; outbound на legacy чек-лист L01, гайд L02 `/news?num=2&category=9`, CTA защиты знака уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (14 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **9** L-статей с `canonical_path` (добавлен L09); копии `llms.txt` / `llms-full.txt` в каталоге L09.
