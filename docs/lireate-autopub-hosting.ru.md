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

**Важно:** команды `git` выполняйте только внутри `$HOME/lireate-autopub/repo` (из `~` будет `fatal: не найден git репозиторий`). Сначала:

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
cd "$LIREATE_AUTOPUB_HOME/repo"
```

Или одной командой из любого каталога (после `git pull` хотя бы раз вручную):

```bash
bash "$HOME/lireate-autopub/repo/scripts/lireate_hosting_operator.sh"
```

Клон с feature-ветки часто **не имеет локальной `main`** — тогда `git checkout main` даёт `pathspec 'main' did not match`. Используйте:

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_REPO_BRANCH=main
bash "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_git_sync.sh"
```

Если скрипта ещё нет (старый clone), одноразово:

```bash
cd "$LIREATE_AUTOPUB_HOME/repo"
git fetch origin '+refs/heads/main:refs/heads/main'
git checkout main
git pull --ff-only origin main
```

Если `origin/main не является коммитом` — это нормально для shallow clone; достаточно `git pull --ff-only origin main` (как у вас после fast-forward).
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

### Картинки в статье

Шаблон CMS берёт **обложку списка и `imgBlock`** из `template/images/blog/`, не из `full_story`:

| Назначение | Путь на диске | Размер |
|------------|---------------|--------|
| Обложка (страница + список `/news`) | `$LIREATE_DOCROOT/template/images/blog/{seo_url}.jpg` | 860×400 |
| Миниатюра в списке | `$LIREATE_DOCROOT/template/images/blog/small/{seo_url}.jpg` | 350×163 |
| Дубль обложки (legacy) | `$LIREATE_DOCROOT/images/{seo_url}.jpg` | 860×400 |
| Inline в тексте | `$LIREATE_DOCROOT/images/{seo_url}_inline_01.jpg` … | из `cover/inline-*.png` |

Источник: `cover/cover.png`. Если на хостинге нет Pillow — те же пути, **копия** исходника (без ресайза). С Pillow — центральная обрезка и **JPEG RGB**.

В `full_story` lead-картинка как у старых новостей: `src="/template/images/blog/{seo_url}.jpg"` (838×400, не float). Inline: `/images/...`, не `cover/inline-*.png`.

Проверка после публикации:

```bash
ls -la "$LIREATE_DOCROOT/template/images/blog/"*{seo_url}*
ls -la "$LIREATE_DOCROOT/template/images/blog/small/"*{seo_url}*
ls -la "$LIREATE_DOCROOT/images/"*{seo_url}*
```

### Повторная выкладка (битые картинки, правка HTML)

Если новость уже в БД, обычный запуск выдаёт `STATUS: ALREADY_PUBLISHED` и **не** обновляет текст. Чтобы залить картинки заново и обновить `full_story`:

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
# в .env: LIREATE_ALLOW_PUBLISH=yes
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_publish.py" --update
```

Ожидаемо: `hosting_images` в `lireate-publish-result.json`, в ответе PHP `updated: true`.

### CRON (ежедневно 12:00 Москва)

Рекомендуется обёртка с `git pull` и `--update`:

```cron
TZ=Europe/Moscow
0 12 * * * bash $HOME/lireate-autopub/repo/scripts/lireate_hosting_cron.sh >> $HOME/lireate-autopub/logs/cron.log 2>&1
```

Без pull/update (устарело — после первого INSERT только `ALREADY_PUBLISHED`):

```cron
0 12 * * * $(cat $HOME/lireate-autopub/.python-interpreter) $HOME/lireate-autopub/repo/scripts/lireate_hosting_publish.py >> $HOME/lireate-autopub/logs/cron.log 2>&1
```

## Почему не HTTP-админка

На `/admin/login.php` есть **captcha**; автоматический вход без человека не делаем. Публикация — прямой INSERT как в `admin/editor/news.php`.

## Логи

`$HOME/lireate-autopub/logs/publish.log`, состояние: `state/published.json`.

## Яндекс.Вебмастер (экспорт с хостинга)

Инструкция для владельца (OAuth, cron 07:30 МСК, защищённый JSON): [lireate-webmaster-export.ru.md](lireate-webmaster-export.ru.md).
