# Promotion checklist — L78 narushayut-tovarnyy-znak-chto-delat-pravoobladatelyu

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/narushayut_tovarnyy_znak_chto_delat_pravoobladatelyu/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/` (×2), `/pretenziya_za_ispolzovanie_tovarnogo_znaka_kak_otvetit/` (L79, ручной), `/kak_zashchitit_intellektualnye_prava_v_sude/` (×2), `/poluchili_pretenziyu_ot_pravoobladatelya_chto_proverit/`, `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (правообладатели, производители, селлеры с ТЗ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Конкурент тянет ваш бренд? Реестр → сходство → фиксация URL → претензия 30 дней.

• ст. 1484 и п. 55 ППВС № 10
• компенсация 10 000–10 000 000 ₽ (с 04.01.2026)
• маршрут истца до арбитража

Читать: {LIREATE_PUBLIC_SITE_URL}/narushayut_tovarnyy_znak_chto_delat_pravoobladatelyu/
```

## Перелинковка

- [ ] **После live L78:** L79 — cross-link «ответчик» ↔ «правообладатель»; L27 — inbound с маркетплейсов; L45 — недобросовестная конкуренция
- [ ] **После live L79:** inbound из intro L79 на L78 (live canonical с underscore)
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «нарушение прав на товарный знак что делать» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-20): interlinker — **0** авто в L78; ручной outbound L78→L79 в блоке про ответ оппонента; writer links L02, L74, L75. Inbound: L79→L78 (interlinker, исправлен href на `lireate_seo_url`). llms: см. L77 notes; копии в каталоге.