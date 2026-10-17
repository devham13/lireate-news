# Lireate.ru — production hosting (REG.RU)

Обновлено по фактам с live-сервера (не коммитить секреты).

| Параметр | Значение |
|----------|----------|
| Хостинг | `server324.hosting.reg.ru` |
| Shell/FTP user | `u3650956` |
| `HOME` | `/var/www/u3650956/data` |
| Autopub | `$HOME/lireate-autopub` |
| Docroot | `$HOME/www/public_html` → `/var/www/u3650956/data/www/public_html` |
| Python (записан в `.python-interpreter`) | `/opt/python/python-3.8.8/bin/python` (3.8.6) |
| Доступ с сервера | публичный HTTPS домен из `.env`; `http://127.0.0.1` — 404 без vhost |
| CMS | PHP admin + таблица `news`, `data/db.php` (mysqli) |
| Admin login | captcha — **HTTP-логин не используем** |
| Публикация | `scripts/lireate_db_publish.php` + `lireate_hosting_publish.py` |

Старый черновик с `u3249004` / `server176` — не актуален для live.
