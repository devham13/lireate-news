# Promotion checklist — L01 proverka-tovarnogo-znaka-pered-podachey-v-rospatent

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/proverka-tovarnogo-znaka-pered-podachey-v-rospatent` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (theme или plugin)
- [ ] Проверить internal links из статьи (200): `/7_prichin_zaregestrirovat_tovarnyiy_znak`, `/kak_zaschitit_tovarnyiy_znak_i_reputaciyu_biznesa_v_seti`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, малый бизнес, бренд) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Не платите пошлину вслепую: проверьте товарный знак по открытым реестрам Роспатента и ФИПС до подачи заявки.

• Поисковая платформа + реестр заявок, TMview, МКТУ
• Таблица рисков: сходство, однородность, ст. 1483 ГК РФ
• Когда хватит DIY и когда нужен патентный поверенный

Читать: {PUBLIC_SITE_URL}/proverka-tovarnogo-znaka-pered-podachey-v-rospatent
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Обновить 1–2 старых поста на lireate → link to new (при наличии релевантных материалов)
- [ ] После появления других L-статей — перезапустить `excalibur_blog_interlinker.py --apply --site-base $PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «проверка товарного знака перед регистрацией» (ручная проверка / Wordstat)

## Notes

Indexer (2026-10-16): interlinker `--apply` по всему `memory/blog/articles` — **0** автоматических вставок (единственная L-статья в репо; anchor_variants L01 не матчятся в B01–B05; outbound в `article.html` уже вручную). llms: `memory/blog/lireate-site/llms.txt` (1 статья, относительные пути), mayai-индекс `memory/blog/llms.txt` — 5 статей B01–B05 без изменения состава.
