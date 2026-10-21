# Promotion checklist — L10 domennoe-imya-nma-ili-net

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/domennoe-imya-nma-ili-net` (заполнить после publish)  
Рубрика: Сайт (`category_id=12`) — `{PUBLIC_SITE_URL}/news?num=2&category=12`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (×2), `/news?num=2&category=9`, `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (бухгалтерия, ИТ, владельцы сайтов) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Домен на счёт 08 или в расходы при продлении? По ФСБУ 14/2022 отдельное имя редко НМА — смотрите пять признаков п. 4 и объект учёта (сайт vs домен).

• Первая регистрация при создании сайта → 08; продление после ввода → 26/44 или 97
• БУ и НУ: таблица различий, учётная политика
• До оплаты имени — чек-лист L01 и досудебные ограничения .RU (14 дней)

Читать: {PUBLIC_SITE_URL}/domennoe-imya-nma-ili-net
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 12), если нет авто
- [ ] После publish — рассмотреть inbound из L06/L01 на anchor «учёт домена» / «проверка ТЗ до регистрации домена» (ручная вставка: interlinker не сматчил фразы)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как учесть домен нма или нет» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-21): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (15 статей; anchor_variants L10 не матчатся в чужих HTML; outbound на legacy чек-лист L01 (×2), рубрика ТЗ `/news?num=2&category=9`, CTA защиты знака уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (15 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **10** L-статей с `canonical_path` (добавлен L10); копии `llms.txt` / `llms-full.txt` в каталоге L10.
