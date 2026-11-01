# Promotion checklist — L26 promyshlennyy-obrazec-ili-tovarnyy-znak-dizayn-tovara

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/promyshlennyy-obrazec-ili-tovarnyy-znak-dizayn-tovara` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/blog/kak-opredelit-klass-mktu/` (interlink L26→L06); `/patent`; `/reg-tz-main` (≤3); `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`; `/registraciya-brenda-odezhdy-mktu`; `/kak_zaregistrirovat_brend_na_ozon_i_wildberries_proverka_imeni_i_nuzhen_li_tz`; рубрика `/news?num=2&category=9`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (селлеры MP, FMCG, D2C с уникальной упаковкой) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Копируют силуэт, а не логотип? Промышленный образец охраняет внешний вид по ст. 1352; объёмный ТЗ — форму как источник, но нужна различительность и обход п. 4 ст. 1483.

• Минимум пошлин на ПО ~15 000 ₽ (2k+3k+10k) по ГУ Роспатента
• Патент ПО до 25 лет; свидетельство ТЗ — 10 лет
• Публикация на WB до заявки бьёт по новизне — 12 месяцев льготы

Читать: {PUBLIC_SITE_URL}/promyshlennyy-obrazec-ili-tovarnyy-znak-dizayn-tovara
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Inbound: L25 → L26 (ручная вставка в блок «ТЗ vs промышленный образец») — выполнено indexer
- [ ] Outbound в L26: writer L01/L03/L25 + `/patent` + `/reg-tz-main`; interlink L26→L06 «классы МКТУ»
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «защита дизайна товара» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-01): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** автоматическая вставка (L26 → L06 по «классы МКТУ»); **1** ручная inbound (L25 → L26 в `article.html`). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (31 статья, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L26 — **26** L-статей с `canonical_path` (добавлен L26). Live publish не выполнялся.
