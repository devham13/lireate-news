# Promotion checklist — L67 chestnyy-znak-import-prostymi-slovami

Дата публикации: 2026-11-18  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/chestnyy-znak-import-prostymi-slovami/` (подтвердить после INSERT на хостинге)  
Рубрика: Маркировка (`category_id=11`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=11`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/mozhno-li-zapretit-vvoz-analoga-zapatentovannogo-tovara/` (interlinker ТРОИС); `/registraciya_tovarnogo_znaka/`; CTA Telegram
- [ ] Рассмотреть ручной inbound на L56 «ТРОИС» во втором абзаце (interlinker: 2nd opportunity не применён — фраза уже в ссылке)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (импортёры, маркетплейсы, владельцы бренда) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Импорт и «Честный знак»: Data Matrix и поле «товарный знак» в НК — не то же самое, что ® в Роспатенте.

• ТН ВЭД + checking_codes, УКЭП, КМ по 50 коп., «Ввезен в РФ»
• Графа 31 и ввод с ФТС до витрины WB
• ТРОИС отдельно от заказа кодов

Читать: {LIREATE_PUBLIC_SITE_URL}/chestnyy-znak-import-prostymi-slovami/
```

## Перелинковка

- [ ] Outbound indexer L67→L31 (ТРОИС) — в `article.html`
- [ ] Outbound writer: `/registraciya_tovarnogo_znaka/`, markirovka.ru, docs.crpt.ru — без изменений indexer
- [ ] Рассмотреть inbound из L22/L56 на «честный знак импорт простыми словами» / anchor_variants L67
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как пройти честный знак импорт простыми словами» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-18): CLI `--article-dir` не поддерживается — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** автоматическая вставка **L67→L31** (якорь «таможенный реестр объектов интеллектуальной собственности»); вторая opportunity L67→L56 не применена (контекст уже залинкован). Inbound на L67 — **0**. `memory/blog/interlink-suggestions.json` обновлён (72 статьи, 2 opportunities). llms: `memory/blog/llms.txt` + `llms-full.txt` (72 статьи, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` с `LIREATE_PUBLIC_SITE_URL=https://example.invalid` → **67** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L67 `/chestnyy-znak-import-prostymi-slovami`); копия `memory/blog/llms.txt` в каталоге L67. Live publish / WP: **не выполнялся** (выкладка — CRON REG.RU после merge).