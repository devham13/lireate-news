# Promotion checklist — L45 nedobrosovestnaya-konkurenciya-kopirovanie-bez-tz

Дата публикации: 2026-11-11  
Live URL: `{PUBLIC_SITE_URL}/nedobrosovestnaya-konkurenciya-kopirovanie-bez-tz` (заполнить после publish)  
Рубрика: Бизнес (`category_id=15`) — `{PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L27 (`/narushenie-tovarnogo-znaka-na-marketpleyse/`); L37 (`/zashchita_dizayna_upakovki_marketpleysy/`); L24 (`/sajt-klon-zashchita-brenda-v-internete/`); CTA `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti/`
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
Без свидетельства на ТЗ: авторский контент карточки, жалоба МП по ст. 1253.1 и смешение по п. 2 ст. 14.6 135-ФЗ — не КоАП 14.6.

• развилка: АП / претензия / УФАС / ст. 14.33 КоАП
• outbound: L27, L37, L24
• когда регистрировать ТЗ — следующий шаг

Читать: {PUBLIC_SITE_URL}/nedobrosovestnaya-konkurenciya-kopirovanie-bez-tz
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 15), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как остановить копирование карточки товара недобросовестная конкуренция» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-11): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **0** автоматических вставок, затрагивающих L45 (52 статьи; `anchor_variants` L45 не сматчились в чужих HTML; outbound writer на L27, L37, L24, CTA уже в `article.html`). Дополнительно hub **L06**: **3** вставки (L29, L38, L18 → «классы МКТУ»). Inbound на L45 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (52 статьи, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **47** L-статей с `canonical_path` (добавлен L45); копии `llms.txt` / `llms-full.txt` в каталоге L45. Live publish не выполнялся.
