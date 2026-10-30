# Promotion checklist — L21 osparivanie-tovarnogo-znaka-v-rospatente

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/osparivanie-tovarnogo-znaka-v-rospatente` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`, `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti`, `/news?num=2&category=9`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, правообладатели, заявители ТЗ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Путаете ст. 1493, 1500 и 1513? В Роспатенте три разных входа: обращение на экспертизе, возражение заявителя (4 мес., 9 000 ₽) и спор против чужой охраны (14 000 ₽).

• Таблица процедур, каналы подачи в ФИПС и 7 шагов до коллегии ППС
• Отличие от возражения по своему отказу и от детального гайда по атаке чужой регистрации (L08)
• Суд по ст. 1248 — после решения ППС, не вместо пропущенного срока

Читать: {PUBLIC_SITE_URL}/osparivanie-tovarnogo-znaka-v-rospatente
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Рассмотреть ручной inbound из L07/L08 на «оспаривание в роспатенте» / «ст. 1500» (interlinker не сматчил `anchor_variants` L21)
- [ ] Outbound в L21: legacy чек-лист L01, CTA защиты знака, рубрика ТЗ — уже в `article.html`
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «оспаривание товарного знака в роспатенте» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-30): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **5** автоматических вставок в L17/L18/L19 (→ L06, L03, L11); **0** inbound/outbound по ключам L21 (26 статей в индексе; `anchor_variants` L21 не матчатся в чужих HTML). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (26 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L21 — **21** L-статья с `canonical_path` (полная пересборка, добавлены L17–L21). Live publish не выполнялся.
