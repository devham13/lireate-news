# Promotion checklist — L23 zashchita-prav-na-bazu-dannyh

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/zashchita_prav_na_bazu_dannyh_kak_oformit_i_dokazat_narushenie` (заполнить после publish)  
Рубрика: Авторское право (`category_id=17`) — `{PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`, если выложен)
- [ ] Проверить internal links из статьи (200): `/news?num=2&category=17`; после live — `/rezhim-kommercheskoj-tajny-kak-vvesti` (L14), если ссылка в HTML заменена с плейсхолдера
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (владельцы каталогов, SaaS, маркетплейсы) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Конкурент выгрузил ваш каталог? Защита БД — это ст. 1334 и изготовитель, а не штрафы РКН за 152-ФЗ.

• Изготовитель в договорах, 10 000 элементов или существенные затраты
• Роспатент: 5 000 ₽, 62 рабочих дня — добровольно
• Претензия и ст. 1311: от 10 000 до 5 000 000 ₽

Читать: {PUBLIC_SITE_URL}/zashchita_prav_na_bazu_dannyh_kak_oformit_i_dokazat_narushenie
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 17), если нет авто
- [ ] Рассмотреть inbound из L05/L14 на «коммерческая тайна и база данных» / «защита каталога» (interlinker не сматчил `anchor_variants` L23)
- [ ] Outbound в L23: рубрика «Авторское право», плейсholder L14 (КТ) до live — уже в `article.html`
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «защита прав на базу данных» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-31): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (28 статей в индексе; `anchor_variants` L23 не матчатся в чужих HTML). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (28 статей, `/blog/{slug}/`); `memory/blog/lireate-site/` и копии в каталоге L23 — **23** L-статьи с `canonical_path` (добавлен L23). Live publish не выполнялся.
