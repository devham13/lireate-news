# Promotion checklist — L77 patentnyy-trolling-kak-proverit-pretenziyu-i-zashchititsya

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/patentnyy_trolling_kak_proverit_pretenziyu_i_zashchititsya/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Бизнес (`category_id=15`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/poluchili_pretenziyu_ot_pravoobladatelya_chto_proverit/` (×2), `/patentnyie_trolli_kto_oni/` (×2), `/kak_obosnovat_snizhenie_kompensatsii_za_narushenie_prav/`, `/kak_zashchitit_intellektualnye_prava_v_sude/`, `/struktura_mktu_kak_opredelit_klass_dlya_tovara_i_uslugi/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (селлеры, ответчики массовых претензий) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Массовая претензия по ИС? Сначала реестр и досье на истца, не перевод денег.

• матрица злоупотребления по ст. 10 и Обзору ВС 2023
• встречные 1486 / 1512–1513
• ответ без признания вины → связка L75 + L76

Читать: {LIREATE_PUBLIC_SITE_URL}/patentnyy_trolling_kak_proverit_pretenziyu_i_zashchititsya/
```

## Перелинковка

- [ ] **После live L77:** L75 — inbound «сценарий троллинга / злоупотребление»; L79 — различие «узкий ТЗ» vs «троллинг»
- [ ] Inbound из L75 в FAQ «недобросовестный правообладатель» на L77
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «патентный троллинг как защититься» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-20): interlinker full blog — **1** авто (L77→L06 «классы МКТУ»); outbound writer: L75, L76, L74, legacy «патентные тролли». llms: `memory/blog/llms.txt` + `llms-full.txt` (83 статьи); `lireate-site/llms.txt` (78 L*) + append L77 в `llms-full`; копии `llms.txt` / `llms-full.txt` в каталоге. `--article-dir` в CLI не поддерживается.