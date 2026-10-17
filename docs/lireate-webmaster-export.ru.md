# Экспорт Яндекс.Вебмастера с хостинга lireate.ru

Данные собирает cron на **REG.RU** (`u3650956`), потому что с вашего ПК API `api.webmaster.yandex.net` может не открываться по TLS.

Файл на сервере: `$HOME/lireate-autopub/analytics/webmaster.json`  
Публичная выдача (только с секретным ключом): `https://ВАШ_ДОМЕН/lireate-analytics/webmaster.php` (как в `LIREATE_PUBLIC_SITE_URL`)

Скрипт: `scripts/lireate_hosting_webmaster_export.py` (Python 3.8, только stdlib).

---

## Шаг 1. Сгенерировать ключ и дописать `.env`

В **Shell ISPmanager** выполните **одну** команду (она покажет ключ — скопируйте и сохраните у себя, в чат не присылайте):

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub" && KEY="$(/opt/python/python-3.8.8/bin/python -c 'import secrets; print(secrets.token_urlsafe(32))')" && echo "Скопируйте ключ (один раз): $KEY" && touch "$LIREATE_AUTOPUB_HOME/.env" && grep -q '^YANDEX_WEBMASTER_TOKEN=' "$LIREATE_AUTOPUB_HOME/.env" || echo 'YANDEX_WEBMASTER_TOKEN=' >> "$LIREATE_AUTOPUB_HOME/.env" && grep -q '^LIREATE_ANALYTICS_KEY=' "$LIREATE_AUTOPUB_HOME/.env" || echo "LIREATE_ANALYTICS_KEY=$KEY" >> "$LIREATE_AUTOPUB_HOME/.env" && chmod 600 "$LIREATE_AUTOPUB_HOME/.env" && echo "Готово. Теперь откройте .env и вставьте OAuth-токен после YANDEX_WEBMASTER_TOKEN="
```

Откройте файл `.env` в файловом менеджере (`$HOME/lireate-autopub/.env`) и **вручную** вставьте токен Яндекса в строку `YANDEX_WEBMASTER_TOKEN=` (OAuth, права `webmaster:hostinfo` и `webmaster:verify`).

---

## Шаг 2. Обновить код репозитория

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub" && cd "$LIREATE_AUTOPUB_HOME/repo" && git pull origin main
```

Автодеплоя PHP на сайт **нет**: после `git pull` снова выполните `--deploy-php` (шаг 3).

---

## Шаг 3. Первый экспорт и PHP-эндпоинт

Шаблон **только** из git: `$LIREATE_AUTOPUB_HOME/repo/hosting/lireate-analytics/webmaster.php` (не копия в `$LIREATE_AUTOPUB_HOME/hosting/` вне `repo/`).

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub" LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env" && PY="$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" && "$PY" "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_webmaster_export.py" --deploy-php && ls -la "$LIREATE_AUTOPUB_HOME/analytics/webmaster.json"
```

Ожидаемо в конце: `STATUS: OK written=... host=https:lireate.ru:443 ...` и строки `deploy source repo: .../repo`, `deployed: ... (≈2500 bytes, mode 644)`.

Только переустановить PHP после `git pull` (без API):

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub" LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env" && PY="$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" && "$PY" "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_webmaster_export.py" --deploy-php-only
```

Проверка синтаксиса тем же PHP CLI, что для публикации (не обязательно совпадает с mod_php сайта, но ловит `declare(strict_types)`):

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub" LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env" && bash "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_webmaster_php_lint.sh"
```

---

## Шаг 4. Проверка JSON по HTTPS

Подставьте **тот же** ключ, что в `.env` (`LIREATE_ANALYTICS_KEY`), вместо `ВАШ_КЛЮЧ`:

```bash
curl -sS -H "X-Lireate-Key: ВАШ_КЛЮЧ" "${LIREATE_PUBLIC_SITE_URL%/}/lireate-analytics/webmaster.php" | head -c 400
```

Должен начаться с `{"generated_at":` (не `forbidden`).

Без заголовка должен быть ответ `403`.

---

## Шаг 5. CRON (каждый день 07:30 по Москве)

В панели хостинга → **Планировщик (cron)** добавьте **одну** строку:

```cron
TZ=Europe/Moscow
30 7 * * * $(cat $HOME/lireate-autopub/.python-interpreter) $HOME/lireate-autopub/repo/scripts/lireate_hosting_webmaster_export.py >> $HOME/lireate-autopub/logs/webmaster-export.log 2>&1
```

Лог: `$HOME/lireate-autopub/logs/webmaster-export.log`.

---

## Переменные `.env`

| Переменная | Назначение |
|------------|------------|
| `YANDEX_WEBMASTER_TOKEN` | OAuth-токен Вебмастера (не публиковать) |
| `LIREATE_ANALYTICS_KEY` | Секрет для заголовка `X-Lireate-Key` |
| `LIREATE_DOCROOT` | Нужен для `--deploy-php` / `--deploy-php-only` (`$HOME/www/public_html`) |
| `LIREATE_REPO_ROOT` | Опционально: путь к git checkout, если не `$LIREATE_AUTOPUB_HOME/repo` |

Скрипт **никогда** не выводит токен в stdout/логи.
