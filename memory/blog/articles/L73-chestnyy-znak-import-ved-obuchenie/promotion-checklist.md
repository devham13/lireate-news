# Promotion checklist — L73 chestnyy-znak-import-ved-obuchenie

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/chestnyy_znak_import_ved_obuchenie/` (канон `lireate_seo_url`; подтвердить после INSERT на хостинге)  
Рубрика: Маркировка (`category_id=11`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=11`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/chek_list_markirovka_importa_chestnyiy_znak_i_tovarnyiy_znak_brenda/` (L22, ×4 + indexer); `/registraciya_tovarnogo_znaka/` (×2); markirovka.ru, docs.crpt.ru, consultant.ru
- [ ] Рассмотреть ручные inbound из L67/L36 на anchor_variants L73 и кластер «ВЭД до ФТС»
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (импорт, ВЭД, маркировка) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Брокер уже просит CMR и графу 31, а ВЭД путает КМ и ТЗ? Внутренний маршрут из 8 модулей — без курса на 72 часа.

• RACI: ВЭД сверяет CMR↔КМ, юрист — ДС/СС и ТЗ
• заказ КМ «Ввезен в РФ» только после ТН ВЭД
• пакет брокеру при статусе «Нанесён»

Читать: {LIREATE_PUBLIC_SITE_URL}/chestnyy_znak_import_ved_obuchenie/
```

## Перелинковка

- [ ] Outbound indexer **L73→L22** (якорь «честный знак импорт» → live SEO URL чек-листа L22) — в `article.html`
- [ ] Outbound writer: L67, L36 в тексте (кластер); чек-лист L22, CTA ТЗ — уже в `article.html`
- [ ] Inbound на L73 — **0** (interlinker)
- [ ] После merge — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «честный знак импорт ved обучение» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-20): в CLI нет `--article-dir` — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** автоматическая вставка **L73→L22** (якорь «честный знак импорт»); href приведён к live SEO URL L22 (`/chek_list_markirovka_importa_chestnyiy_znak_i_tovarnyiy_znak_brenda/`). Inbound на L73 — **0**. `memory/blog/interlink-suggestions.json` обновлён (84 статьи, 1 opportunity). llms: перегенерация `memory/blog/llms.txt` + `llms-full.txt` (84 статьи, `https://example.com/blog/{slug}/`); `lireate_llms_site_generate.py` → **79** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L73 `chestnyy_znak_import_ved_obuchenie`); в `memory/blog/lireate-site/llms-full.txt` добавлен полный блок L73; копия `memory/blog/llms.txt` в каталоге L73. Live publish **не** выполнялся (CRON REG.RU после merge).