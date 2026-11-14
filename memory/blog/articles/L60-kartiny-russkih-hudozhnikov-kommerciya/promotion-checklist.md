# Promotion checklist — L60 kartiny-russkih-hudozhnikov-kommerciya

Дата публикации: 2026-11-14  
Live URL: `{PUBLIC_SITE_URL}/kartiny-russkih-hudozhnikov-kommerciya/` (заполнить после publish)  
Рубрика: Авторское право (`category_id=17`) — `{PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L35 (`/avtorskoe-voznagrazhdenie-po-gk-rf/`); CTA Telegram/WhatsApp/MAX
- [ ] Inbound: L17 → L60 на «свободное использование»
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (маркетологи, селлеры мерча) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Картина в таргете и на футболке — не «бесплатный декор»: 70 лет по ст. 1281, ст. 1274 не для рекламы, у музея — ст. 36 54-ФЗ.

• Различить образ полотна и JPG с сайта ГТГ / Пушкинского
• Общественное достояние ≠ право копировать музейный файл
• 9 шагов в чек-листе до запуска мерча и таргета

Читать: {PUBLIC_SITE_URL}/kartiny-russkih-hudozhnikov-kommerciya/
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 17), если нет авто
- [ ] Inbound L17 → L60 (interlinker на «свободное использование»; href приведён к `/kartiny-russkih-hudozhnikov-kommerciya/`)
- [ ] Рассмотреть anchor L13 ↔ L60 (некоммерция vs коммерция) вручную после publish
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`; поправить `/blog/*` на live `canonical_path` при необходимости

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «чек-лист использование изображений картин русских художников в коммерческих целях» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-14): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **1** автоматическая вставка (inbound L17→L60 по secondary «свободное использование»); href `/blog/kartiny-russkih-hudozhnikov-kommerciya/` заменён на `/kartiny-russkih-hudozhnikov-kommerciya/` для live. Outbound writer: L35 (×2) уже в `article.html`. `memory/blog/interlink-suggestions.json` (65 статей, 1 opportunity). llms: `memory/blog/llms.txt` + `llms-full.txt` (65 статей, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **60** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L60); копии `llms.txt` / `llms-full.txt` в каталоге L60. Live publish не выполнялся.

Hosting publish prep (2026-11-14): `excalibur_blog_link_verify.py --site-base $LIREATE_PUBLIC_SITE_URL` → **pass** (21 ссылок; `privacy_policy_violations: []`). `lireate_collage_publish_gate.py` → **PASS**. `lireate_hosting_publish.py --dry-run` → **DRY_RUN** (`seo_url`: `chek_list_kartinyi_russkix_xudozhnikov_v_kommercii_sroki_i_isklyucheniya`, `category`: **17**, 6 image files). `lireate-publish-result.json` + `publish-bundle/` в каталоге статьи. **БД INSERT не выполнялся**; `shared/published-articles-lireate.md` не трогали. Live после merge → CRON `lireate_hosting_cron.sh` (на сервере `LIREATE_ALLOW_PUBLISH=yes`).