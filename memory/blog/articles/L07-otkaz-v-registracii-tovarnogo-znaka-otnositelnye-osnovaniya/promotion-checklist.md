# Promotion checklist — L07 otkaz-v-registracii-tovarnogo-znaka-otnositelnye-osnovaniya

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/otkaz-v-registracii-tovarnogo-znaka-otnositelnye-osnovaniya` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (×2), `/blog/kak-opredelit-klass-mktu/`, `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, заявители ТЗ, селлеры) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Отказ в регистрации ТЗ по п. 6–10 ст. 1483? Не путайте уведомление (6 мес. на доводы) и возражение в ППС (4 мес., 9 000 ₽).

• Таблица относительных оснований и сроков с даты направления письма
• Письмо-согласие, сужение МКТУ, аргументы о несходстве в Поисковой платформе
• Чек-лист полей согласия и типовых ошибок перед подачей

Читать: {PUBLIC_SITE_URL}/otkaz-v-registracii-tovarnogo-znaka-otnositelnye-osnovaniya
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — рассмотреть inbound из L01/L02 на anchor «относительные основания» / «ответ на уведомление экспертизы» (ручная вставка, если interlinker не сматчит)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «относительные основания для отказа в регистрации товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-20): interlinker `--apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL` — **1** вставка (L07 → L06 по «классы МКТУ»; outbound на чек-лист L01, `/reg-tz-main` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (12 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — 7 L-статей с `canonical_path`; копии `llms.txt` / `llms-full.txt` в каталогах L01–L07.
