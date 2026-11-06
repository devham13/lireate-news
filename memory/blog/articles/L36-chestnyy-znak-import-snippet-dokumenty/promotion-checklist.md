# Promotion checklist — L36 chestnyy-znak-import-snippet-dokumenty

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/chestnyy-znak-import-snippet-dokumenty` (заполнить после publish)  
Рубрика: Маркировка (`category_id=11`) — `{PUBLIC_SITE_URL}/news?num=2&category=11`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links и CTA из статьи (200)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (импорт, маркировка) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Сниппет в «Честном знаке» после обмена с ФТС? Часто рвётся не «черновик», а цепочка: ЕРВК → заказ «Ввезен в РФ» → графа 31 → ввод.

• ошибка FtsGoodsReleaseMarkRes_orh / attachment — полный XML и support@crpt.ru
• ЕРВК с 01.03.2026: без уведомления у новых — отказ
• 7 шагов и таблица узлов — в материале

Читать: {PUBLIC_SITE_URL}/chestnyy-znak-import-snippet-dokumenty
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 11), если нет авто
- [ ] Outbound в L36: markirovka.ru, docs.crpt.ru, kv-ai.ru (Make), Telegram — проверить 200 после деплоя
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как исправить сниппет честный знак импорт» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-06): `excalibur_blog_interlinker.py` в репозитории не принимает `--article-dir`; выполнено `--apply --blog-dir memory/blog/articles` — **0** автоматических вставок (41 статья; новых матчей по anchor_variants нет). `memory/blog/interlink-suggestions.json` обновлён. llms: в `memory/blog/llms.txt` и конец `memory/blog/llms-full.txt` дописана только **L36** (без полной перегенерации всего индекса; URL с `https://example.com/blog/...` как в остальных строках репо-индекса); канон для Lireate: `memory/blog/lireate-site/llms.txt` + `llms-full.txt` — строка L36 + полный блок с `canonical_path`; копии в каталоге статьи. Live publish не выполнялся.
