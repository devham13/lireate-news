# Lireate — автопубликация на REG.RU (хостинг)

Канон для владельца сайта: **`docs/lireate-autopub-hosting.ru.md`**

Кратко:

- Установка: `scripts/lireate_hosting_install.sh` → `~/lireate-autopub`
- Cron-скрипт: `scripts/lireate_hosting_publish.py`
- Проверка: `scripts/lireate_hosting_selfcheck.py`
- Облачный FTP/CMS (Cursor): `scripts/lireate_news_publish.py` + `shared/lireate-worker-setup.md`

Объединяет PR #1–#4: L01, REG.RU check, CMS HTTP, **hosting cron** (локальный docroot + `127.0.0.1` admin).
