# Promotion checklist — L54 graficheskiy-tovarnyy-znak-smeshchenie

Дата публикации: 2026-11-12  
Live URL: `{PUBLIC_SITE_URL}/graficheskiy_tovarnyy_znak_smeshchenie_do_podachi` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L01, L39, L38, L07; CTA Telegram/WhatsApp/MAX; interlink L54→L06
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
Похожий логотип уже в реестре в ваших классах МКТУ? До пошлин — поиск по JPG на платформе Роспатента и матрица п. 43.

• пять признаков сходства изобразительных знаков
• однородность п. 45 и что менять в Figma
• согласие, сужение МКТУ или новая заявка по ст. 1497

Читать: {PUBLIC_SITE_URL}/graficheskiy_tovarnyy_znak_smeshchenie_do_podachi
```

## Перелинковка

- [ ] Добавить ссылку в ленту /news (рубрика 9), если нет авто
- [ ] Inbound L39→L54 добавлен interlinker (якорь «доработка логотипа перед регистрацией»)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base` (публичный URL из env деплоя)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как снизить риск смешения графического товарного знака» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-12): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base https://example.com` (--article-dir в CLI не поддерживается) — **2** автоматические вставки: **L54→L06** («классы МКТУ»); **L39→L54** («Доработка логотипа перед регистрацией»). Inbound на L54 — **1**. `memory/blog/interlink-suggestions.json` обновлён (59 статей, 2 opportunity). llms: полная перегенерация `memory/blog/llms.txt` + `llms-full.txt` (59 статей, `https://example.com/blog/{slug}/`); `memory/blog/lireate-site/` — строка L54 в `llms.txt` + блок в `llms-full.txt`; копии в каталоге L54. Live publish не выполнялся.
