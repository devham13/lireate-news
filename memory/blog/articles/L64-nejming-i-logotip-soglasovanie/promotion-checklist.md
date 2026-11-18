# Promotion checklist — L64 nejming-i-logotip-soglasovanie

Дата публикации: 2026-11-18  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/nejming_i_logotip_soglasovanie/` (подтвердить после INSERT на хостинге)  
Рубрика: Бренд (`category_id=13`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=13`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): L06 (writer + interlinker `/blog/kak-opredelit-klass-mktu/`); L11, L38, L48, L39, L01; CTA `/reg-tz-main`
- [ ] Inbound interlinker: L37, L20 → L64 (`/blog/nejming-i-logotip-soglasovanie/` — при live привести к `nejming_i_logotip_soglasovanie`)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (основатели, маркетинг до дизайна) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Сначала имя в реестрах и МКТУ — потом логотип. Иначе перерисовываете макет под отказ.

• Одна заявка = один знак (ст. 1492): комбо vs две заявки
• Бриф дизайнеру только после отсева имён
• Чек-лист перед пошлинами

Читать: {LIREATE_PUBLIC_SITE_URL}/nejming_i_logotip_soglasovanie/
```

## Перелинковка

- [ ] Outbound L64→L06: interlinker на «классы МКТУ» в TL;DR (live href — при необходимости `/struktura_mktu_...` или единый slug)
- [ ] Inbound L37, L20: «комбинированное обозначение» → L64
- [ ] Рассмотреть inbound из L11/L39/L38 на anchor «нейминг» / «согласование логотипа» (interlinker inbound сверх L37/L20 — **0**)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «нейминг и логотип» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-18): `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` (`--article-dir` в CLI не поддерживается) — **3** автоматические вставки, все с участием L64: **outbound** L64→L06 по «классы МКТУ»; **inbound** L37→L64 и L20→L64 по secondary «комбинированное обозначение» (`anchor_variants` L64 в чужих HTML — **0** доп.). Outbound writer: L06, L11, L38, L48, L39, L01, `/reg-tz-main` — уже в `article.html`. `memory/blog/interlink-suggestions.json` обновлён (69 статей, 3 opportunities). llms: `memory/blog/llms.txt` + `llms-full.txt` (69 статей, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **64** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L64 `/nejming_i_logotip_soglasovanie`); копия `llms.txt` в каталоге L64 (полный `llms-full.txt` — только в `memory/blog/`).

Live publish: **не выполнялся** (`publish:no`; выкладка — CRON REG.RU после merge).