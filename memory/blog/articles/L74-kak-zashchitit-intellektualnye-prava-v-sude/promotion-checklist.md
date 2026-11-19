# Promotion checklist — L74 kak-zashchitit-intellektualnye-prava-v-sude

Дата публикации: YYYY-MM-DD  
Live URL: `{LIREATE_PUBLIC_SITE_URL}/kak_zashchitit_intellektualnye_prava_v_sude/` (канон `lireate_seo_url`; подтвердить после INSERT)  
Рубрика: Бизнес (`category_id=15`) — `{LIREATE_PUBLIC_SITE_URL}/news?num=2&category=15`

Excalibur создаёт этот файл после `✅ ARTICLE OK` (до или после выкладки на Lireate /news).

## Сразу после publish

- [ ] Открыть live URL — title, excerpt, featured image, FAQ
- [ ] View source — JSON-LD BlogPosting + FAQPage (`schema.jsonld`)
- [ ] Проверить internal links из статьи (200): `/narushenie-tovarnogo-znaka-na-marketpleyse/`, `/sajt-klon-zashchita-brenda-v-internete/`, `/kak_zashchitit_kompyuternuyu_programmu_ot_plagiata/`, `/zashchita_prav_na_bazu_dannyh_kak_oformit_i_dokazat_narushenie/`, `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/` (×2), `/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta/`, `/konkurent_zaregistriroval_pohozhiy_tovarnyy_znak/`, CTA `/uslugi/`, `/contacts/`, `/reg-tz-main/`
- [ ] Яндекс.Вебмастер / GSC — URL отправлен (если настроено)
- [ ] Выложить `llms.txt` / `llms-full.txt` в корень сайта (артефакты в `memory/blog/` и `memory/blog/lireate-site/`)

## Соцсети / каналы (из conversion-tracking-map)

| Канал | Действие | Статус |
|-------|----------|--------|
| Telegram | Пост: hook + ссылка + 1 факт из статьи | ☐ |
| VK / Max | Адаптировать под ЦА (правообладатели, ИП, бренд) | ☐ |
| Email / рассылка | Если есть в conversion map | ☐ |

## Snippet для Telegram (черновик)

```
Нарушили бренд или контент? Без объекта права и ст. 1252 иск в арбитраж могут вернуть.

• объект ИС → требования п. 1 ст. 1252 → фиксация по п. 55 ППВС № 10
• претензия 30 дней при денежном иске ЮЛ/ИП
• компенсация: 1515 / 1301 / 1311 и ст. 1252.1 с 04.01.2026

Читать: {LIREATE_PUBLIC_SITE_URL}/kak_zashchitit_intellektualnye_prava_v_sude/
```

## Перелинковка

- [ ] **После live L74:** L75 «ответ на претензию (любой объект)» → inbound на anchor «ответ на чужую претензию» (заменить/дополнить L02 в L74)
- [ ] **После live L76:** L74 п. «ответчик оспаривает компенсацию» → ссылка на L76 (live)
- [ ] Inbound из L27, L24, L32 на anchor_variants L74 (судебный маршрут правообладателя)
- [ ] Перезапустить `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL`

## Метрики (7 дней)

- [ ] Metrika / GA4 — goal `blog_read` или из conversion map
- [ ] Позиция primary query «как защитить интеллектуальные права в суде» (ручная проверка / Wordstat)

## Notes

Indexer (2026-11-19): CLI `--article-dir` не поддерживается — `excalibur_blog_interlinker.py --apply --blog-dir memory/blog/articles --site-base $LIREATE_PUBLIC_SITE_URL` — **0** автоматических вставок (77 статей). Ручные outbound: L74→L02 (×2, live `/otvet_na_pretenziyu_pravoobladatelya_tovarnogo_znaka_poryadok_srok_30_dney_i_obrazec/`); кластер L75/L76 **не** в outbound до HTTP 200 их canonical URL. llms: `memory/blog/llms.txt` + `llms-full.txt` (77 статей); `lireate_llms_site_generate.py` → **72** L-записей в `memory/blog/lireate-site/llms.txt`; копии `llms.txt` / `llms-full.txt` в каталоге L74. `link-verify.json` — **pass**. Live publish: не выполнялся (CRON REG.RU после merge).