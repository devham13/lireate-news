# Promotion checklist — L57 naricatelnye-brendy-aspirin-obobshchenie

Дата публикации: 2026-11-13  
Live URL: `{PUBLIC_SITE_URL}/naricatelnye-brendy-aspirin-obobshchenie` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L01 (`/proverka_tovarnogo_znaka_pered_registraciey_chek_list…`), L40 (`/nuzhno-li-registrirovat-tovarnyy-znak/`), CTA `/registraciya_tovarnogo_znaka/`; consultant-ссылки на ГК РФ (1483, 1514, 1486, 1512)
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
«Принеси скотч» — для владельца ТЗ это не комплимент: имя бренда подменило вид товара.

• п. 1 и п. 3 ст. 1483 vs п. 6 ст. 1514 и ст. 1486 — разные процедуры
• самотест: 8 красных флагов обобщения
• brand guidelines, договоры с дилерами и архив для Роспатента

Читать: {PUBLIC_SITE_URL}/naricatelnye-brendy-aspirin-obobshchenie
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 9), если нет авто
- [ ] Inbound автолинков на L57 — **0** (anchor_variants L57 не сматчились в чужих HTML на этом прогоне)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как не допустить обобщения бренда нарицательное наименование» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-13): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **1** автоматическая вставка на весь индекс (L59→L06 «классы МКТУ»; к L57 напрямую **0** inbound/outbound interlinker). Outbound writer: L01 (×2), L40, CTA `/registraciya_tovarnogo_znaka/` уже в `article.html`. `memory/blog/interlink-suggestions.json` обновлён (63 статьи, 1 opportunity). llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (63 статьи, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` → **58** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L57); копии `llms.txt` / `llms-full.txt` в каталоге L57. Live publish **не** выполнялся.
