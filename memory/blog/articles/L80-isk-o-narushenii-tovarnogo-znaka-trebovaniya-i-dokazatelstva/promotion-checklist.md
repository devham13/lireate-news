# Promotion checklist — L80 isk-o-narushenii-tovarnogo-znaka-trebovaniya-i-dokazatelstva

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/isk_o_narushenii_tovarnogo_znaka_trebovaniya_i_dokazatelstva/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/narushayut_tovarnyy_znak_chto_delat_pravoobladatelyu/` (L78), `/kompensatsiya_za_narushenie_tovarnogo_znaka_raschet_i_dokazatelstva/` (L81), `/pretenziya_za_ispolzovanie_tovarnogo_znaka_kak_otvetit/`, `/kak_zashchitit_intellektualnye_prava_v_sude/`, `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (правообладатели ТЗ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Претензия отработала 30 дней? Иск по ТЗ — в арбитраж субъекта, не в СИП.

• ответчик, п. 57 ППВС: конкретные URL
• один способ п. 4 ст. 1515 → расчёт L81
• приложения по ст. 125 АПК

Читать: {LIREATE_PUBLIC_SITE_URL}/isk_o_narushenii_tovarnogo_znaka_trebovaniya_i_dokazatelstva/
```

## Перелинковка

- [ ] **L81:** inbound на L80 из расчёта компенсации (indexer 2026-11-26)
- [ ] **L78:** двусторонняя связка «до суда / иск»
- [ ] **L83-L85:** после live L83/L84 — краткий inbound из кластера IP-споров
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «иск о нарушении прав на товарный знак» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-26): interlinker full blog — **0** авто; ручной L80→L81. llms: `memory/blog/llms.txt` (88 статей), `lireate-site/llms.txt` (83 entries); копии в каталоге L80. publish/published-articles.md не трогали.