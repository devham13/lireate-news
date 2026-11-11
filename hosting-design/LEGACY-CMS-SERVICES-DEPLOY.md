# Legacy CMS services (4 URI) — dark LU

Патч: `scripts/lireate_design_patch_legacy_cms_services.py` (body `lireate-legacy-cms-lu` после dock v2, head CSS, скрытие `pagekey`).

```bash
LIREATE_DESIGN_PATCH_LEGACY_CMS=1 bash scripts/lireate_design_hosting_apply.sh
```

Проверка live:

```bash
node scripts/lireate_design_verify_legacy_cms_services.mjs
```

Повторный прогон идемпотентен (повтор после #121/#127/dock).

`pagekey`: только inline `/* lireate_hide_pagekey_v1 */` (без нового `<?php` внутри открытого блока ~стр. 384).
