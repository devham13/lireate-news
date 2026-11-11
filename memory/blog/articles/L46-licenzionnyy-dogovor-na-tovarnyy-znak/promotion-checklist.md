# Promotion checklist — L46 licenzionnyy-dogovor-na-tovarnyy-znak

Дата публикации: 2026-11-11  
Live URL: `{PUBLIC_SITE_URL}/licenzionnyy-dogovor-na-tovarnyy-znak` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L41 (`/otchuzhdenie-tovarnogo-znaka-dogovor-reestr/`); L40 (`/nuzhno-li-registrirovat-tovarnyy-znak/`); L19 (`/chto_delat_esli_tovarnyiy_znak_zanyat/`); L03 (`/kak_zaregistrirovat_brend_na_ozon_i_wildberries_proverka_imeni_i_nuzhen_li_tz/`); L06 (`/kak-opredelit-klass-mktu/` или `/blog/kak-opredelit-klass-mktu/` после interlinker); CTA `/registraciya_tovarnogo_znaka/`
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
Без записи лицензии на ТЗ в Роспатенте право использования несостоявшееся (ст. 1232 п. 6).

• письменная форма и вид лицензии (ст. 1490; иначе простая — ст. 1236 п. 2)
• пошлина п. 3.10: 15 000 ₽ за знак
• сублицензия — только с согласием (ст. 1238)

Читать: {PUBLIC_SITE_URL}/licenzionnyy-dogovor-na-tovarnyy-znak
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как оформить лицензионный договор на товарный знак» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-11): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **1** автоматическая вставка **L46→L06** («классы МКТУ» → `/blog/kak-opredelit-klass-mktu/`). Inbound на L46 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (54 статьи, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **49** L-статей с `canonical_path` (добавлен L46 `/licenzionnyy-dogovor-na-tovarnyy-znak`); копии `llms.txt` / `llms-full.txt` в каталоге L46. Live publish не выполнялся.
