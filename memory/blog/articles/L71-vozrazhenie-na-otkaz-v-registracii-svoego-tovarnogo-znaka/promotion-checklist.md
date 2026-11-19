# Promotion checklist — L71 vozrazhenie-na-otkaz-v-registracii-svoego-tovarnogo-znaka

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/vozrazhenie-na-otkaz-v-registracii-svoego-tovarnogo-znaka/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/otnositelnyie_osnovaniya_otkaza_v_registracii_tz_otvet_ekspertize/` (L07), `/ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu/` (L48), `/dorabotka-logotipa-pered-registraciey-tovarnogo-znaka/` (L39), `/vozrazhenie_protiv_registracii_chuzhogo_tovarnogo_znaka_sroki_i_poryadok/` (L08, граница), `/registraciya_tovarnogo_znaka/` (CTA)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (заявители ТЗ, предприниматели после отказа) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
После отказа в регистрации своего знака — возражение в ППС по ст. 1500 за 4 месяца (не путать с уведомлением за 6 мес.).

• 9 000 ₽ по п. 2.28.2 и запрос копий за 2 месяца
• Таблица: уведомление vs решение vs возражение против чужого знака
• Сервис «Обращения в ППС» на ФИПС

Читать: {LIREATE_PUBLIC_SITE_URL}/vozrazhenie-na-otkaz-v-registracii-svoego-tovarnogo-znaka/
```

## Перелинковка

- [ ] Outbound writer: L07, L48, L39, L08 (граница), CTA `/registraciya_tovarnogo_znaka/` — без изменений indexer
- [ ] Рассмотреть inbound из L07/L08 на anchor_variants L71 (ст. 1500, 4 месяца, 9 000 ₽) после publish
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как подать возражение на отказ в регистрации товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-19): CLI `--article-dir` не поддерживается — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base https://example.com` — **0** автоматических вставок (79 статей в индексе; `anchor_variants` L71 не сматчились в чужих HTML без правок; outbound writer уже в `article.html`). `memory/blog/interlink-suggestions.json` обновлён (79 статей, 0 opportunities). llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (79 статей, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` (`LIREATE_PUBLIC_SITE_URL=https://example.invalid`) → **74** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L71); в `memory/blog/lireate-site/llms-full.txt` добавлен полный блок L71 (`/vozrazhenie-na-otkaz-v-registracii-svoego-tovarnogo-znaka`); копия `llms.txt` в каталоге L71. Live publish **не** выполнялся (CRON REG.RU после merge).