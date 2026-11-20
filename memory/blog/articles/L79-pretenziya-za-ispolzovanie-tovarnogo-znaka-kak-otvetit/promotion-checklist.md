# Promotion checklist — L79 pretenziya-za-ispolzovanie-tovarnogo-znaka-kak-otvetit

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/pretenziya_za_ispolzovanie_tovarnogo_znaka_kak_otvetit/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/narushayut_tovarnyy_znak_chto_delat_pravoobladatelyu/` (L78), `/poluchili_pretenziyu_ot_pravoobladatelya_chto_proverit/`, `/struktura_mktu_kak_opredelit_klass_dlya_tovara_i_uslugi/`, `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/` (L02), `/kak_obosnovat_snizhenie_kompensatsii_za_narushenie_prav/` (×2), `/kak_zashchitit_intellektualnye_prava_v_sude/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (селлеры, ответчики по ТЗ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Требуют деньги за бренд? Сначала реестр, МКТУ и способ использования — не платите вслепую.

• ст. 1484 и п. 4 ст. 1515 в одном чек-листе
• ответ без признания вины; календарь L02
• контррасчёт → L76

Читать: {LIREATE_PUBLIC_SITE_URL}/pretenziya_za_ispolzovanie_tovarnogo_znaka_kak_otvetit/
```

## Перелинковка

- [ ] **После live L79:** L76 FAQ — ссылка на L79 (уже в L76 inbound interlinker); L02 — уточнить разводку «календарь vs ТЗ-диагностика»
- [ ] **После live L78:** двусторонняя связка с L78 (истец / ответчик)
- [ ] Inbound из L75 «письмо только по ТЗ» на anchor L79
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «претензия за использование товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-20): interlinker — **2** авто (L79→L78, L79→L06); исправлен href L78 на underscore canonical. Outbound writer: L75, L02, L76, L74. Inbound: L76 FAQ (interlinker, href исправлен). llms: см. L77 notes; копии в каталоге.