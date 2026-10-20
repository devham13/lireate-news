# Promotion checklist — L08 vozrazhenie-protiv-registracii-tovarnogo-znaka-sroki-poryadok

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/vozrazhenie-protiv-registracii-tovarnogo-znaka-sroki-poryadok` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (×2), `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, правообладатели, селлеры) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Чужой товарный знак в реестре? До регистрации — обращение по ст. 1493; после — возражение в ППС по ст. 1512, 14 000 ₽ и срок 5 лет.

• Таблица: обращение vs возражение vs ответ по своей заявке (ст. 1500)
• 8 шагов: статус в реестре, доказательства, пошлина, заседание коллегии
• Отличие от возражения заявителя на отказ (9 000 ₽) — не путать процедуры

Читать: {PUBLIC_SITE_URL}/vozrazhenie-protiv-registracii-tovarnogo-znaka-sroki-poryadok
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — рассмотреть inbound из L07 на anchor «ст. 1512» / «оспаривание чужого знака» (ручная вставка: interlinker не сматчил фразы)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как подать возражение против регистрации товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-20): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (13 статей; anchor_variants L08 не матчатся в чужих HTML без slug; outbound на legacy чек-лист L01 и CTA защиты знака уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (13 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **8** L-статей с `canonical_path` (добавлен L08); копии `llms.txt` / `llms-full.txt` в каталогах L01–L08.
