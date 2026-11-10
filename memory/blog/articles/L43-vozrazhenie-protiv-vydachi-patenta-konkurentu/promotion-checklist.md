# Promotion checklist — L43 vozrazhenie-protiv-vydachi-patenta-konkurentu

Дата публикации: 2026-11-10  
Live URL: `{PUBLIC_SITE_URL}/vozrazhenie-protiv-vydachi-patenta-konkurentu` (заполнить после publish)  
Рубрика: Патент (`category_id=20`) — `{PUBLIC_SITE_URL}/news?num=2&category=20`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L04, L05, L08, L31; CTA `/patent`
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
Конкуренту выдали патент на ваш рынок? В РФ нет «оппозиции на 6 месяцев» — есть замечания по заявке и возражение в ППС.

• до выдачи — замечания по ст. 1386 без п. 1.27.3
• после выдачи — ППС, 7 000 ₽ за независимый пункт (п. 1.27.3)
• не путать с отказом вам (L04) и возражением по ТЗ (L08)

Читать: {PUBLIC_SITE_URL}/vozrazhenie-protiv-vydachi-patenta-konkurentu
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 20), если нет авто
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «возражение против выдачи патента» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-10): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (48 статей; `anchor_variants` L43 не сматчились в чужих HTML; outbound writer на L04, L05, L08, L31, `/patent` уже в `article.html`). Inbound на L43 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (48 статей, `/blog/{slug}/`, site-base example.com); `memory/blog/lireate-site/` — **43** L-статьи с `canonical_path` (добавлен L43); копии `llms.txt` / `llms-full.txt` в каталоге L43. Live publish не выполнялся.

Publish prep (2026-11-10): `excalibur_blog_link_verify.py` PASS (0 failed, `privacy_policy_violations` []); `lireate_collage_publish_gate.py` PASS; `lireate_hosting_publish.py --dry-run` → `seo_url`: `vozrazhenie_protiv_vydachi_patenta_konkurentu`, `category`: 20; артефакт `lireate-publish-result.json` (`verdict`: `dry_run`). Live INSERT на хостинге не выполнялся (ожидание merge + CRON/`LIREATE_ALLOW_PUBLISH=yes` на REG.RU).
