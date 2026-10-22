# Promotion checklist — L14 rezhim-kommercheskoj-tajny-kak-vvesti

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/rezhim-kommercheskoj-tajny-kak-vvesti` (заполнить после publish)  
Рубрика: Бизнес (`category_id=15`) — `{PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/sposoby-zashchity-izobreteniya`, `/dogovor-na-razrabotku-logotipa-prava-ot-dizajnera`, `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec`, `/news?num=2&category=15`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (собственники, HR, операционные директора) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
NDA без пяти мер ст. 10 98-ФЗ в споре часто не спасает: суд смотрит перечень, гриф, журнал доступа и цепочку утечки.

• Пять мер ч. 1 ст. 10 и дата «режим закрыт»
• Передача подрядчику по договору ≠ разглашение постороннему
• Комиссия по ст. 193 ТК и пакет для иска

Читать: {PUBLIC_SITE_URL}/rezhim-kommercheskoj-tajny-kak-vvesti
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 15), если нет авто
- [ ] Inbound: L05 → L14 (режим КТ) — сделано indexer
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как доказать разглашение коммерческой тайны» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-22): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (19 статей; `anchor_variants` L14 не матчатся в чужих HTML). Ручные outbound в L14: L05 (патент/ноу-хау/КТ), L11 (договор с исполнителем); inbound L05 → L14; outbound на L02-гайд претензии и рубрика «Бизнес» уже в `article.html`. llms: `memory/blog/llms.txt` + `llms-full.txt` (19 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` — **14** L-статей с `canonical_path` (добавлен L14); копии `llms.txt` / `llms-full.txt` в каталоге L14.
