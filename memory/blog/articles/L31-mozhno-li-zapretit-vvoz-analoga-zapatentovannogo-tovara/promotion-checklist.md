# Promotion checklist — L31 mozhno-li-zapretit-vvoz-analoga-zapatentovannogo-tovara

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/mozhno-li-zapretit-vvoz-analoga-zapatentovannogo-tovara` (заполнить после publish)  
Рубрика: Патент (`category_id=8`) — `{PUBLIC_SITE_URL}/news?num=2&category=8`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/news?num=2&category=20` (L05); `/patent`; рубрика `/news?num=2&category=8`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (патентообладатели, импортёры, in-house IP) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Патент на ввоз аналога на таможне одной заявкой не блокируется: в ТРОИС — знаки, не формула изобретения. По бренду на упаковке — приостановление 7–10 раб. дней; спор о конструкции — претензия и иск.

• ст. 1358 — право на ввоз vs отсутствие патента в реестре ФТС
• ст. 328 / 113 289-ФЗ — ТРОИС и сроки
• Перечень Минпромторга — параллельный импорт оригинала

Читать: {PUBLIC_SITE_URL}/mozhno-li-zapretit-vvoz-analoga-zapatentovannogo-tovara
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 8), если нет авто
- [ ] Рассмотреть inbound из L04/L05/L22 на «таможня / патент / ТРОИС / параллельный импорт» (ручная вставка, если `anchor_variants` L31 не сматчились в чужих HTML)
- [ ] Outbound в L31: writer — L05 (`/news?num=2&category=20`), `/patent`; interlinker inbound на L31 — **0**; interlinker hub **2** вставки (L29→L06, L30→L06 по «классы МКТУ» — повтор на ветке L31)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как запретить ввоз аналога запатентованного продукта» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-04): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **2** автоматические вставки (L29→L06, L30→L06 по «классы МКТУ»; inbound на L31 — **0**, `anchor_variants` L31 не сматчились в чужих HTML). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (36 статей, `/blog/{slug}/`, site-base Lireate); `memory/blog/lireate-site/` и копии в каталоге L31 — **31** L-статья с `canonical_path` (добавлен L31). Live publish не выполнялся.
