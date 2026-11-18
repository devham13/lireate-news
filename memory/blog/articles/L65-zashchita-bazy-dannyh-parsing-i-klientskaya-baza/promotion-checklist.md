# Promotion checklist — L65 zashchita-bazy-dannyh-parsing-i-klientskaya-baza

Дата публикации: 2026-11-18  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/klientskaya_baza_katalog_i_parsing_kak_zaschitit_bazu_dannyix_po_gk_rf/` (подтвердить после INSERT на хостинге)  
Рубрика: Авторское право (`category_id=17`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image (collage-v1), FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L23, L14, L32, L20, L45; legal pages КТ; CTA Telegram
- [ ] Collage: cover `lx-article-cover` + 3× `inline-collage` в `full_story`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи, `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (e‑commerce, SaaS, владельцы каталогов) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Конкурент слил каталог роботом? CRM и публичная витрина — разные режимы: ст. 1334, 98-ФЗ и 152-ФЗ.

• Три контура: каталог / закрытая CRM / ПДн
• Изготовитель по ст. 1333, оферта против автосбора
• Чек-лист 72 часа и претензия по ст. 1311

Читать: {LIREATE_PUBLIC_SITE_URL}/klientskaya_baza_katalog_i_parsing_kak_zaschitit_bazu_dannyix_po_gk_rf/
```

## Перелинковка

- [ ] Outbound L65→L23/L14/L32/L20/L45 — уже в `article.html` (writer)
- [ ] Рассмотреть inbound из L23 на anchor «парсинг каталога» / «клиентская база» (interlinker **0** матчей по `anchor_variants` L65)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «защита клиентской базы данных» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-18): CLI `--article-dir` не поддерживается — запуск `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (70 статей в индексе). Outbound writer: L23, L14, L32, L20, L45, `/rezhim_kommercheskoy_taynyi_*`, `/nedobrosovestnaya_konkurenciya_*`. `memory/blog/interlink-suggestions.json` обновлён. Cover: `lireate_collage_publish_gate.py` → **PASS** (`lx-article-cover` + inline-01..03 уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (70 статей, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` → **65** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L65 по `canonical_path`); копия `llms.txt` в каталоге L65. Live publish: **не выполнялся** (`publish:no`; выкладка — CRON REG.RU после merge).