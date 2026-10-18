# Lireate NEWS — контракт публикации (REG.RU, не WordPress)

Сайт: домен из `LIREATE_PUBLIC_SITE_URL`, рубрика «Блог» (`/news`), категории через query `category=<id>`.

**Юридические страницы в тексте статей:** политика и согласие на ПДн — только `shared/lireate-legal-page-urls.md` (не `/privacy/`, не `/policy`).

## Секреты (только `LIREATE_*`)

| Переменная | Назначение |
|------------|------------|
| `LIREATE_SFTP_HOST` | Хост FTP из ISPmanager (не A-запись сайта) |
| `LIREATE_SFTP_PORT` | `21` (FTP; имена `SFTP_*` исторические) |
| `LIREATE_SFTP_USER` / `LIREATE_SFTP_PASSWORD` | Учётная запись FTP |
| `LIREATE_REMOTE_SITE_ROOT` | `CWD` после логина (корень `public_html`) |
| `LIREATE_PUBLIC_SITE_URL` | Публичный URL сайта (без секретов в git) |
| `LIREATE_ALLOW_PUBLISH` | `yes` — разрешить реальную выкладку |

**Запрещено** для Lireate: `excalibur_blog_wp_publish.py`, `FTP_*` / `SFTP_*` (BeGet), `WP_*`.

## Входные артефакты статьи

Каталог `memory/blog/articles/<TOPIC>-<slug>/`:

| Файл | Назначение |
|------|------------|
| `article.html` | Тело (фрагмент без обёртки темы) |
| `article.meta.json` | `slug`, SEO, `lireate_category_id`, `canonical_path` |
| `cover/cover.png` | Featured / OG |
| `cover/inline-*.png` | Иллюстрации в тексте |
| `schema.jsonld` | BlogPosting + FAQPage (в мета темы или вручную) |

## Поля CMS (наблюдаемое поведение сайта)

- Список: `/news`, фильтр «Товарный знак» → `category_id=9` (`/news?num=2&category=9`).
- ЧПУ статей: корневой путь, например `/kak_zapolnit_zayavku_na_tovarnyiy_znak` (под L01 допускается slug с дефисами по `canonical_path`).
- Картинки в статьях на сервере: `/template/images/blog/<имя_файла>`.
- Админка: `/admin/` (логин `admin/login.php`), с challenge-cookie; с IP Cloud Agent часто **403** после редиректов.
- Публичный `wp-login.php` на домене — редирект-ловушка, не канал публикации Lireate.

## Автоматизация

Полный чеклист секретов: **`shared/lireate-autopublish-requirements.md`**.

```bash
python3 scripts/lireate_news_publish.py \
  --article-dir memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent
```

Скрипт:

1. Проверяет `LIREATE_ALLOW_PUBLISH` и **`LIREATE_SFTP_PORT=21`**.
2. Собирает `publish-bundle/`.
3. Загружает картинки по FTP (если data channel доступен).
4. Создание записи в CMS — после **`LIREATE_ADMIN_*`** (или БД); см. requirements doc.
5. Журнал: `shared/published-articles-lireate.md`.

## Журнал

`shared/published-articles-lireate.md` — date | topic_id | slug | url | category_id | status.

## Post-publish

- Live URL 200, рубрика 9, обложка и inline-картинки.
- `llms.txt` / `llms-full.txt` в корне (артефакты `memory/blog/lireate-site/`).
- Handoff: маркер `=== EXCALIBUR BLOG PUBLISH ===` в `.cursor/excalibur-blog-handoff.md`.
