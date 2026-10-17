# Автопубликация Lireate — что нужно от вас

Сейчас пайплайн **готовит статью** (`article.html`, картинки, `publish-bundle/`).  
Чтобы **`python3 scripts/lireate_news_publish.py` сам выложил материал в /news**, не хватает **одного из каналов ниже**.

## Уже должно быть в Cloud Secrets

| Переменная | Значение |
|------------|----------|
| `LIREATE_SFTP_HOST` | IP из ISPmanager «FTP-клиент» (не A-запись сайта) |
| `LIREATE_SFTP_PORT` | **`21`** (не `22`) |
| `LIREATE_SFTP_USER` / `LIREATE_SFTP_PASSWORD` | FTP-учётка |
| `LIREATE_REMOTE_SITE_ROOT` | Каталог после входа FTP (pwd в FileZilla сразу после login) |
| `LIREATE_PUBLIC_SITE_URL` | Публичный URL сайта (только в Secrets) |
| `LIREATE_ALLOW_PUBLISH` | `yes` |

Проверка: `python3 scripts/lireate_reg_ru_check.py`

## Почему одного FTP мало

Новости на сайте хранятся в **CMS (админка + БД)**, а не как отдельный `.html` в корне.  
FTP нужен в основном для **картинок** в `/template/images/blog/`.  
Создать запись в рубрике **«Товарный знак» (`category_id=9`)** без админки/БД скрипт пока не умеет.

## Вариант A (рекомендуемый): учётка админки

Добавьте в **Cursor → Cloud Secrets**:

| Переменная | Описание |
|------------|----------|
| `LIREATE_ADMIN_URL` | Опционально; иначе `{LIREATE_PUBLIC_SITE_URL}/admin/` |
| `LIREATE_ADMIN_USER` | Логин редактора блога |
| `LIREATE_ADMIN_PASSWORD` | Пароль |

После этого можно доработать `lireate_news_publish.py` под **HTTP-форму** вашей CMS (нужен один тестовый прогон с вашей стороны или экспорт HTML формы «создать новость»).

**Ограничение:** с **IP Cursor Cloud** админка часто отдаёт anti-bot (`RCPC` → 403). Тогда используйте **вариант B**.

## Вариант B: self-hosted worker (рекомендуется)

Пошагово: **`shared/lireate-worker-setup.md`** (pool `lireate`, probe CMS, publish).

1. Worker на ПК/VPS, где открывается `/admin/login.php`.
2. Те же секреты `LIREATE_*` + `LIREATE_ADMIN_*`.
3. `python3 scripts/lireate_cms_probe.py` → `memory/lireate-cms-http-config.json`.
4. `python3 scripts/lireate_news_publish.py` или Automation на pool **`lireate`**.

## Вариант C: прямой доступ к MySQL (максимум автоматики)

Если дадите доступ к БД сайта (только в Secrets, не в git):

| Переменная | Описание |
|------------|----------|
| `LIREATE_DB_HOST` | Хост MySQL (часто `localhost` с туннеля или хост REG.RU) |
| `LIREATE_DB_PORT` | `3306` |
| `LIREATE_DB_NAME` | Имя БД |
| `LIREATE_DB_USER` / `LIREATE_DB_PASSWORD` | Пользователь БД |

Нужны **имена таблиц** новостей и поле `category_id` (или SQL-дамп структуры из phpMyAdmin). Без схемы БД автоматическая вставка не делается.

## Вариант D: готовая сессия (временный костыль)

| Переменная | Описание |
|------------|----------|
| `LIREATE_ADMIN_COOKIE` | Строка `Cookie:` после ручного входа в `/admin/` в браузере (срок жизни ограничен) |

Подходит для разовых публикаций, пока не настроены A или C.

## Что сделать прямо сейчас (минимум)

1. Исправить в Secrets: **`LIREATE_SFTP_PORT=21`** (если стоит `22`, FTP ломается).
2. Добавить **`LIREATE_ADMIN_USER`** и **`LIREATE_ADMIN_PASSWORD`** (вариант A).
3. Написать в чат: «секреты админки добавил» — доделаем HTTP-публикацию в CMS.
4. Если админка с Cloud не пускает — включить **self-hosted worker** (вариант B).

## Ручная публикация (пока нет A/B/C)

`python3 scripts/lireate_news_publish.py --dry-run` → каталог `publish-bundle/` и шаги в `lireate-publish-result.json` → `manual_steps`.
