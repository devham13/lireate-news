# Promotion checklist — L70 registraciya-tovarnogo-znaka-s-oplatoy-za-rezultat

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta/` (L01), `/ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu/` (L48), `/kak-opredelit-klass-mktu/` (L06, interlinker), `/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/` (CTA услуги)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (заявители ТЗ, предприниматели, сравнение бюро) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
«Оплата только за результат» в рекламе бюро? Сначала три кошелька: пошлины, гонорар, допработы.

• success fee ≠ гарантия Роспатента; 35 000 ₽ пошлин отдельно
• 15 пунктов договора до подписи
• красный флаг «100% регистрации»

Читать: {LIREATE_PUBLIC_SITE_URL}/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/
```

## Перелинковка

- [ ] Outbound indexer **L70→L06** по «классы МКТУ» в blockquote «три кошелька»
- [ ] Outbound writer: L01 (чек-лист), L48 (экспертиза), CTA `/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/` — без изменений indexer
- [ ] Рассмотреть inbound из L07/L08/L30 на anchor_variants L70 (success fee, договор регистрации ТЗ)
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «регистрация товарного знака с оплатой за результат» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-19): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **1** автоматическая вставка **в L70** (L70→L06 «классы МКТУ»; inbound на L70 — **0**). `memory/blog/interlink-suggestions.json` обновлён (78 статей, 1 opportunity → applied). llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (78 статей, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` → **73** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L70); в `memory/blog/lireate-site/llms-full.txt` добавлен полный блок L70 (`/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat`); копии `llms.txt` / `llms-full.txt` в каталоге L70. Live publish **не** выполнялся.