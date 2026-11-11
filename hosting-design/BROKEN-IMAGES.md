# Битые картинки (без правок CMS/DB)

Скан: `node scripts/lireate_broken_images_crawl.mjs` (переменные `LIREATE_IMG_SCAN_PAGES`, `LIREATE_IMG_SCAN_CONCURRENCY`).

На live ~41 уникальный URL при 100 страницах sitemap (часть — HEAD=0 на REG.RU).

Деплой: JS прячет `img` после `error` / `naturalWidth===0`:

```bash
LIREATE_DESIGN_PATCH_BROKEN_IMAGES=1 bash scripts/lireate_design_hosting_apply.sh
```

Долгосрочно: залить файлы в `/template/images/...` или поправить HTML в CMS (не в этом репо).
