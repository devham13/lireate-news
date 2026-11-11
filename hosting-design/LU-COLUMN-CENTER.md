# LU wide column center (`lireate_wide_center_hotfix_v2` / `lireate_lu_column_center_v1`)

На ≥1400px колонка 1120px в правой панели (после `#leftSideBar`) центрируется через `margin-left/right: auto` — как `.page_container` на `/uslugi/`.

**Файлы:** `lireate-lu-viewport.css` (**vp6**, брейкпоинт **1500px**), `lireate-cms-lu.css`, `lireate-mktu-lu.css`, `lireate-home-lu.css`.

**Деплой** — без нового флага, достаточно копии CSS тем же apply:

```bash
LIREATE_DESIGN_PATCH_STATIC=1 \
LIREATE_DESIGN_PATCH_GLOBAL_UX=1 \
LIREATE_DESIGN_PATCH_NEWS_LU=1 \
LIREATE_DESIGN_PATCH_LEGACY_CMS=1 \
LIREATE_DESIGN_PATCH_SERVICE_DOCK=1 \
LIREATE_DESIGN_PATCH_SERVICE_LANDINGS=1 \
LIREATE_DESIGN_DEPLOY_NEW_SERVICES=1 \
LIREATE_DESIGN_PATCH_HOME_SERVICE_URLS=1 \
LIREATE_DESIGN_PATCH_USLUGI_CARDS=1 \
bash scripts/lireate_design_hosting_apply.sh
```

`sed` в apply поднимет `lireate-lu-viewport.css?v=20261111vp6` в `main.php` (cache-control immutable ~30д).

**QA:** `node scripts/lireate_design_lu_column_center_check.mjs`, скриншоты `node scripts/lireate_design_lu_column_center_screenshots.mjs`.
