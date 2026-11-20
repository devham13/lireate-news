# Promotion checklist — L72 dorabotka-logotipa-pod-trebovaniya-rospatenta

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/dorabotka_logotipa_pod_trebovaniya_rospatenta/` (канон `canonical_path` `/dorabotka-logotipa-pod-trebovaniya-rospatenta`; подтвердить после INSERT на хостинге)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/dorabotka-logotipa-pered-registraciey-tovarnogo-znaka/` (L39, ×4); `/graficheskiy_tovarnyy_znak_smeshchenie_do_podachi/` (L54); `/dogovor_na_razrabotku_logotipa_kak_poluchit_prava_ot_dizaynera/` (L11); `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta/` (L01, ×2); CTA `/reg-tz-main` (×2)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (заявители ТЗ, дизайнеры, маркетинг до подачи) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
В одной заявке — один макет в графе 540: TIFF ≥300 dpi, непрозрачный фон, 8×8 см, поля 591 и 571.

• п. 2 ст. 1492: нельзя склеивать цветной и ч/б в один файл
• Цветная подача → заполняете 591; ч/б → графу 591 не трогаете
• Чек-лист перед загрузкой в кабинет ФИПС

Читать: {LIREATE_PUBLIC_SITE_URL}/dorabotka_logotipa_pod_trebovaniya_rospatenta/
```

## Перелинковка

- [ ] Outbound writer: L39, L54, L11, L01, CTA `/reg-tz-main` — без изменений indexer
- [ ] Inbound indexer **L39→L72** по «доработка логотипа под требования Роспатента» — в `L39/article.html`
- [ ] Рассмотреть inbound из L66/L11/L48 на `anchor_variants` L72 после publish
- [ ] После merge — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «доработка логотипа под требования роспатента» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-20): в CLI нет `--article-dir` — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** автоматическая вставка **L39→L72** (якорь «доработка логотипа под требования Роспатента» → `/dorabotka-logotipa-pod-trebovaniya-rospatenta/`). Outbound/inbound в `L72/article.html` indexer **0**. `memory/blog/interlink-suggestions.json` обновлён (80 статей, 1 opportunity). llms: перегенерация `memory/blog/llms.txt` + `llms-full.txt` (80 статей, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` → **75** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L72 `dorabotka_logotipa_pod_trebovaniya_rospatenta`); в `memory/blog/lireate-site/llms-full.txt` добавлен полный блок L72; копия `memory/blog/llms.txt` в каталоге L72. Live publish **не** выполнялся (CRON REG.RU после merge).