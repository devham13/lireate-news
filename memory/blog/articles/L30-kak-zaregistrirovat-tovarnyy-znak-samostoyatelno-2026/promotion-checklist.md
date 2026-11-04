# Promotion checklist — L30 kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/rospatent-fips-proverit-tovarnyy-znak-onlayn-besplatno` (L29); `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta` (L01); `/kak-opredelit-klass-mktu` (L06); `/otkaz-v-registracii-tovarnogo-znaka-otnositelnye-osnovaniya` (L07); `/chto-delat-esli-tovarnyy-znak-zanyat` (L19); `/registraciya-brenda-odezhdy-mktu` (L25); `/reg-tz-main`; рубрика `/news?num=2&category=9`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, малый бизнес, in-house юристы, DIY до поверенного) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
ТЗ без бюро в 2026: проверка L01/L29 → МКТУ-13 → online.rospatent или Госуслуги с УКЭП → 2.1+2.4 от 35 000 ₽ за класс → экспертиза → 2.11. Срок услуги ~18 мес. + 2 нед., без гарантии регистрации.

• УКЭП обязательна для электронной заявки
• 2.11 платят после положительного решения (18 000 ₽ / класс)
• При уведомлении — ответ за 6 мес. (L07)

Читать: {PUBLIC_SITE_URL}/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Inbound на L30: рассмотреть из L01/L29 на «как зарегистрировать товарный знак самостоятельно» / DIY-маршрут (ручная вставка: `anchor_variants` L30 не сматчились в чужих HTML на этой ветке)
- [ ] Outbound в L30: writer — L01, L29, L06, L07, L19, L25, L03, `/reg-tz-main`; interlinker в L30 — **0** (hub-вставки в других статьях: L29→L06 «классы МКТУ»; повтор L21→L28 по ст. 1493)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как зарегистрировать товарный знак» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-04): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **3** автоматические вставки (L29→L06; L21→L28 ×2; четвёртая возможность «куда подается…» в L21 не применена — overlap в том же абзаце). Inbound на L30 — **0**. `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (35 статей, `/blog/{slug}/`, site-base Lireate); `memory/blog/lireate-site/` и копии в каталоге L30 — **30** L-статей с `canonical_path` (добавлены L29, L30). Live publish не выполнялся.
