# Cover KIE QA checklist

- **cover_era:** Мушкетёры
- **cover_headline:** (ручная замена обложки оператором)

## Automated

- PASS: preview 396x300 exists (`cover-preview-396x300.png`, центральный кроп с 860×400)
- PASS: cover.png 860×400, cover-small.png 350×163

## Human (required before merge)

- [x] Лицо узнаваемо (identity lock)
- [x] Кириллица в заголовке без ошибок («ПРЕТЕНЗИЯ: 30 ДНЕЙ НА ОТВЕТ»)
- [x] Заголовок не на лице
- [x] Читаемо при 396×300 (центральный кроп: плашка в верхней трети, текст целиком в средней трети ширины кропа)
- [x] Руки без артефактов
- [x] Только @LIREATE латиницей внизу
