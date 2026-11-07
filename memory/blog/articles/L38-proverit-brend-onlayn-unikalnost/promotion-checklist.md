# Promotion checklist — L38 proverit-brend-onlayn-unikalnost

Дата публикации: 2026-11-07  
Live URL: `{PUBLIC_SITE_URL}/proverit-brend-onlayn-unikalnost` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L01, L29, L10; `/reg-tz-main`; `/kak_proverit_brend_na_wildberries_svoboden_li_tovarnyy_znak`; inbound `/blog/kak-zapatentovat-nazvanie-i-logotip/`, `/blog/kak-opredelit-klass-mktu/`
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
Свободный .ru не значит свободный бренд: за вечер — Роспатент, ЕГРЮЛ, whois и ники.

• четыре независимых слоя «онлайн-следа»
• домен ≠ товарный знак
• таблица рисков и когда менять имя

Читать: {PUBLIC_SITE_URL}/proverit-brend-onlayn-unikalnost
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «проверить бренд на уникальность онлайн» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-07): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles` (site-base из env при apply) — **3** автоматические вставки: **L38→L34** (лид, якорь «проверить бренд на уникальность онлайн» → `/blog/kak-zapatentovat-nazvanie-i-logotip/`); **L38→L06** («классы МКТУ» → `/blog/kak-opredelit-klass-mktu/`); **L37→L06** (таблица, «Классы МКТУ»). Inbound на L38 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (43 статьи, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **38** L-статей с `canonical_path` (добавлен L38 `/proverit-brend-onlayn-unikalnost`); копии `llms.txt` / `llms-full.txt` в каталоге L38. Live publish не выполнялся.
