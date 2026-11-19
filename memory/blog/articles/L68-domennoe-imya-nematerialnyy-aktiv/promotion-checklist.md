# Promotion checklist — L68 domennoe-imya-nematerialnyy-aktiv

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/domennoe-imya-nematerialnyy-aktiv/` (подтвердить после INSERT на хостинге)  
Рубрика: Бренд (`category_id=13`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=13`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/domennoe_imya_nma_ili_net_uchet_i_zaschita_domena_po_fsbu_14_2022/` (L10, ×4); `/kak-opredelit-klass-mktu/` (interlinker L68→L06); `/proverit-brend-onlayn-unikalnost/` (×3); `/sajt-klon-zashchita-brenda-v-internete/` (×3); `/mozhno_li_pokazyivat_chuzhie_logotipyi_i_emblemyi_v_video_i_na_oblozhkax/`; `/findtz/`; `/registraciya_tovarnogo_znaka/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (бухгалтерия, ИТ, владельцы бренда) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Домен на 08, уступка или товарный знак? Три слоя без мифа «купил домен — бренд мой».

• ФСБУ 14/2022: обычно сайт на 08, продление 26/44; сделка — уступка администрирования
• Сверка SLD с реестром до претензии; МКТУ в одной таблице с доменом
• 9 шагов мониторинга: WHOIS, учётная политика, спор

Читать: {LIREATE_PUBLIC_SITE_URL}/domennoe-imya-nematerialnyy-aktiv/
```

## Перелинковка

- [ ] Outbound indexer **L68→L06** по «классы МКТУ» — в `article.html`
- [ ] Outbound writer: L10, L38, L24, L17, CTA `/findtz/`, `/registraciya_tovarnogo_znaka/` — без изменений indexer
- [ ] Рассмотреть inbound из L10/L38 на anchor_variants L68 («доменное имя как нематериальный актив», «сверить домен с реестром ТЗ»)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «доменное имя как нематериальный актив» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-19): CLI `--article-dir` не поддерживается — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** автоматическая вставка **L68→L06** (якорь «классы МКТУ»). Inbound на L68 — **0**. `memory/blog/interlink-suggestions.json` обновлён (73 статьи, 1 opportunity). llms: `memory/blog/llms.txt` + `llms-full.txt` (73 статьи, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **68** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L68 `/domennoe-imya-nematerialnyy-aktiv`); копия `memory/blog/llms.txt` в каталоге L68. Live publish: **не выполнялся** (выкладка — CRON REG.RU после merge).