# Promotion checklist — L16 kak-legalno-opublikovat-perevod-knigi

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/kak-legalno-opublikovat-perevod-knigi` (заполнить после publish)  
Рубрика: Авторское право (`category_id=17`) — `{PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec`, `/news?num=2&category=17`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (переводчики, издатели, блогеры, fan-сообщества) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Любительский перевод книги — не «свободный контент»: три слоя прав (оригинал, лицензия, текст переводчика), письменная лицензия и отдельно личное чтение по ст. 1273.

• 70 лет и общественное достояние — не чужой готовый перевод с сайта
• Молчание автора ≠ согласие; публикация в сети — ст. 1270 даже без монетизации
• Чек-лист, шаблон письма правообладателю, FAQ про Роспатент vs AP

Читать: {PUBLIC_SITE_URL}/kak-legalno-opublikovat-perevod-knigi
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 17), если нет авто
- [ ] Outbound в L16: L02-гайд претензии, art.etopravo (обложка) — уже в `article.html`; рассмотреть ручной inbound из L11/L13 на «перевод» / «репродукция»
- [ ] Inbound по `anchor_variants` L16: 0 автоматических вставок (21 статья в индексе interlinker)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «можно ли делать любительский перевод» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-23): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (21 статья; `anchor_variants` L16 не матчатся в чужих HTML; outbound на L02-гайд претензии уже в `article.html`). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (21 статья, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L16 — **16** L-статей с `canonical_path` (добавлен L16). Live publish не выполнялся.
