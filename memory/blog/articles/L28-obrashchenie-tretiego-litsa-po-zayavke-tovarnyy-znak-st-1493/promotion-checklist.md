# Promotion checklist — L28 obrashchenie-tretiego-litsa-po-zayavke-tovarnyy-znak-st-1493

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/obrashchenie-tretiego-litsa-po-zayavke-tovarnyy-znak-st-1493` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/vozrazhenie_protiv_registracii_chuzhogo_tovarnogo_znaka_sroki_i_poryadok` (L08); `/osparivanie_tovarnogo_znaka_v_rospatente_kak_podat_vozrazhenie` (L21); `/reg-tz-main`; рубрика `/news?num=2&category=9`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (правообладатели, in-house юристы, патентные поверенные) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Чужая заявка в бюллетене? До свидетельства — не ППС с 14 000 ₽, а обращение по ст. 1493 с номером заявки и доводами по 1483.

• Любое лицо после публикации заявки, без «3 месяцев» в ГК
• Почта, окно, ФИПС, ЕПГУ — без пошлины 2.28.4
• После регистрации — ветка 1512–1513 (L08)

Читать: {PUBLIC_SITE_URL}/obrashchenie-tretiego-litsa-po-zayavke-tovarnyy-znak-st-1493
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Inbound: L21 → L28 (2 автоматические вставки interlinker по primary/secondary query; slug L28 в HTML L21)
- [ ] Outbound в L28: writer — L08, L21, `/reg-tz-main`; interlinker в L28 — **0** (slug L08/L21 уже в HTML)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «возражение на заявку на товарный знак» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-02): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **2** inbound в L21 → L28 (`/blog/obrashchenie-tretiego-litsa-po-zayavke-tovarnyy-znak-st-1493/`; 3-я возможность «куда подается…» не применена — overlap в том же абзаце). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (33 статьи, `/blog/{slug}/`, site-base Lireate); `memory/blog/lireate-site/` и копии в каталоге L28 — **28** L-статей с `canonical_path` (добавлен L28). Live publish не выполнялся.
