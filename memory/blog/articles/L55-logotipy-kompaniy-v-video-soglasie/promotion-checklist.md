# Promotion checklist — L55 logotipy-kompaniy-v-video-soglasie

Дата публикации: 2026-11-13  
Live URL: `{PUBLIC_SITE_URL}/mozhno_li_ispolzovat_logotipyi_kompaniy_v_video_chek_list_riskov` (заполнить после publish)  
Рубрика: Авторское право (`category_id=17`) — `{PUBLIC_SITE_URL}/news?num=2&category=17`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ (7 пар)
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L09, L02, L17, L27, L01; CTA Telegram/WhatsApp/MAX; interlink L55→L06, L55→L17
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
Коллаж «нам доверяют» с чужими логотипами? Три контура до рендера: ТЗ, графика файла и добросовестность — дисклеймер согласие не заменяет.

• матрица форматов ролика и красная зона промо
• согласие по ст. 1489 и компенсация 1515 с 04.01.2026
• куда идти при претензии (L02) и отстройка от превью L17

Читать: {PUBLIC_SITE_URL}/mozhno_li_ispolzovat_logotipyi_kompaniy_v_video_chek_list_riskov
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 17), если нет авто
- [ ] Рассмотреть inbound из L17/L09 на anchor «чужой логотип в видео» (interlinker дал 2 outbound в L55)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «можно ли использовать логотипы компаний в видео — чек-лист рисков» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-13): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (--article-dir в CLI не поддерживается) — **2** автоматические вставки **в L55** (якорь «Чужой логотип в видео» → L17; «классы МКТУ» → L06). Inbound на L55 — **0**. `memory/blog/interlink-suggestions.json` обновлён (60 статей, 2 opportunity). llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (60 статей, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — **55** L-статей с `canonical_path` (добавлен L55 `/logotipy-kompaniy-v-video-soglasie`); копии `llms.txt` / `llms-full.txt` в каталоге L55. Live publish не выполнялся.
