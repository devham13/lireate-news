# Lireate — подключение REG.RU (единственный хостинг)

Репозиторий **lireate-news** в коде и документации использует только **REG.RU** (`LIREATE_*`).  
Скрипты этого репо **не читают** `FTP_*` / `SFTP_*` (BeGet и др.). Эти переменные могут оставаться в Cloud Secrets для других проектов — **удалять в Dashboard не нужно**.

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

## Другие секреты в Cloud (BeGet, WP, mayai)

В Dashboard могут одновременно лежать `FTP_*`, `SFTP_*`, `PUBLIC_SITE_URL`, `WP_*` — для **других** репозиториев или автоматизаций.  
Для **lireate-news** агент должен опираться только на `LIREATE_*`; пути и примеры BeGet в этом репозитории не используются.

Имена `LIREATE_SFTP_*` исторические: для REG.RU это **FTP по порту 21**, не SFTP.

## Автопубликация в /news

FTP выкладывает **картинки**; запись в рубрике (например `category_id=9`) — через **админку CMS** или **MySQL**.  
Чеклист секретов и варианты (админка, worker, БД): **`shared/lireate-autopublish-requirements.md`**.
