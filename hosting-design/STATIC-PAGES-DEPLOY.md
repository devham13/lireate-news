# Static pages LU hotfix (spasibo / portfolio / reviews)

```bash
bash scripts/lireate_design_hosting_apply.sh
# опционально: подтянуть static-hero.js в main.php
LIREATE_DESIGN_PATCH_STATIC=1 bash scripts/lireate_design_hosting_apply.sh
```

Проверки (CSS из репо инжектится в Playwright для pre-deploy QA):

```bash
node scripts/lireate_design_static_contrast_check.mjs
node scripts/lireate_design_static_pages_screenshots.mjs
```

Кэш: `lireate-static-pages-lu.css?v=20261111static3`, `lireate-static-hero-lu.js?v=20261111static3`.

После любого патча `main.php`: `lireate_design_main_php_sanitize_cli.py` убирает хвост `</script>" />` (ботч v2 upgrade).

Проверка: `node scripts/lireate_design_verify_stray_quote.mjs`
