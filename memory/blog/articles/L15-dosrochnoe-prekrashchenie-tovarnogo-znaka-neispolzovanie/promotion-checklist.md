# Promotion checklist — L15 dosrochnoe-prekrashchenie-tovarnogo-znaka-neispolzovanie

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/dosrochnoe-prekrashchenie-tovarnogo-znaka-neispolzovanie` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/blog/kak-opredelit-klass-mktu/`, `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec`, `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta`, `/news?num=2&category=9`, `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (владельцы брендов, e-commerce, юристы МСБ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Чужой ТЗ в реестре без товара? Сначала письмо по ст. 1486, два месяца ожидания, иск в СИП за 30 дней — не ППС.

• ППС ≠ неиспользование: спор о регистрации vs три года без оборота
• Три года считают до даты предложения; использование доказывает правообладатель
• Заинтересованность — не только заявка в Роспатент (практика СИП-60/2025)

Читать: {PUBLIC_SITE_URL}/dosrochnoe-prekrashchenie-tovarnogo-znaka-neispolzovanie
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Outbound в L15: L06 (классы МКТУ) — indexer `--apply`; L01, L02, рубрика 9, `/reg-tz-main` — уже в `article.html`
- [ ] Inbound по `anchor_variants` L15: 0 автоматических вставок в чужие статьи (20 статей в индексе)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как подать иск о неиспользовании товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-22): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** вставка (L15 → L06 «классы МКТУ»). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (20 статей); `memory/blog/lireate-site/` и копии в каталоге L15 — **15** L-статей с `canonical_path` (добавлен L15). Live publish не выполнялся.
