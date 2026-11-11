# Новые LU-лендинги: /dogovory/ и /registraciya_programm_evm/

Деплой из worktree (не из основного cron-repo):

```bash
cd ~/lireate-autopub/design-wt
git fetch origin main && git checkout design-deploy && git merge --ff-only origin/main

LIREATE_DESIGN_DEPLOY_NEW_SERVICES=1 \
LIREATE_DESIGN_PATCH_HOME_SERVICE_URLS=1 \
LIREATE_DESIGN_PATCH_USLUGI_CARDS=1 \
LIREATE_DESIGN_PATCH_SERVICE_LANDINGS=1 \
LIREATE_DESIGN_PATCH_SERVICE_DOCK=1 \
bash scripts/lireate_design_hosting_apply.sh
```

- `LIREATE_DESIGN_DEPLOY_NEW_SERVICES` — копирует `hosting-design/service-landings/{dogovory,registraciya_programm_evm}/index.php` в DOCROOT (отдельно от `LIREATE_DESIGN_PATCH_CMS=1`, чтобы не пересекаться с legacy CMS PR).
- `LIREATE_DESIGN_PATCH_HOME_SERVICE_URLS` — ссылки в модалке главной и кнопки «Подробнее» (патч `main.php` через guard).
- `LIREATE_DESIGN_PATCH_USLUGI_CARDS` — карточки на `/uslugi/`.
- `LIREATE_DESIGN_PATCH_SERVICE_LANDINGS` — канонический `.lx-mobile-bar` на всех standalone LU.
- `LIREATE_DESIGN_PATCH_SERVICE_DOCK` — исключить standalone из dock в `main.php` (v2), без второй панели.

Проверка до/после:

```bash
LIREATE_LOCAL_PREVIEW=1 node scripts/lireate_design_verify_new_service_pages.mjs http://127.0.0.1:8765
# после выкладки на прод (LIREATE_PUBLIC_SITE_URL в env хостинга):
node scripts/lireate_design_verify_new_service_pages.mjs "$LIREATE_PUBLIC_SITE_URL"
node scripts/lireate_design_verify_service_dock_count.mjs "$LIREATE_PUBLIC_SITE_URL"
```

Локальный превью-сервер (страницы из репо):

```bash
php -S 127.0.0.1:8765 -t hosting-design/service-landings
```

Sitemap: пути в `shared/lireate-sitemap-static.json` подхватывает существующий пайплайн sitemap на хостинге.
