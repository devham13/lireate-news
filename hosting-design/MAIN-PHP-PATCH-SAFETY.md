# main.php — безопасный деплой дизайна

## Инцидент 2026-11-11

`lireate_design_patch_main.py` (PR #110) обрезал `template/main.php` до ~1893 строк: в цикле hero-патчей
использовалось `text = before + block` **без хвоста** после следующего `<?php if($temp['page']`.

На хостинге сохранён артефакт: `main.php.broken-2026-11-11-0800`.

## Правила

1. **Нет** полного копирования `main.php` из git (файла там нет).
2. Патч только через `scripts/lireate_design_patch_main.py` (без hero) или точечный sed.
3. Hero — отдельно `lireate_design_patch_heroes.py` (хвост сохраняется).
4. Перед/после: `lireate_main_php_guard.sh` — `wc -l` ≥ 5000, `page_container`, `php -l`.
4b. Патчи main.php идут через `lireate_design_main_php_patch_lib.sh` (копия `.patch-work` → guard/php -l → `mv`; при ошибке откат из `.pre-design-patch` / `*.bak-2026-11-11-design`).
5b. **Инцидент 2026-11-11 #118:** dock v2 нельзя было апгрейдить regex по body — только точная замена v1-сниппета. См. `scripts/lireate_design_service_mobile_dock_selftest.sh`.
5. После: `lireate_design_post_deploy_verify.sh` — 10 URL, ровно один `<h1>`.
6. `touch template/main.php` после записи (opcache).

## CMS dark (patent/mktu) — точечные зоны

- `<head>` ~303–317: Inter + `lireate-cms-page-dark.css` (+ home extras).
- `<body class=…>`: `lireate-cms-page-dark` для страниц из списка.
- JS ~1470: `lireateResizeMainScreen` + класс `lireate-cms-page-dark`.

Деплой CSS/JS: `LIREATE_DESIGN_PATCH_MAIN=0 bash scripts/lireate_design_hosting_apply.sh` (по умолчанию main.php **не** трогаем).
