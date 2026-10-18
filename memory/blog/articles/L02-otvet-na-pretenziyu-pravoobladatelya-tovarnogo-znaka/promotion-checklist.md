# Promotion checklist — L02 otvet-na-pretenziyu-pravoobladatelya-tovarnogo-znaka

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/otvet-na-pretenziyu-pravoobladatelya-tovarnogo-znaka` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (theme или plugin)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`, `/7_prichin_zaregestrirovat_tovarnyiy_znak`, `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, селлеры, бренд) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Претензия по товарному знаку? Не платите и не признавайте вину вслепую — у вас окно ~30 дней до риска иска по компенсации.

• Первые 10 дней: реестры ФИПС, сходство, ст. 1487, ст. 1483
• Структура ответа без признания вины + контррасчёт (лимиты с 04.01.2026)
• Шаблон формулировок для ИП и маркетплейсов

Читать: {PUBLIC_SITE_URL}/otvet-na-pretenziyu-pravoobladatelya-tovarnogo-znaka
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Обновить L01 (`/proverka-tovarnogo-znaka-pered-podachey-v-rospatent`) → ссылка на L02 при публикации (anchor «ответ на претензию» / «досудебная претензия»)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «ответ на претензию о нарушении исключительных прав на товарный знак» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-18): interlinker `--apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL` — **0** автоматических вставок (7 статей; anchor_variants L01/L02 не матчатся в чужих HTML; outbound на lireate legacy URL и `/7_prichin…`, `/kak_zaschitit…` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (7 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — 2 L-статьи с `canonical_path`; копии `llms.txt` / `llms-full.txt` в каталоге статьи.
