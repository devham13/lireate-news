# Promotion checklist — L75 poluchili-pretenziyu-pravoobladatelya-chto-proverit

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/poluchili_pretenziyu_ot_pravoobladatelya_chto_proverit/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Бизнес (`category_id=15`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/` (×2), `/narushenie-tovarnogo-znaka-na-marketpleyse/` (×3), `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta/`, `/avtorskoe-voznagrazhdenie-po-gk-rf/` (×2), `/contacts/`, `/uslugi/`, `/news?num=2&category=15`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ИП, селлеры, ответчик) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Претензия по ИС на столе? Не платите вслепую — сначала реестр, 30 дней и ответ без признания вины.

• проверка отправителя и цепочки права
• матрица объект → реестр → компенсация
• структура письма + оговорка + контррасчёт (ТЗ → L02)

Читать: {LIREATE_PUBLIC_SITE_URL}/poluchili_pretenziyu_ot_pravoobladatelya_chto_proverit/
```

## Перелинковка

- [ ] **После live L75:** L74 — inbound «если вы правообладатель, а не ответчик»; L76 — inbound на «контррасчёт / снижение в суде» (заменить отсылку только к L02)
- [ ] **После live L76:** L75 п. «Компенсация» в чек-листе ответа → ссылка на L76
- [ ] Inbound из L16, L58, L32 (претензии по контенту) на anchor_variants L75
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «получил претензию от правообладателя что делать» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-19): interlinker — **0** авто; ручные outbound: L75→L02 (×2 live), L27 (live); исправлен ошибочный якорь «L02» на МП URL. L76 не линкуется до 200. llms: `memory/blog/` + `lireate-site/` (72 L*); копии в каталоге L75. `link-verify.json` — **pass**.