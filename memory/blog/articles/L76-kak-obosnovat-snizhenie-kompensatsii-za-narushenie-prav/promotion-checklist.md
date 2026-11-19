# Promotion checklist — L76 kak-obosnovat-snizhenie-kompensatsii-za-narushenie-prav

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/kak_obosnovat_snizhenie_kompensatsii_za_narushenie_prav/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Бизнес (`category_id=15`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/` (×2), `/avtorskoe-voznagrazhdenie-po-gk-rf/`, `/narushenie-tovarnogo-znaka-na-marketpleyse/` (×2), `/konkurent_zaregistriroval_pohozhiy_tovarnyy_znak/`, `/uslugi/`, `/contacts/`; внешние НПА — КонсультантПлюс (ППВС № 10 через `cons_doc_LAW_329754`)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (ответчики, селлеры) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Завышенная компенсация в претензии? Суд не снизит сумму сам — нужны контррасчёт и заявление.

• три способа по п. 4 ст. 1515 и проверка расчёта
• ст. 1252.1 (с 04.01.2026) и п. 61–62 ППВС № 10
• ходатайство в суде + практика СИП

Читать: {LIREATE_PUBLIC_SITE_URL}/kak_obosnovat_snizhenie_kompensatsii_za_narushenie_prav/
```

## Перелинковка

- [ ] **После live L76:** L75 — ссылка на L76 в блоке «Компенсация» и FAQ; L02 — одна строка «снижение в суде → L76» без дублирования
- [ ] **После live L75:** L76 intro / FAQ — ссылка на универсальный чек-лист L75 (не только L02)
- [ ] Inbound из L02 (контррасчёт) на anchor «снижение компенсации»
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «снижение компенсации за нарушение исключительных прав» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-19): interlinker — **0** авто; ручные outbound L76→L02 (×2), L27, legacy ТЗ/CTA; замена `vsrf.ru/files/27771` на КонсультантПлюс ППВС № 10 (таймаут vsrf → **pass** link-verify). Кросс-линки L75↔L76 — в чек-листе после live. llms: `memory/blog/` + `lireate-site/`; копии в каталоге L76.