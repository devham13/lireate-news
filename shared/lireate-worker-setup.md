# Lireate — self-hosted worker и автопубликация

Публикация **не работает из облака Cursor** (RCPC на `/admin/`, таймаут FTP data).  
Запускайте выкладку на **своём ПК или VPS** в worker pool **`lireate`**.

---

## Часть A. Один раз: Cursor Dashboard

### A1. Секреты (Cloud → Secrets)

Убедитесь, что заданы (значения только в Dashboard, не в git):

| Переменная | Пример / правило |
|------------|------------------|
| `LIREATE_PUBLIC_SITE_URL` | `https://…` ваш домен |
| `LIREATE_SFTP_HOST` | IP из ISPmanager «FTP-клиент» |
| `LIREATE_SFTP_PORT` | **`21`** |
| `LIREATE_SFTP_USER` / `LIREATE_SFTP_PASSWORD` | FTP |
| `LIREATE_REMOTE_SITE_ROOT` | каталог после login в FileZilla |
| `LIREATE_ALLOW_PUBLISH` | `yes` |
| `LIREATE_ADMIN_USER` / `LIREATE_ADMIN_PASSWORD` | вход в `/admin/` |

### A2. API-ключ для worker

1. Откройте [cursor.com](https://cursor.com) → войдите в аккаунт.
2. **Settings** (иконка профиля) → раздел **API Keys** / **Cloud**.
3. Создайте ключ → скопируйте (показывается один раз).  
   Это будет `CURSOR_API_KEY` на вашем компьютере.

### A3. Automation (после поднятия worker)

1. **Cursor** → **Automations** → **New automation**.
2. **Repository:** `devham13/lireate-news` (ваш fork).
3. **Branch:** `main` (или ветка с PR worker/CMS).
4. **Worker pool:** `lireate` (имя из шага B4).
5. **Schedule:** по желанию или **Manual**.
6. **Prompt** (минимум для публикации L01):

```text
Репозиторий lireate-news. Worker pool lireate.

1. python3 scripts/lireate_reg_ru_check.py — должен быть PASS.
2. python3 scripts/lireate_news_publish.py \
     --article-dir memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent

Если CMS config ещё не калиброван — сначала:
python3 scripts/lireate_cms_probe.py
(пользователь правит memory/lireate-cms-http-config.json)

Ответ: verdict из lireate-publish-result.json + live URL.
```

7. В настройках automation включите **передачу Secrets** в run (как в других ваших automations).

---

## Часть B. Один раз: компьютер worker (Windows / macOS / Linux)

Нужен ПК, с которого в браузере **открывается форма входа** `/admin/login.php` (не бесконечный RCPC).

### B1. Cursor CLI

- Установите **Cursor** на эту машину или CLI по [документации Cloud Agent setup](https://cursor.com/docs/cloud-agent/setup).
- В терминале должна работать команда `agent` (или путь из установки Cursor).

### B2. Клон репозитория

```bash
git clone https://github.com/devham13/lireate-news.git
cd lireate-news
git pull
```

### B3. Переменные в терминале (сессия worker)

**Windows PowerShell:**

```powershell
cd $HOME\lireate-news
$env:CURSOR_API_KEY = "ваш_ключ_из_A2"
$env:EXCALIBUR_PROJECT_ROOT = (Get-Location).Path
# Опционально: те же LIREATE_* локально, если automation не подставляет их в worker-run
```

**Linux / macOS:**

```bash
cd ~/lireate-news
export CURSOR_API_KEY="ваш_ключ_из_A2"
export EXCALIBUR_PROJECT_ROOT="$PWD"
```

### B4. Запуск worker pool

```bash
agent worker start --pool --pool-name lireate --idle-release-timeout 3600
```

Окно **не закрывайте**, пока нужна автоматизация. В Dashboard в списке workers должна появиться машина с pool **`lireate`**.

### B5. Проверка FTP с worker-машины

В **новом** терминале на той же машине (с теми же `LIREATE_*` в env или через automation secrets):

```bash
cd ~/lireate-news
python3 scripts/lireate_reg_ru_check.py
```

Ожидание: **`PASS`**, `port_effective: 21`.

---

## Часть C. Калибровка CMS (один раз на worker)

1. На worker-машине (секреты админки в env):

```bash
python3 scripts/lireate_cms_probe.py
```

2. Откройте папку `memory/lireate-cms-probe/` — HTML страниц админки.
3. Найдите форму **«создать / редактировать новость»** (поля title, текст, рубрика, alias).
4. Отредактируйте `memory/lireate-cms-http-config.json` (создаётся probe): блок **`news.fields`** — имена полей как в `<input name="…">`.
5. Шаблон: `shared/lireate-cms-http-config.json.example`.

Плейсхолдеры в значениях: `{title}`, `{h1}`, `{description}`, `{slug}`, `{alias}`, `{canonical_path}`, `{category_id}`, `{body_html}`.

---

## Часть D. Публикация статьи L01

На worker (вручную или через Automation из части A3):

```bash
python3 scripts/lireate_news_publish.py \
  --article-dir memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent
```

Успех: в `lireate-publish-result.json` → `"verdict": "published"`, URL **200**, строка в `shared/published-articles-lireate.md`.

Только CMS (картинки уже залиты):

```bash
python3 scripts/lireate_news_publish.py --cms-only --article-dir memory/blog/articles/L01-...
```

---

## Часть E. Что нажать вручную, если автоматика не прошла

1. **REG.RU ISPmanager** → сайт → **Менеджер файлов** → `template/images/blog/` → загрузить файлы из `publish-bundle/images/`.
2. Браузер → **`/admin/`** → логин → раздел **Блог / Новости**.
3. **Создать материал:** рубрика **Товарный знак** (`category_id=9`), ЧПУ из `article.meta.json`, тело из `publish-bundle/article-body.html`.
4. **Опубликовать** → проверить URL статьи и ленту `/news?num=2&category=9`.

---

## Быстрая диагностика

| Симптом | Действие |
|---------|----------|
| RCPC / нет формы логина | Запуск только с **worker**, не Cloud |
| FTP 530 | Пароль/порт **21** в Secrets |
| `news.create_path missing` | Запустить `lireate_cms_probe.py` |
| CMS OK, URL 404 | Неверные `news.fields` в config JSON |

См. также: `shared/lireate-autopublish-requirements.md`, `shared/lireate-news-publish-contract.md`.
