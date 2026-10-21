# Promotion checklist — L12 madridskaya-sistema-poshliny-i-podacha-iz-rossii

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/madridskaya-sistema-poshliny-i-podacha-iz-rossii` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (×2), `/blog/kak-opredelit-klass-mktu/`, `/registraciya_tovarnogo_znaka_v_kitae`, `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (экспорт, e-com, бренд-менеджеры) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Мадрид из РФ — не одна касса: 5 000 ₽ + классы по п. 4.14 и 653/903 CHF в ВОИС, плюс 100 CHF или individual по каждой стране.

• Базовый знак в Роспатенте, форма ММ2, перечень МКТУ не шире базы
• Китай с 12.04.2026 — individual fees; пример расчёта в статье
• 12/18 мес. предварительного отказа и риск центральной атаки по базе

Читать: {PUBLIC_SITE_URL}/madridskaya-sistema-poshliny-i-podacha-iz-rossii
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] После publish — рассмотреть inbound из L01 на anchor «мадридские знаки» / «международная регистрация» (ручная вставка: interlinker не сматчил фразы)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «мадридская система пошлины подача из России» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-21): interlinker `--apply --blog-dir memory/blog/articles` — **0** автоматических вставок (17 статей; anchor_variants L12 не матчатся в чужих HTML; ручная вставка L12 → L06 по «классов МКТУ»; outbound на legacy чек-лист L01 (×2), Китай, `/reg-tz-main` уже в `article.html`). llms: repo memory/blog (17 статей); site bundle 12 L-статей с canonical_path (добавлен L12); копии в каталоге L12.
