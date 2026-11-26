# Promotion checklist — L85 ukrali-fotografii-kak-zafiksirovat-narushenie-i-zashchitit-prava

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/ukrali_fotografii_kak_zafiksirovat_narushenie_i_zashchitit_prava/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Авторское право (`category_id=8`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=8`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links (200): `/mozhno-li-publikovat-foto-kartin-hudozhnika/` (L13), `/kak_zashchitit_intellektualnye_prava_v_sude/` (×2), `/konkurent_zaregistriroval_vash_brend_kakie_est_varianty/` (L83), `/prodazha_originalnogo_tovara_kogda_sporyat_ob_ischerpanii_prava/` (L84), `/kompensatsiya_za_narushenie_tovarnogo_znaka_raschet_i_dokazatelstva/` (L81)
- [ ] Яндекс.Вебмастер / GSC — URL отправлен
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта

## Соцсети / каналы

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Фиксация до письма, ст. 1301, не 1515 | ☐ |
| VK / Max | Фотографы, студии, маркетинг | ☐ |

## Snippet для Telegram (черновик)

```
Украли фото? Сначала URL и время на скрине — потом претензия и ст. 1301.

• ППВС № 10 п. 55
• 30 дней по п. 5.1 ст. 1252
• 10k–10M за фото, не за товарный знак

Читать: {LIREATE_PUBLIC_SITE_URL}/ukrali_fotografii_kak_zafiksirovat_narushenie_i_zashchitit_prava/
```

## Перелинковка

- [ ] **После live L83/L84:** reciprocal links в новых статьях на L85 (блок кластера)
- [ ] **L13:** inbound «до публикации» vs L85 «после кражи»
- [ ] Interlinker `--apply` после появления L83/L84 html
- [ ] llms копии в каталоге (indexer 2026-11-26)

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read`
- [ ] Primary query «украли фотографии что делать»

## Notes

Indexer (2026-11-26): interlinker full blog — **0** авто; ручной блок L83-L85 + L81 в `article.html`. L83/L84 без html — outbound только с L85. llms: 88 статей в `memory/blog/llms.txt`; копии в каталоге L85. `shared/published-articles.md` не обновлялся.