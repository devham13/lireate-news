# LU wide column center (`lireate_lu_column_center_v1`)

На ≥1400px колонка 1120px в правой панели (после `#leftSideBar`) центрируется через `margin-left/right: auto` — как `.page_container` на `/uslugi/`.

**Файлы:** `lireate-lu-viewport.css` (vp5), `lireate-cms-lu.css`, `lireate-mktu-lu.css`, `lireate-home-lu.css`.

**Деплой** — без нового флага, достаточно копии CSS тем же apply:

```bash
LIREATE_DESIGN_PATCH_STATIC=1 \
LIREATE_DESIGN_PATCH_GLOBAL_UX=1 \
LIREATE_DESIGN_PATCH_NEWS_LU=1 \
LIREATE_DESIGN_PATCH_LEGACY_CMS=1 \
bash scripts/lireate_design_hosting_apply.sh
```

`sed` в apply поднимет `lireate-lu-viewport.css?v=20261111vp5` в `main.php`.

**QA:** `node scripts/lireate_design_lu_column_center_check.mjs`, скриншоты `node scripts/lireate_design_lu_column_center_screenshots.mjs`.
