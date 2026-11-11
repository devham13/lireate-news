# Promotion checklist — L51 patent-na-poleznuyu-model-rospatent

Дата публикации: 2026-11-11  
Live URL: `{PUBLIC_SITE_URL}/patent_na_poleznuyu_model_rospatent` (заполнить после publish)  
Рубрика: Патент (`category_id=20`) — `{PUBLIC_SITE_URL}/news?num=2&category=20`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage + HowTo (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L05 (`/patent`), отказ L04 (`/otkazali_v_vyidache_patenta_chto_delat_dalshe_sroki_pps_i_povtornaya_zayavka/`), L43 (`/vozrazhenie_protiv_vydachi_patenta_konkurentu/`), CTA `/patent`
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
Патент на полезную модель — это устройство по ст. 1351, не «идея» и не способ.

• минимум пошлин 15 000 ₽ (п. 1.2 + 1.9 + 1.17)
• экспертиза по существу для ПМ — автоматически (ст. 1390)
• срок охраны 10 лет; после публичного показа — 6 месяцев на подачу

Читать: {PUBLIC_SITE_URL}/patent_na_poleznuyu_model_rospatent
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 20), если нет авто
- [ ] Рассмотреть inbound из L05 на anchor «полезная модель» / «устройство» (interlinker не сматчил)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «патент на полезную модель роспатент» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-11): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **0** автоматических вставок (53 статьи в индексе; `anchor_variants` L51 не сматчились в чужих HTML; outbound writer на `/patent`, L04, L43 уже в `article.html`). Inbound на L51 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (53 статьи, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **48** L-статей с `canonical_path` (добавлен L51 `patent_na_poleznuyu_model_rospatent`); копии `llms.txt` / `llms-full.txt` в каталоге L51. Live publish не выполнялся.
