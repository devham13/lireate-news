# Автопубликация новостей Lireate на хостинге REG.RU

Инструкция для владельца сайта **без программирования**: скрипт ставится **вне** открытой папки сайта и запускается по **расписанию CRON** в ISPmanager.

## Зачем так

С компьютеров Cursor Cloud админка `/admin/` часто показывает защиту от ботов (RCPC), а FTP «зависает» на загрузке файлов. На **самом сервере** REG.RU картинки копируются в каталог сайта напрямую, а вход в админку идёт по **локальному адресу** `127.0.0.1` — без блокировки.

## Что понадобится

- Доступ к **ISPmanager** (Shell-клиент и планировщик CRON).
- Логин и пароль редактора в `/admin/`.
- Путь к **public_html** вашего домена (в файловом менеджере — «полный путь» к корню сайта).

## Установка (один раз)

1. Откройте в ISPmanager **Shell-клиент** (как SSH).
2. Вставьте и выполните **одну команду** (после слияния PR в `main`):

```bash
curl -fsSL https://raw.githubusercontent.com/devham13/lireate-news/main/scripts/lireate_hosting_install.sh | bash
```

Если ветка ещё не в `main`, укажите ветку:

```bash
export LIREATE_REPO_BRANCH=cursor/lireate-hosting-cron-762f
curl -fsSL "https://raw.githubusercontent.com/devham13/lireate-news/${LIREATE_REPO_BRANCH}/scripts/lireate_hosting_install.sh" | bash
```

3. Скрипт создаст папку `~/lireate-autopub`, клонирует репозиторий и файл **`~/lireate-autopub/.env`** (права только для вас).

## Настройка `.env`

Откройте файл `~/lireate-autopub/.env` в редакторе ISPmanager и заполните:

| Переменная | Что указать |
|------------|-------------|
| `LIREATE_PUBLIC_SITE_URL` | `https://ваш-домен.ru` |
| `LIREATE_DOCROOT` | Полный путь к корню сайта (где лежит `index.php`) |
| `LIREATE_CMS_HTTP_BASE` | Обычно `http://127.0.0.1` |
| `LIREATE_ADMIN_USER` / `LIREATE_ADMIN_PASSWORD` | Данные входа в админку |
| `LIREATE_ALLOW_PUBLISH` | Сначала `no`, для реальной публикации — `yes` |

Секреты **не** храните в git и никому не отправляйте в чат.

## Проверка без публикации

```bash
export LIREATE_ENV_FILE=~/lireate-autopub/.env
python3 ~/lireate-autopub/repo/scripts/lireate_hosting_publish.py --dry-run
```

В конце должно быть: **`STATUS: DRY_RUN`** и папка `publish-bundle` у статьи L01.

Общая проверка окружения:

```bash
python3 ~/lireate-autopub/repo/scripts/lireate_hosting_selfcheck.py
```

## Настройка CMS (один раз)

1. В `.env` уже должны быть логин и пароль админки.
2. Выполните:

```bash
cd ~/lireate-autopub/repo
export LIREATE_ENV_FILE=~/lireate-autopub/.env
python3 scripts/lireate_cms_probe.py
```

3. Откройте созданный черновик конфига и скопируйте его в:

`~/lireate-autopub/cms-config/lireate-cms-http-config.json`

4. При необходимости поправьте имена полей формы «создать новость» (см. HTML в `memory/lireate-cms-probe/` на сервере внутри клона).

## Первая реальная публикация (статья L01)

1. В `.env` поставьте `LIREATE_ALLOW_PUBLISH=yes`.
2. Укажите путь к статье (если пусто — используется L01 по умолчанию):

```bash
LIREATE_ARTICLE_DIR=~/lireate-autopub/repo/memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent
```

3. Запуск:

```bash
python3 ~/lireate-autopub/repo/scripts/lireate_hosting_publish.py
```

Успех: **`STATUS: PUBLISHED`** и открывается страница статьи в браузере (код ответа 200).

Повторный запуск **не создаст дубликат**: если URL уже отдаёт 200, будет **`STATUS: ALREADY_PUBLISHED`**.

Лог: `~/lireate-autopub/logs/publish.log`

## CRON (ежедневно в 12:00 по Москве)

В ISPmanager → **Планировщик (CRON)** добавьте задание.

Если часовой пояс сервера **UTC** (часто на хостинге), 12:00 МСК ≈ 09:00 UTC (летом — 09:00, зимой — 09:00; для точности задайте `TZ`):

Используйте **тот же Python**, что записал установщик в `~/lireate-autopub/.python-interpreter` (на REG.RU это часто не `/usr/bin/python3`):

```cron
TZ=Europe/Moscow
0 12 * * * $(cat $HOME/lireate-autopub/.python-interpreter) $HOME/lireate-autopub/repo/scripts/lireate_hosting_publish.py >> $HOME/lireate-autopub/logs/cron.log 2>&1
```

Для вашего пути: `$HOME` = `/var/www/u3249004/data`, каталог = `lireate-autopub`.

Если планировщик **не** понимает `TZ=` в той же строке, задайте время вручную под часовой пояс сервера или добавьте в начало скрипта-обёртки `export TZ=Europe/Moscow`.

Альтернатива с блокировкой от двойного запуска (если в CRON нет `flock`):

```cron
0 12 * * * /usr/bin/python3 $HOME/lireate-autopub/repo/scripts/lireate_hosting_publish.py >> $HOME/lireate-autopub/logs/cron.log 2>&1
```

(блокировка уже внутри Python-скрипта)

## Если что-то пошло не так

| Сообщение | Что делать |
|-----------|------------|
| `BLOCKER ... CMS HTTP config` | Выполните probe и положите JSON в `cms-config/` |
| `BLOCKER ... live URL still 404` | Проверьте поля формы в `lireate-cms-http-config.json` |
| `BLOCKER another publish run` | Подождите или удалите устаревший lock в `~/lireate-autopub/var/` |
| Нет формы логина в probe | Убедитесь, что `LIREATE_CMS_HTTP_BASE=http://127.0.0.1` |

Ручная публикация: загрузите картинки из `publish-bundle/images/` в `/template/images/blog/` и создайте новость в админке из `publish-bundle/article-body.html`.

## Безопасность

- Файл `.env` — только `chmod 600`.
- Не коммитьте пароли в репозиторий.
- `LIREATE_ALLOW_PUBLISH=no` оставляйте, пока тестируете `--dry-run`.
