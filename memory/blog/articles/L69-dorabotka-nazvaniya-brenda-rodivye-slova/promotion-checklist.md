# Promotion checklist — L69 dorabotka-nazvaniya-brenda-rodivye-slova

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/dorabotka_nazvaniya_brenda_s_rodovyim_slovom_kak_proyti_ekspertizu_tovarnogo_znaka/` (канон репо: `/dorabotka-nazvaniya-brenda-rodivye-slova`; подтвердить после INSERT на хостинге)  
Рубрика: Бренд (`category_id=13`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=13`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/nejming_i_logotip_soglasovanie/` (L64, ×2); `/ekspertiza-tovarnyh-znakov-formalnaya-po-suschestvu/` (L48, ×3); `/struktura_mktu_kak_opredelit_klass_dlya_tovara_i_uslugi/` (×4); `/kak-opredelit-klass-mktu/` (interlinker L69→L06); `/rospatent-fips-proverit-tovarnyy-znak-onlayn-besplatno/`; CTA `/reg-tz-main`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (нейминг, заявители ТЗ, маркетинг) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Имя с родовым ядром («трава») и отказ по п. 1? Косметическая правка не снимает описательность.

• п. 1 ст. 1483: меняйте доминирующее слово, не только шрифт и регистр
• п. 6: после переименования снова поиск в Поисковой платформе ФИПС
• Учебный сценарий «Трава» + чек-лист перед повторной заявкой (без гарантий регистрации)

Читать: {LIREATE_PUBLIC_SITE_URL}/dorabotka_nazvaniya_brenda_s_rodovyim_slovom_kak_proyti_ekspertizu_tovarnogo_znaka/
```

## Перелинковка

- [ ] Outbound indexer **L69→L06** по «классы МКТУ» — в `article.html`
- [ ] Outbound writer: L64, L48, legacy МКТУ URL, L01-чек-лист, CTA `/reg-tz-main` — без изменений indexer
- [ ] Рассмотреть inbound из L39/L07/L62 на anchor_variants L69 («доработка названия бренда с родовым словом», «описательное обозначение ст 1483»)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «доработка названия бренда» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-19): CLI `--article-dir` не поддерживается — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **1** автоматическая вставка **L69→L06** (якорь «классы МКТУ»). Inbound на L69 — **0**. `memory/blog/interlink-suggestions.json` обновлён (74 статьи, 1 opportunity). llms: `memory/blog/llms.txt` + `llms-full.txt` (74 статьи, `$LIREATE_PUBLIC_SITE_URL/blog/{slug}/`); `lireate_llms_site_generate.py` → **69** L-записей в `memory/blog/lireate-site/llms.txt` (добавлен L69 `dorabotka_nazvaniya_brenda_s_rodovyim_slovom_kak_proyti_ekspertizu_tovarnogo_znaka`); копия `memory/blog/llms.txt` в каталоге L69. Live publish: **не выполнялся** (`publish:no`; выкладка — CRON REG.RU после merge).