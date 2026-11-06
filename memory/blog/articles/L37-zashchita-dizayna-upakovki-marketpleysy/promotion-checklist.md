# Promotion checklist — L37 zashchita-dizayna-upakovki-marketpleysy

Дата публикации: 2026-11-06  
Live URL: `{PUBLIC_SITE_URL}/zashchita-dizayna-upakovki-marketpleysy` (заполнить после publish)  
Рубрика: Авторское право (`category_id=12`) — `{PUBLIC_SITE_URL}/news?num=2&category=12`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/promyshlennyy-obrazec-ili-tovarnyy-znak-dizayn-tovara`; `/mktu` (×2); `/avtorskoe-voznagrazhdenie-po-gk-rf`; `/kak_proverit_brend_na_wildberries_svoboden_li_tovarnyy_znak` (×2); `/news?num=2&category=12` (×2). После публикации L06 на проде — при желании вернуть прямую ссылку на гайд по классам (см. Notes).
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Клон упаковки на WB? Три слоя: © макета, патент на ПО для формы, ТЗ для бренда — и отдельно логистика по инструкции площадки.

• ст. 1352/1363 ГК РФ — ПО; ст. 1259 — произведение на этикетке
• реестры ФИПС → заявка → жалоба по правилам WB
• договор с дизайнером до спора «кто автор»

Читать: {PUBLIC_SITE_URL}/zashchita-dizayna-upakovki-marketpleysy
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 12), если нет авто
- [ ] Outbound в L37: Consultant, eg-online, seller.wildberries.ru, selsup.ru, klerk.ru — проверить 200 после деплоя
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (подставить базовый URL публичного сайта из настроек деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «запатентовать дизайн упаковки» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-06): в репозитории `excalibur_blog_interlinker.py` **не** принимает `--article-dir`; выполнено `--apply --blog-dir memory/blog/articles --site-base https://example.com` — **2** автоматические вставки **в L37** (таблица: якорь на L06; блок про договор: L35). Для проверки ссылок: `excalibur_blog_link_verify.py --site-base` с публичным URL продакшена; из-за **404** на каноническом пути гайда L06 до публикации материала прямая ссылка на L06 в таблице **снята**, остались текст «Классы МКТУ» и `/mktu`. Ссылка на L35: `/avtorskoe-voznagrazhdenie-po-gk-rf`. `memory/blog/interlink-suggestions.json` обновлён (остаётся 1 потенциальная вставка L37→L06). llms: в `memory/blog/llms.txt` добавлена строка L37, в `memory/blog/llms-full.txt` вставлен полный блок L37 (остальной индекс как в `HEAD`, без полной перегенерации; URL вида `https://example.com/blog/{slug}/`); для Lireate — строка и полный блок L37 в `memory/blog/lireate-site/llms.txt` и `llms-full.txt` с `canonical_path` `/zashchita-dizayna-upakovki-marketpleysy`; копии в каталоге статьи = `lireate-site`. Live publish не выполнялся.
