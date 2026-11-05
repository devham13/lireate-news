# Promotion checklist — L34 kak-zapatentovat-nazvanie-i-logotip

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/kak-zapatentovat-nazvanie-i-logotip` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (L01); `/rospatent-fips-proverit-tovarnyy-znak-onlayn-besplatno` (L29); `/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026` (L30); `/mktu` (L06); `/blog/kak-opredelit-klass-mktu/` (L06 alt); `/reg-tz-main`; рубрика `/news?num=2&category=9`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, SMB, «запатентовать» в поиске → ТЗ) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
«Патент» на бренд? Нет: патент — ст. 1350, не слово на витрине. © держит рисунок логотипа, не монополию на название. Монополия — товарный знак в МКТУ после регистрации.

• Поиск в реестрах бесплатен (L29)
• Пошлины 2.1+2.4+2.11 — минимум 35 000 ₽ / класс
• DIY-маршрут после проверки — L30

Читать: {PUBLIC_SITE_URL}/kak-zapatentovat-nazvanie-i-logotip
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Inbound на L34: L01 (FAQ сроки), L11 (© vs ТЗ + «запатентовать»), L25 (выбор объекта охраны), L30 (один знак / две заявки); outbound в L34: L01, L29, L30, L06, `/reg-tz-main`
- [ ] Interlinker auto: L34→L06 «классы МКТУ» (`/blog/kak-opredelit-klass-mktu/`)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как запатентовать логотип и название» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-05): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** автоматическая вставка (L34→L06 «классы МКТУ»). Inbound на L34 — **4** ручные вставки (L01, L11, L25, L30). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/lireate-site/` + копии в каталоге L34; добавлена строка L34 в индекс (**34** L-статей с `canonical_path` в lireate-site). `memory/blog/llms.txt` перегенерирован скриптом. Live publish не выполнялся.
