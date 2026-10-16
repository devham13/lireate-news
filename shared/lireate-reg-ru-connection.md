# Lireate — подключение REG.RU (единственный хостинг)

Репозиторий **lireate-news** работает только с **REG.RU** (`lireate.ru`).  
**Не** подключать и **не** документировать здесь учётки **BeGet**, `FTP_*`, `SFTP_*` для других сайтов.

## Cloud Secrets (обязательно)

| Переменная | Комментарий |
|------------|-------------|
| `LIREATE_SFTP_HOST` | Адрес из панели «FTP-клиент», **не** A-запись сайта |
| `LIREATE_SFTP_PORT` | `21` (FTP). Не `22`, если в панели только FTP |
| `LIREATE_SFTP_USER` | Учётная запись FTP из ISPmanager |
| `LIREATE_SFTP_PASSWORD` | Пароль FTP (секрет) |
| `LIREATE_REMOTE_SITE_ROOT` | Путь после `CWD` от корня FTP-сессии |
| `LIREATE_PUBLIC_SITE_URL` | Публичный URL сайта |
| `LIREATE_ALLOW_PUBLISH` | `yes` / `no` — разрешение выкладки |

Панель REG.RU: раздел ISPmanager → сайт → настройки FTP.

## Проверка из репозитория

```bash
python3 scripts/lireate_reg_ru_check.py
```

## Что удалить из Cloud Secrets для этого репо

Если остались от старого Excalibur/BeGet — **уберите**, чтобы агент не путал хостинги:

- `FTP_HOST`, `FTP_USER`, `FTP_PASSWORD`, `FTP_PORT`
- `SFTP_HOST`, `SFTP_USER`, `SFTP_PASSWORD`
- `PUBLIC_SITE_URL` / `WP_*` для **mayai.ru** (другой проект)

Имена `LIREATE_SFTP_*` исторические: для REG.RU это **FTP по порту 21**, не SFTP.
