# Автопубликация новостей Lireate на хостинге REG.RU

Путь для **ISPmanager Shell + CRON**: код в `$HOME/lireate-autopub`, статья попадает в MySQL таблицу `news` через **PHP CLI** (подключает `public_html/data/db.php` — пароль БД **не** кладём в `.env`).

Актуальный production: `memory/hosting/lireate-reg-ru-production.md` (`u3650956`, `server324.hosting.reg.ru`).

## Установка

```bash
export LIREATE_REPO_BRANCH=cursor/lireate-hosting-cron-762f
curl -fsSL "https://raw.githubusercontent.com/devham13/lireate-news/${LIREATE_REPO_BRANCH}/scripts/lireate_hosting_install.sh" | bash
```

В `.env` укажите:

- публичный URL сайта в `.env` (шаблон установщика, https://…)
- `LIREATE_DOCROOT=$HOME/www/public_html` (полный путь: `/var/www/u3650956/data/www/public_html`)
- `LIREATE_ALLOW_PUBLISH=no` до тестов

## Команды на сервере (копировать блоками)

### Обновить код

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
cd "$LIREATE_AUTOPUB_HOME/repo"
git fetch origin cursor/lireate-hosting-cron-762f
git checkout cursor/lireate-hosting-cron-762f
git pull
```

### Self-check

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_selfcheck.py"
```

### Диагностика БД (read-only)

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_db_diagnostic.py"
```

### Dry-run L01 (без INSERT)

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_publish.py" --dry-run
```

### Реальная публикация L01

В `.env` поставьте `LIREATE_ALLOW_PUBLISH=yes`, затем:

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_publish.py"
```

Успех: `STATUS: PUBLISHED` и HTTP 200 на URL статьи.

### CRON (ежедневно 12:00 Москва)

```cron
TZ=Europe/Moscow
0 12 * * * $(cat $HOME/lireate-autopub/.python-interpreter) $HOME/lireate-autopub/repo/scripts/lireate_hosting_publish.py >> $HOME/lireate-autopub/logs/cron.log 2>&1
```

## Почему не HTTP-админка

На `/admin/login.php` есть **captcha**; автоматический вход без человека не делаем. Публикация — прямой INSERT как в `admin/editor/news.php`.

## Логи

`$HOME/lireate-autopub/logs/publish.log`, состояние: `state/published.json`.
