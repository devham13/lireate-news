# Promotion checklist — L48 ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu

Дата публикации: 2026-11-11  
Live URL: `{PUBLIC_SITE_URL}/ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L30 (`/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026`); L07 (`/otnositelnyie_osnovaniya_otkaza_v_registracii_tz_otvet_ekspertize`); L08 (`/vozrazhenie_protiv_registracii_chuzhogo_tovarnogo_znaka_sroki_i_poryadok`); CTA `/registraciya_tovarnogo_znaka`
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
Экспертиза ТЗ — две стадии: формальная (ст. 1498) и по существу (ст. 1499).

• формальная — до 1 мес., без проверки сходства
• по существу — до 12 мес.; на уведомление по п. 3 ст. 1499 — 6 мес. на доводы
• не путать запрос (3 мес.) и уведомление (6 мес.)

Читать: {PUBLIC_SITE_URL}/ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Рассмотреть inbound из L30/L07 на anchor «экспертиза товарного знака» (interlinker не сматчил)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как проходит экспертиза товарных знаков» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-11): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (55 статей в индексе; `anchor_variants` L48 не сматчились в чужих HTML; outbound writer на L30, L07, L08, `/registraciya_tovarnogo_znaka` уже в `article.html`). Inbound на L48 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (55 статей, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **50** L-статей с `canonical_path` (добавлен L48 `/ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu`); копии `llms.txt` / `llms-full.txt` в каталоге L48. Live publish не выполнялся.
