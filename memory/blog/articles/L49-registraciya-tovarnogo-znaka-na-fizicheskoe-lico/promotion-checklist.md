# Promotion checklist — L49 registraciya-tovarnogo-znaka-na-fizicheskoe-lico

Дата публикации: 2026-11-12  
Live URL: `{PUBLIC_SITE_URL}/registraciya-tovarnogo-znaka-na-fizicheskoe-lico` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L30 (`/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026`); L41 (`/otchuzhdenie-tovarnogo-znaka-dogovor-reestr`); L19 (legacy URL из writer); CTA `/registraciya_tovarnogo_znaka`
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
Одна заявка в Роспатент — разные последствия: ФЛ, ИП, ООО или самозанятый.

• после 193-ФЗ заявителем может быть гражданин без ИП
• пошлины ~35 000 ₽ одинаковы для всех форм
• передача в ООО — лицензия или отчуждение в реестре

Читать: {PUBLIC_SITE_URL}/registraciya-tovarnogo-znaka-na-fizicheskoe-lico
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Рассмотреть inbound из L30/L40 на anchor «товарный знак на физлицо» (interlinker не сматчил)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «регистрация товарного знака на физическое лицо» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-12): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (56 статей в индексе; `anchor_variants` L49 не сматчились в чужих HTML; outbound writer на L30, L41, L19 уже в `article.html`). Inbound на L49 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (56 статей, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/llms.txt` — **51** L-статья с `canonical_path` (добавлен L49 `/registraciya-tovarnogo-znaka-na-fizicheskoe-lico`); копии `llms.txt` / `llms-full.txt` в каталоге L49. Live publish не выполнялся.
