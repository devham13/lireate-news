# Каннибализация L-статей vs legacy URL (10.11.2026)

Правило: **старая страница с показами/позициями остаётся главной**; редиректы 301 **не применялись** (только решения). Тип (б) — правки в этой ветке PR.

| Новая (L) | Старая (показы / поз. / входы 30д) | Решение | Обоснование |
|---|---|---|---|
| L22, L36 | `/markirovka_importnyix_tovarov_chestnyiy_znak/` (238 / 20.9 / 14) | **Развести** | L22 — чек-лист импортёра (Data Matrix, ФТС); старая — общий обзор ЧЗ. Перекрёстная ссылка L22→legacy в PR. |
| L08, L21, L28 | `/kuda_podat_vozrazhenie_protiv_registracii_tovarnogo_znaka/` (176 / 12.4 / 27) | **Развести** | Старая — «куда подать»; L08 — ветки обращение/ППС по ст. 1493/1512. Ссылка L08→legacy в PR. |
| L39 | `/dorabotka_tovarnogo_znaka_kak_dorabotat_logotip_i_naimenovanie/` (144 / 6.2) | **Развести** | Старая — общая доработка; L39 — PDF/кабинет и ст. 1497. Ссылка + title в PR. |
| L10 | `/domennoe_imya_kak_nematerialnyiy_aktiv/` (69 / 9.1) | **Развести** | L10 — ФСБУ 14/2022 и учёт; старая — НМА в общем. Перекрёстная ссылка при публикации. |
| L20 | `/registraciya_mobilnogo_prilozheniya_v_rospatente/` (61 / 10.5) | **Развести** | L20 — ЭВМ vs ТЗ в 2026; старая — общий патентный гайд. |
| L19 | `/chto_delat_esli_tovarnyiy_znak_zanyat/` (41 / 6.8) | **301** (после согласования) | Почти тот же URL и интент; старая в выдаче. Новую снять из sitemap, 301 не применяли. |
| L02 | `/otvet_na_pretenziyu_o_narushenii_…` (36 / 11.3) | **Развести** | L02 — срок 30 дней и образец 2026; старая — нужен ли ответ. |
| L05 | `/sposobyi_zaschityi_izobreteniy_i_sekretov…` (32 / 8.4) | **Развести** | L05 — патент/ноу-хау/публикация; старая — без сравнительной таблицы. |
| L11 | `/kak_oformit_avtorskie_prava_na_logotip/` … | **Развести** | L11 — договор с дизайнером; legacy — оформление прав. |
| L09 | `/mozhno_li_upominat…` (25 / 7.5) | **Развести** | L09 — форматы рекламы; старая — упоминание бренда. |
| L35 | `/vyiplata_avtorskogo_voznagrazhdeniya…` (23 / 11.4 / 23) | **Развести** | L35 — ГК РФ 2026; старая — выплата автору. |
| L26, L37 | `/zaschita_dizayna_tovara_i_upakovki/` (19 / 12.9) | **Развести** | L-материалы — маркетплейсы/выбор ПО vs ТЗ; legacy общий. |
| L24 | `/kak_zablokirovat_saytklon_/` (24 / 12.5) | **Развести** | L24 — блокировка клона 2026; старая — общая защита бренда. |
| L33 | `/konkurentyi_zaregistrirovali…` (19 / 10.4) | **Развести** | L33 — похожий знак раньше; legacy — другой угол. |
| L14 | `/kak_dokazat_razglashenie_kommercheskoy_taynyi…` (6 / 12.2 / 6) | **Развести** | L14 — ввод режима; старая — доказать разглашение. |
| L04 | `/chto_delat_esli_otkazali_v_vyidache_patenta/` (6 / 8.8) | **Развести** | L04 — ППС и сроки; тема та же, но L сильнее по интенту «что дальше». Мониторинг; 301 не сейчас. |
| L07 | `/osnovaniya_dlya_otkaza_v_registracii_tovarnogo_znaka/` | **Развести** | L07 — ответ экспертизе; legacy — перечень оснований. |
| L15 | dosrochnoe_prekraschenie (две legacy) | **Развести** | L15 — иск неиспользования; legacy — общие процедуры. |
| L25 | `/kak_zaregistrirovat_brend_odezhdyi/` (26 / 11.5) | **Развести** | L25 — МКТУ одежда 2026; legacy — регистрация бренда. |
| L50, L41 | `/kak_prodat_tovarnyiy_znak/` … | **Развести** | L41/L50 — отчуждение и налоги 2026; legacy — продажа. |
| L01, L18, L29, L38 | `/findtz/`, poisk… | **Развести** | L — чек-листы/checklist; услуга findtz — коммерческий интент. |
| L30, L34, L40 | `/registraciya_tovarnogo_znaka/`, reg-tz-main | **Развести** | L — DIY/осмысление; услуга — под ключ. Ссылки на `/registraciya_tovarnogo_znaka/` в PR. |
| L47 | `/prodlenie_tovarnogo_znaka/` | **Развести** | L47 — пошлины 2026; услуга — сопровождение. |

**Полный дубль (кандидат 301):** только L19 → `/chto_delat_esli_tovarnyiy_znak_zanyat/` (внедрение редиректа и sitemap — отдельным шагом после выкладки PR).
