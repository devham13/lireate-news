# Lireate REG.RU — выкладка SEO-артефактов из репозитория

Документ зафиксирован по факту с production (2026-11-10). CMS-ядро **не** лежит в git; в репо — эталоны и скрипты.

## Docroot

| Переменная | Путь (типично) |
|------------|----------------|
| `LIREATE_DOCROOT` | `/var/www/<user>/data/www/public_html` |
| Автопаб | `~/lireate-autopub/repo` |

## Wave 1 / каноникал / htaccess (уже на сервере)

| Репо | Сервер | Назначение |
|------|--------|------------|
| `hosting-seo/data/lireate-seo-runtime.php` | `data/lireate-seo-runtime.php` | Парсинг `REQUEST_URI`, `$lireate_canonical_url`, noindex |
| `hosting-seo/data/lireate-seo-head.inc.php` | `data/lireate-seo-head.inc.php` | `<link rel="canonical">`, robots meta |
| `hosting-seo/lireate-seo.htaccess.inc` | вставка в корневой `.htaccess` | 301, слэши, noindex env |
| — | `index.php` (начало) | `require data/lireate-seo-runtime.php` |
| — | `template/main.php` (`<head>`) | `require data/lireate-seo-head.inc.php` + `lireate_seo_render_head_tags()` |

Фрагмент `template/main.php` (подтверждено на live):

```php
$_lireate_seo_head = dirname(__DIR__) . '/data/lireate-seo-head.inc.php';
if (is_file($_lireate_seo_head)) {
    require_once $_lireate_seo_head;
    lireate_seo_render_head_tags();
}
```

**Бэкап перед правками:** `*.bak-2026-11-10-seo3` (или актуальная дата волны).

## Мессенджеры (ошибки «lireate-messenger-urls.php not found»)

Канонический файл: `template/lireate/lireate-messenger-urls.php`.

Лендинги и конфиги ищут также:

- `pages/services/_shared/lireate-messenger-urls.php`
- `template/page/news/lireate-messenger-urls.php` (есть)

На сервере **нет** каталога `pages/services/_shared/` — из-за этого падают часть услуг. Исправление: создать каталог и положить тонкий `require` на канон (см. `scripts/lireate_hosting_messenger_shim.sh`).

Дополнительно: `template/parts/online.php` — плавающий виджет TG/WA/MAX; подвал — `template/lireate/lireate-service-footer.inc.php`.

## Блог / schema

| Путь на сервере | Роль |
|-----------------|------|
| `template/page/news/lireate-blog-*.php` | Рендер статей, подвал, подписка |
| `template/page/news/lireate-blog-load.php` | `lireate_blog_dir_up()` (единственное определение — не дублировать require без `require_once`) |
| `pages/blog/_shared/lireate-blog-load.php` | Копия load; подключать **только один** экземпляр за запрос |

JSON-LD: генерируется в репо (`memory/blog/articles/L*/schema.jsonld`), на live часто **вшит в шаблон** из CMS — не через `lireate_hosting_publish.py`. Wave 2: явно прописать вывод schema в шаблоне статьи или колонке БД.

## Публикация статей из git

```bash
export LIREATE_ENV_FILE=~/lireate-autopub/.env
PY=$(cat ~/lireate-autopub/.python-interpreter)
cd ~/lireate-autopub/repo
"$PY" scripts/lireate_hosting_publish.py --update --article-dir memory/blog/articles/Lxx-.../
```

`--update` **не** меняет `news.datetime` (см. `scripts/lireate_db_publish.php`).

## Диагностика

```bash
DOCROOT=$(grep ^LIREATE_DOCROOT= ~/lireate-autopub/.env | cut -d= -f2-)
php ~/lireate-autopub/repo/scripts/lireate_db_publish.php diagnostic "$DOCROOT"
php ~/lireate-autopub/repo/scripts/lireate_db_publish.php sitemap_urls "$DOCROOT"
```

## Что сознательно не в git

- `template/main.php`, `engine/func/function.php`, большинство `template/page/*`
- Правки — через бэкап на сервере + опциональные патчи в `hosting/lireate-php-patches/`

## Связанные файлы репозитория

- `docs/seo-cannibalization-decisions-2026-11-10.md`
- `memory/hosting/lireate-reg-ru-production.md`
- `scripts/lireate_hosting_messenger_shim.sh` — каталог `_shared` и симлинк мессенджера
