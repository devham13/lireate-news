# Быстрая индексация (sitemap + IndexNow) на REG.RU

После каждой успешной автопубликации скрипт `lireate_hosting_publish.py` **сам** обновляет `sitemap.xml` в корне сайта и отправляет URL в Яндекс через [IndexNow](https://yandex.com/support/webmaster/indexing-options/index-now.html). Ошибки индексации **не отменяют** публикацию статьи.

## Что нужно сделать владельцу (один раз)

### 1. Сгенерировать ключ

На своём компьютере или в Shell ISPmanager выполните:

```bash
openssl rand -hex 16
```

Скопируйте строку из **32** символов (латиница a–f и цифры) — это ваш `INDEXNOW_KEY`.

Пример (не используйте этот ключ в проде): `a1b2c3d4e5f6789012345678abcdef01`.

### 2. Добавить ключ в `.env` на хостинге

Откройте файл:

`$HOME/lireate-autopub/.env`

Добавьте строку (подставьте свой ключ):

```bash
INDEXNOW_KEY=ваш_ключ_из_32_символов
```

Сохраните файл. Переменные из этого `.env` читает cron и скрипт публикации.

### 3. Выложить файл проверки ключа в корень сайта

В Shell на хостинге (после `git pull` с веткой, где есть эта функция):

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
cd "$LIREATE_AUTOPUB_HOME/repo"
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  scripts/lireate_hosting_publish.py --deploy-indexnow-key
```

Успех: `STATUS: INDEXNOW_KEY_DEPLOYED` и путь к файлу вида  
`$LIREATE_DOCROOT/<ваш_ключ>.txt`.

Проверка в браузере: URL из `LIREATE_PUBLIC_SITE_URL` + `/<ваш_ключ>.txt` — внутри только ключ, без лишнего текста.

### 4. (Рекомендуется) Обновить robots.txt

Черновик исправленного `robots.txt` — в репозитории:  
`docs/proposals/robots.lireate.ru.txt` (вручную через «Менеджер файлов» ISPmanager, **не** через автопубликацию).

## Что происходит при каждой публикации

1. Статья попадает в MySQL и отдаётся с сайта (как раньше).
2. Из таблицы `news` (только чтение) собирается новый `public_html/sitemap.xml`: только URL **lireate.ru**, у статей — **со слэшем** в конце, `lastmod` — дата из БД; отдельно `/news/`.
3. POST на `https://yandex.com/indexnow` с URL статьи и `sitemap.xml`. В логе: `fast_indexing: IndexNow HTTP 200` или `202`.

Лог: `$HOME/lireate-autopub/logs/publish.log`. Детали также в `lireate-publish-result.json` → поле `fast_indexing`.

## Если IndexNow не настроен

Без `INDEXNOW_KEY` публикация работает как раньше; sitemap всё равно пересобирается. В логе будет: `IndexNow skipped (INDEXNOW_KEY not set)`.
