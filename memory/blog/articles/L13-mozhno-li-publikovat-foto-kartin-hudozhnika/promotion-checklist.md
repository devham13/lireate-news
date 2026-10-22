# Promotion checklist — L13 mozhno-li-publikovat-foto-kartin-hudozhnika

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/mozhno-li-publikovat-foto-kartin-hudozhnika` (заполнить после publish)  
Рубрика: Авторское право (`category_id=17`) — `{PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec`, `/news?num=2&category=17`, `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (блогеры, SMM, кураторы выставок, арт-галереи) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
В посте с картиной два слоя прав: живопись и фотофайл. Скачивание из интернета ≠ законное использование (обзор ВС РФ, п. 7).

• 70 лет после смерти автора — общественное достояние, но файл музея всё равно по copyright
• Ст. 1274 и 1276: цель поста, объём, своя съёмка vs JPG с сайта
• Чек-лист, таблицы и шаблон подписи перед публикацией

Читать: {PUBLIC_SITE_URL}/mozhno-li-publikovat-foto-kartin-hudozhnika
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 17), если нет авто
- [ ] После publish — рассмотреть inbound из L11 (договор с дизайнером) и L09 (бренд на полотне) на anchor «фото картины» / «репродукция в соцсетях» (ручная вставка: interlinker не сматчил фразы)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как проверить можно ли публиковать фотографию картины авторское право» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-22): interlinker `--apply --blog-dir memory/blog/articles` — **0** автоматических вставок (18 статей; `anchor_variants` L13 не матчатся в чужих HTML; outbound на L02-гайд претензии, рубрика AP, `/reg-tz-main` уже в `article.html`). llms: `memory/blog/llms.txt` + `llms-full.txt` (18 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **13** L-статей с `canonical_path` (добавлен L13); копии `llms.txt` / `llms-full.txt` в каталоге L13.
