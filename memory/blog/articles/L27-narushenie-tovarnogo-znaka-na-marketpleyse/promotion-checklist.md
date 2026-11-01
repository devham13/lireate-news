# Promotion checklist — L27 narushenie-tovarnogo-znaka-na-marketpleyse

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/narushenie-tovarnogo-znaka-na-marketpleyse` (заполнить после publish)  
Рубрика: Бизнес (`category_id=15`) — `{PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/kak_zaregistrirovat_brend_na_ozon_i_wildberries_proverka_imeni_i_nuzhen_li_tz` (L03); `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/` (L02); `/reg-tz-main`; рубрика `/news?num=2&category=15`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (правообладатели, селлеры MP, in-house юристы бренда) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Чужой логотип на карточке WB/Ozon? Сначала свидетельство и МКТУ, потом скрин с URL и артикулом — жалоба площадке не заменяет претензию селлеру по ст. 1515.

• Цифровой арбитраж WB и brand.ozon.ru — разные сроки ответа
• 30 дней между ИП/юрлицами перед иском о компенсации
• Диапазон 10 000–10 000 000 ₽ с 04.01.2026 — обоснуйте фактами

Читать: {PUBLIC_SITE_URL}/narushenie-tovarnogo-znaka-na-marketpleyse
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 15), если нет авто
- [ ] Рассмотреть inbound из L03/L24/L02 на «нарушение ТЗ на маркетплейсе» / «жалоба правообладателя» (ручная вставка, если `anchor_variants` L27 не сматчились в чужих HTML)
- [ ] Outbound в L27: writer L02/L03 + `/reg-tz-main`; interlinker — **0** автоматических вставок (slug L27 уже не требует hub-матча)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «нарушение товарного знака на маркетплейсе» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-01): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (32 статьи в индексе; `anchor_variants` L27 не матчатся в чужих HTML без slug; outbound L02/L03/reg-tz-main уже в `article.html`). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (32 статьи, `/blog/{slug}/`, site-base Lireate); `memory/blog/lireate-site/` и копии в каталоге L27 — **27** L-статей с `canonical_path` (добавлен L27). Live publish не выполнялся.
