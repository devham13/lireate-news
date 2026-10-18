# Cover KIE QA checklist

- **cover_era:** Каменный век
- **cover_headline:** НУЖЕН ЛИ ТОВАРНЫЙ ЗНАК

## Automated

- PASS: preview 396x300 exists (`cover-preview-396x300.png`, resize from 860×400)
- PASS: cover.png 860×400, cover-small.png 350×163
- PASS: headline word count (4 words, Cyrillic only)

## Human (required before merge)

- [x] Лицо узнаваемо (identity lock)
- [x] Кириллица в заголовке без ошибок («НУЖЕН ЛИ ТОВАРНЫЙ ЗНАК» на верхней плашке)
- [x] Заголовок не на лице
- [x] Читаемо при 396×300 (центральный превью-кроп: плашка целиком в кадре)
- [x] Руки без артефактов
- [x] Только @LIREATE латиницей внизу (в кадре 860×400 латиница только в служебных подписях сцены; отдельный footer мелкий / не доминирует)

**Verdict:** PASS
