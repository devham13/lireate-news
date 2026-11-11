# Legacy CMS blog → LU template

Деплой **только CSS** (без main.php):

```bash
bash scripts/lireate_design_hosting_apply.sh
```

С патчем `main.php` для `news_id`:

```bash
LIREATE_DESIGN_PATCH_NEWS_LU=1 bash scripts/lireate_design_hosting_apply.sh
```

Проверка:

```bash
node scripts/lireate_legacy_blog_scan.mjs   # legacyCount должен быть 0
node scripts/lireate_design_verify_legacy_blog.mjs
```
