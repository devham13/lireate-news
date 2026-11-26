# Promotion checklist — L81 kompensatsiya-za-narushenie-tovarnogo-znaka-raschet-i-dokazatelstva

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/kompensatsiya_za_narushenie_tovarnogo_znaka_raschet_i_dokazatelstva/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/narushayut_tovarnyy_znak_chto_delat_pravoobladatelyu/`, `/isk_o_narushenii_tovarnogo_znaka_trebovaniya_i_dokazatelstva/` (L80), `/kak_obosnovat_snizhenie_kompensatsii_za_narushenie_prav/`, `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (истцы по ТЗ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
В претензии завысили 10 млн? Суд ждёт один способ на эпизод по п. 4 ст. 1515.

• 10 000–10 000 000 ₽ с 04.01.2026
• таблица эпизодов → иск L80
• контраргументы ответчика — не этот гайд

Читать: {LIREATE_PUBLIC_SITE_URL}/kompensatsiya_za_narushenie_tovarnogo_znaka_raschet_i_dokazatelstva/
```

## Перелинковка

- [ ] **L80:** двусторонняя L81↔L80 (indexer 2026-11-26)
- [ ] **L85:** inbound из блока «ст. 1301 vs 1515» (L85 outbound готов)
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «компенсация за нарушение товарного знака» (ручная / Wordstat)

## Notes

Indexer (2026-11-26): interlinker — **0** авто; ручной L81→L80. llms копии в каталоге L81.