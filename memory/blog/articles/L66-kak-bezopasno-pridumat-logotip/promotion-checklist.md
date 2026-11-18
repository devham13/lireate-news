# Promotion checklist — L66 kak-bezopasno-pridumat-logotip

Дата публикации: 2026-11-18  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/kak-bezopasno-pridumat-logotip/` (подтвердить после INSERT на хостинге)  
Рубрика: Логотип (`category_id=10`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=10`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L11 `/dogovor_na_razrabotku_logotipa_kak_poluchit_prava_ot_dizaynera/`; L39 `/dorabotka-logotipa-pered-registraciey-tovarnogo-znaka/`; L64 `/nejming_i_logotip_soglasovanie/`; CTA Telegram
- [ ] Inbound interlinker: **0** автоматических вставок на L66 (anchor_variants в чужих HTML — нет совпадений на этом прогоне)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (фаундеры, маркетинг до тиража) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Логотип на визитке ещё не ваш: © на рисунок, ® только после реестра, у букв — лицензия.

• Пять слоёв проверки до первого тиража
• Договор с дизайнером + папка доказательств
• Поиск сходства в Поисковой платформе ФИПС

Читать: {LIREATE_PUBLIC_SITE_URL}/kak-bezopasno-pridumat-logotip/
```

## Перелинковка

- [ ] Outbound writer L66→L11, L39, L64 — уже в `article.html` (GEO QA canonical paths)
- [ ] Рассмотреть ручной inbound из L11/L34/L55 на anchor «безопасно придумать логотип» / «чек-лист до тиража» (interlinker inbound — **0**)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как безопасно придумать логотип» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-18): CLI `--article-dir` не поддерживается — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **2** автоматические вставки, **0** с участием L66 (L64→L06, L54→L06 по «классы МКТУ»). Outbound writer: L11, L39, L64, consultant.ru, Telegram — без изменений indexer. `memory/blog/interlink-suggestions.json` обновлён (71 статей, 2 opportunities). llms: `memory/blog/llms.txt` + `llms-full.txt` (71 статей, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **66** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L66 `/kak-bezopasno-pridumat-logotip`); копия `llms.txt` в каталоге L66. Live publish: **не выполнялся** (выкладка — CRON REG.RU после merge).