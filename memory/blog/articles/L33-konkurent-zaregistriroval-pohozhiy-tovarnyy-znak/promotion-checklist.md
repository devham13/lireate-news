# Promotion checklist — L33 konkurent-zaregistriroval-pohozhiy-tovarnyy-znak

Дата публикации: YYYY-MM-DD  
Live URL: `{PUBLIC_SITE_URL}/konkurent-zaregistriroval-pohozhiy-tovarnyy-znak` (заполнить после publish)  
Рубрика: Товарный знак (`category_id=9`) — `{PUBLIC_SITE_URL}/news?num=2&category=9`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/vozrazhenie_protiv_registracii_chuzhogo_tovarnogo_znaka_sroki_i_poryadok`; `/osparivanie_tovarnogo_znaka_v_rospatente_kak_podat_vozrazhenie`; `/chto_delat_esli_tovarnyy_znak_zanyat`; `/news?num=2&category=9`; `/politika_konfidencialnosti`; `/private_data`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в каталоге статьи и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (владельцы бренда, in-house IP, e-com) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Конкурент уже в реестре с похожим знаком? Это не сценарий «знак занят до подачи»: ППС по ст. 1512 (14 000 ₽), 5 лет с бюллетеня, претензия и 30 дней до иска по ст. 1515.

• реестр + однородность МКТУ → возражение в ППС
• витрина/реклама → претензия и суд параллельно аннулированию
• отказ ППС → обжалование в СИП

Читать: {PUBLIC_SITE_URL}/konkurent-zaregistriroval-pohozhiy-tovarnyy-znak
```

## Перелинковка

- [ ] Добавить ссылку на новый пост в ленту /news (рубрика 9), если нет авто
- [ ] Inbound interlinker: L08 и L21 → L33 по «возражение против предоставления правовой охраны» (авто `--apply`)
- [ ] Рассмотреть inbound из L19/L27 на «похожий знак / маркетплейс» (ручная вставка, если `anchor_variants` L33 не сматчатся в чужих HTML)
- [ ] Outbound в L33: writer — L08, L21, L19 canonical; interlinker inbound **2** (L08, L21)
- [ ] После publish — перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «конкурент зарегистрировал похожий товарный знак» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-05): interlinker `--apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **2** автоматические inbound-вставки (L08 → L33, L21 → L33 по «возражение против предоставления правовой охраны»; outbound writer уже в `article.html`). `memory/blog/interlink-suggestions.json` обновлён. llms: `memory/blog/llms.txt` + `llms-full.txt` (38 статей, `/blog/{slug}/`, site-base Lireate); `memory/blog/lireate-site/` и копии в каталоге L33 — **33** L-статьи с `canonical_path` (добавлен L33). Live publish не выполнялся.
