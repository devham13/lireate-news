# Деплой /dogovory/ и /registraciya_programm_evm/

```bash
cd ~/lireate-autopub/design-wt
git fetch origin main && git checkout design-deploy && git merge --ff-only origin/main
```

Полный набор (после hotfix #131):

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

`DEPLOY_NEW_SERVICES` копирует `index.php`, `assets/`, `.htaccess` и патчит корневой `.htaccess`.

Verify ждёт body-маркеры до ~150 с (`LIREATE_VERIFY_BODY_RETRIES` × `LIREATE_VERIFY_BODY_SLEEP`); `/reviews` без завершающего `/`; poisk — класс или маркер `legacy_cms_services_v1`. При провале — откат `main.php` из `*.bak-2026-11-11-design-pre-apply`. Python для патчей: **≥3.8** (`python3.12` на REG.RU), см. `lireate_design_resolve_python.sh`.
