# Promotion checklist — L62 izmenenie-tovarnogo-znaka-novaya-registraciya

Дата публикации: 2026-11-17  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/izmenenie-tovarnogo-znaka-novaya-registraciya/` (подтвердить после INSERT на хостинге)  
Рубрика: Товарный знак (`category_id=9`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L39 (`/dorabotka-logotipa-pered-registraciey-tovarnogo-znaka/`); L47 (`/prodlenie_tovarnogo_znaka_gosposhlina/`); L02 (`/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/`); L06 (`/blog/kak-opredelit-klass-mktu/` — interlinker); L30; CTA `/registraciya_tovarnogo_znaka/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, селлеры, франшиза) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Существенная правка знака — новая заявка; адрес и сокращение перечня — п. 2.16 (3 000 ₽) по ст. 1505.

• Три стадии: заявка (1497), реестр (1505), рынок (1486)
• Per se по п. 69 Правил № 482 и обзору СИП СП-22/15
• Расширение МКТУ — только новая заявка, не 2.16

Читать: {LIREATE_PUBLIC_SITE_URL}/izmenenie-tovarnogo-znaka-novaya-registraciya/
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 9), если нет авто
- [ ] Outbound L62→L06: interlinker на «классы МКТУ» в таблице стадий; при publish привести href к live slug при необходимости
- [ ] Рассмотреть inbound из L39/L47 на anchor «изменение ТЗ» / «п. 2.16» (interlinker inbound на L62 — **0**)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как понять когда изменение товарного знака требует новой регистрации» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-17): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **1** автоматическая вставка (L62→L06 по «классы МКТУ»; inbound на L62 — **0**, `anchor_variants` L62 не сматчились в чужих HTML). Outbound writer: L39, L47, L02, L30, `/registraciya_tovarnogo_znaka/`, legacy URL — уже в `article.html`. `memory/blog/interlink-suggestions.json` обновлён (67 статей, 1 opportunity). llms: `memory/blog/llms.txt` + `llms-full.txt` (67 статей, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **62** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L62 `/izmenenie-tovarnogo-znaka-novaya-registraciya`); копия `llms.txt` в каталоге L62 (полный `llms-full.txt` — только в `memory/blog/`).

Hosting publish prep (2026-11-17): `link-verify.json` → **pass** (15 ссылок; `privacy_policy_violations: []`). `lireate_hosting_publish.py --dry-run --article-dir …` → **DRY_RUN** (`seo_url`: `izmenenie-tovarnogo-znaka-novaya-registraciya`, `category`: **9**, 6 image files). Артефакты: `lireate-publish-result.json`, `publish-bundle/`. **БД INSERT не выполнялся**; `shared/published-articles-lireate.md` не трогали. Live после merge → CRON / ручной `lireate_hosting_publish.py` на REG.RU (`LIREATE_ALLOW_PUBLISH=yes`).