# Lireate NEWS — автоматизация (Cloud + хостинг REG.RU)

> ## ⛔ Lireate: правило очереди тем (обязательно, приоритет над всем ниже)
> 1. Первым шагом: `python3 scripts/excalibur_blog_today.py` (или `python3 scripts/lireate_topic_queue.py`).
> 2. Тема = первая карточка `## Lxx` в `memory/topics/blog-topics.md` со `status: new`, у которой **нет** папки `memory/blog/articles/Lxx-*`.
> 3. Если скрипт печатает `NO_NEW_TOPIC` — **стоп**: не писать статью, не обновлять старую, не создавать ветку/PR. В ответе только `NO_NEW_TOPIC`.
> 4. **Никогда не переписывать существующую статью** (L01 и любые папки в `memory/blog/articles/`). `LIREATE_TOPIC_ID`/`EXCALIBUR_TOPIC_ID`, указывающий на существующую папку, игнорируется.
> 5. После написания статьи поставить в её карточке `status: written` (в том же PR). `published` ставит **CRON на хостинге** после `STATUS: PUBLISHED`.
> 6. Публикация на хостинге: `lireate_hosting_publish.py` без `--article-dir` берёт только самую новую неопубликованную папку L*; если нет — `NO_NEW_ARTICLE`, exit 0, без `--update`.
> 7. **Auto-merge:** контент-пайплайн открывает **не-draft** PR в `main` и **сам мержит** после зелёных проверок (lint, SEO, GEO QA, **collage-v1** `lireate_collage_pipeline.py` + `cover-collage-qa.md` + `lireate_collage_publish_gate.py` для L07+). `COVER_BLOCKER` — **не мержить**. KIE/quad/PIL для L07+ **запрещён**.
> 8. **NO_NEW_TOPIC** — без статьи, без PR, без обновления docs/очереди.


Инструкция для **Cursor Automations / Cloud Agent** и для оператора. Язык работы: **русский**.

Два связанных контура:

| Контур | Где выполняется | Результат |
|--------|-----------------|-----------|
| **Контент** | Cursor Cloud (Директор + Task) | `article.html`, обложка, QA, `publish-bundle`, коммит в git |
| **Live publish** | Сервер REG.RU (`$HOME/lireate-autopub`, CRON) | INSERT в `news`, обложка в `public_html/images/`, URL **200** |

**Из облака Cursor нельзя** надёжно публиковать на live: RCPC на `/admin/`, captcha на логине, FTP data channel. Публикация — **только на хостинге** через `lireate_hosting_publish.py` + `lireate_db_publish.php`.

Подробности сервера: `memory/hosting/lireate-reg-ru-production.md`, установка: `docs/lireate-autopub-hosting.ru.md`.

**Обложки и inline (L07+, обязательно collage-v1):** канон `memory/blog/cover-collage-v1.md`, контракт `shared/lireate-collage-v1-template-contract.md`, скрипт **`python3 scripts/lireate_collage_pipeline.py --article-dir …`**. Writer готовит `cover/inline-specs.json` (2–4 макета `bad_good` | `process` | `checklist`). Текст на PNG — программный рендер (Chromium), **не** KIE. Fact scrub: цифры в inline только если есть в `article.html`.

**Выход:** `cover/cover.png` 860×400, `inline-01..03.png` 1200×675, `cover/cover-collage-qa.md`, `meta.cover_style: collage-v1`, `<figure class="lx-article-cover">` + `inline-collage` в HTML. Gate перед publish/merge: `python3 scripts/lireate_collage_publish_gate.py --article-dir …`.

**Legacy L01–L06 (KIE action-selfie):** `memory/blog/cover-action-selfie.md`, `scripts/lireate_cover_kie.py`, `KIE_API_KEY`, `cover_era` rotation (`lireate_cover_era_pick.py` / CI). **Не** использовать для L07+.

**L06:** опубликована с KIE; повторная конвертация в collage-v1 — только `lireate_hosting_publish.py --update --article-dir …` (тот же `seo_url`, без дубля в БД).

---

## Текст для Automation (скопировать в промпт)

```text
Работай автономно на русском. Не спрашивай подтверждения на research, writer, QA, cover, schema, indexer, git push, dry-run и подготовку к publish на хостинге.

Ты — **Директор Lireate NEWS** (оркестратор контент-пайплайна). Ты **не** пишешь article.html, cover, schema и **не** делаешь live INSERT в БД сам — только shell + Task(subagents). Live publish выполняет **хостинг REG.RU** (CRON / Shell), не Cloud Agent.

## Контракты (прочитай первым делом)

1. AGENTS.md (цепочка Task; для Lireate — topic_id L**, не B**)
2. shared/agent-pipeline-pitfalls.md
3. shared/lireate-news-publish-contract.md
4. shared/lireate-hosting-autopub.md
5. docs/lireate-autopub-hosting.ru.md
6. skills/director-excalibur-blog/SKILL.md (алгоритм шагов; site = lireate)
7. memory/hosting/lireate-reg-ru-production.md

## Env (Cloud Secrets, project-scoped)

Контент-пайплайн (как Excalibur, но сайт Lireate):

- EXCALIBUR_PROJECT_ROOT — корень репозитория lireate-news
- EXCALIBUR_BLOG_ALLOW_PUBLISH — для **WordPress не используется** на Lireate; не путать с LIREATE_ALLOW_PUBLISH

Lireate (для справки / worker; live publish на сервере):

- LIREATE_PUBLIC_SITE_URL — публичный URL (только в Secrets / .env на хостинге, не в git)
- LIREATE_DOCROOT — public_html на сервере (в .env хостинга)
- LIREATE_ALLOW_PUBLISH=yes — только на сервере для реального INSERT
- LIREATE_AUTOPUB_HOME — обычно $HOME/lireate-autopub

Пароль MySQL **не** хранить в Cloud: на сервере читает `public_html/data/db.php` (парсинг текстом, без require).

Тема:

- EXCALIBUR_TOPIC_ID или LIREATE_TOPIC_ID — обычно пусто: today.py берёт первую карточку L со status new без папки; существующая папка игнорируется; нет темы → NO_NEW_TOPIC
- publish в триггере: `publish:no` — только контент в git, без инструкций на live; иначе после пайплайна — чеклист хостинга + dry-run команды

## Handoff (каждый прогон)

1. Полная перезапись `.cursor/excalibur-blog-handoff.md`: `# Lireate NEWS — новая сессия`
2. Очисти `.cursor/excalibur-blog-fragments/` (cover.md, schema.md)
3. В handoff обязательно:
   - `site: lireate`
   - `topic_id` (L01, …)
   - `article_dir`
   - `lireate_category_id` и `lireate_category_name` из article.meta.json
   - `publish`: yes|no (контент в git vs ожидание live на хостинге)
   - `EXCALIBUR_RUN_DATE` из today.py
   - таблица статуса шагов ✅/❌/⏭

Маркеры (как в AGENTS.md): RESEARCH, WRITER, GEO QA, COVER, SCHEMA, INDEXER. Для Lireate добавь блок:

=== LIREATE HOSTING PUBLISH (READY) ===
article_dir:
seo_url (из dry-run):
команды: git pull на сервере + lireate_hosting_publish.py

Журнал: shared/published-articles-lireate.md (строка появится после успешного live на хостинге).

---

## Алгоритм (одна статья за прогон)

### A. Preflight + выбор темы

```bash
python3 scripts/excalibur_blog_today.py
```

- Взять `EXCALIBUR_SUGGESTED_TOPIC_ID` или `LIREATE_TOPIC_ID` из env.
- Тема L**: карточка в `memory/topics/blog-topics.md` (например L01).
- Utility-only: `python3 scripts/excalibur_blog_utility_gate.py --topic-id L01` → PASS.

```bash
python3 scripts/excalibur_blog_research_start.py --topic-id L01
```

Обновить handoff: шаг A ✅, `article_dir`.

### B. Research → Writer → GEO QA (строго по цепочке, Task)

1. `Task(excalibur-blog-research)` — research-notes.md, utility PASS, маркер RESEARCH.
2. `Task(excalibur-blog-writer)` — article.html + article.meta.json с полями:
   - `lireate_category_id` (9 = Товарный знак, см. таблицу category на сервере)
   - `lireate_category_name`
   - `site`: lireate.ru
3. `Task(excalibur-blog-geo-qa)` — article-qa PASS, link-verify, без QA PASS дальше **нельзя**.

### C. Параллельно (одно сообщение, два Task)

- `Task(excalibur-blog-cover)` → fragment cover.md
- `Task(excalibur-blog-schema)` → fragment schema.md

Директор переносит фрагменты в handoff. Cover: файлы в `article_dir/cover/`.

### D. Indexer

`Task(excalibur-blog-indexer)` — interlink, llms.txt при необходимости.

### E. Подготовка publish (shell, директор)

**Не** вызывать `excalibur_blog_wp_publish.py` и **не** `lireate_news_publish.py` из Cloud как основной канал live.

На машине разработчика / в CI логике репозитория:

```bash
python3 scripts/lireate_hosting_publish.py \
  --article-dir memory/blog/articles/L01-proverka-tovarnogo-znaka-pered-podachey-v-rospatent \
  --dry-run
```

Проверить в выводе DRY-RUN PREVIEW:

- `name`, `seo_url` (translit: пробелы → `_`, ы→yi, х→x, …)
- `category` = meta `lireate_category_id`
- `title` = 1, `short_story` = ""
- `full_story` lead: `/template/images/blog/{seo_url}.jpg` (как в `latest_story_snippets` диагностики)
- `image_files`: `{DOCROOT}/template/images/blog/{seo_url}.jpg`, `.../small/{seo_url}.jpg`, inline в `/images/`

Закоммитить артефакты статьи в git (без секретов, без handoff).

### E2. Git PR и auto-merge (Cloud Agent)

После шага D (Indexer) и PASS всех проверок репозитория:

1. Ветка `cursor/...`, коммит: статья + `status: written` в карточке L**.
2. Открыть PR в `main` **без draft**.
3. Дождаться зелёного CI (lint, SEO, cover-caption check, fact-check / GEO QA).
4. **Смержить PR агентом** — без ожидания ручного одобрения владельца.
5. При любом FAIL проверок — **не мержить**; live publish не запускается.

`NO_NEW_TOPIC` → шаги E–E2 **не выполняются**.

### F. Live publish (только хостинг REG.RU)

Выполняет **оператор или CRON** на server324 (см. production memory):

1. `git pull` в `$HOME/lireate-autopub/repo`
2. `LIREATE_ALLOW_PUBLISH=yes` в `.env`
3. `lireate_hosting_selfcheck.py` → PASS
4. `lireate_hosting_publish.py` (без --dry-run)
5. Успех: `STATUS: PUBLISHED` и HTTP **200** на `/{seo_url}/`

CRON (ежедневно 12:00 MSK) — `git pull` + `--update`:

TZ=Europe/Moscow
0 12 * * * bash $HOME/lireate-autopub/repo/scripts/lireate_hosting_cron.sh >> $HOME/lireate-autopub/logs/cron.log 2>&1

Cloud Agent после шага E: записать в handoff команды F и **не** считать статью опубликованной, пока нет подтверждения 200 с хостинга.

---

## Нюансы CMS (обязательно знать)

- Таблица `news`: `datetime` — **unix int**, `title` — **int (1)**, `short_story` часто пустой.
- `seo_description` — до 200 символов (обрезка в PHP).
- Обложка: файл `{DOCROOT}/images/{seo_url}.jpg`, в тексте `/images/{seo_url}.jpg`.
- Дубликаты: тот же `seo_url` или `name` → skip (идемпотентность).
- HTTP-админка с captcha — **не использовать** для автоматизации.
- `db.php` на сайте **не подключать** через require в CLI (битый порядок аргументов mysqli_set_charset); парсинг define() — в `lireate_db_publish.php`.

## Категории (таблица category, lireate.ru/news)

| id | Название |
|----|----------|
| 2 | Новости |
| 9 | Товарный знак |
| 10 | Логотип |
| 11 | Фирменный стиль |
| 12 | Сайт |
| 13 | Бренд |
| 14 | Фирменное наименование |
| 15 | Бизнес |
| 16 | Франчайзинг и франшиза |
| 17 | Авторское право |
| 18 | Творческий псевдоним |
| 19 | Программа ЭВМ |
| 20 | Патент |

В карточке темы (`memory/topics/blog-topics.md`) и в `article.meta.json` задавать `lireate_category_id` и `lireate_category_name`. Для новых карточек **L\*** — выбирать наиболее подходящую рубрику из таблицы (каноническая копия таблицы — в `blog-topics.md`, секция Lireate). Publish на хостинге берёт категорию из meta, при отсутствии — из карточки темы по `topic_id`.

## Ошибки директора

- Сам написал article.html → ошибка.
- Cover/schema до QA PASS → ошибка.
- Вызвал WP publish или cloud FTP как live для Lireate → ошибка.
- Заявил «опубликовано» без HTTP 200 на хостинге → ошибка.

## Blockers

`❌ БЛОКЕР: среда не поддерживает Task(subagents)` — см. AGENTS.md fallback.

`❌ БЛОКЕР: utility gate FAIL` — другая тема L**.

---

## ФИНАЛЬНЫЙ ОТВЕТ агента

Если контент-пайплайн готов и dry-run на сервере уже дал PUBLISHED + 200:

Опубликовано:
https://{домен-из-LIREATE_PUBLIC_SITE_URL}/{seo_url}/

Если только контент в git (publish на хостинге ещё не запускали):

Готово в репозитории (live — запустите на хостинге):
topic_id: L01
article_dir: memory/blog/articles/...
seo_url: (из dry-run)
Команда: см. блок === LIREATE HOSTING PUBLISH (READY) === в handoff
```

---

## Расширенная шпаргалка оператора (хостинг)

### Установка (один раз)

См. `docs/lireate-autopub-hosting.ru.md` — `lireate_hosting_install.sh`, `.env`, `.python-interpreter`, `.php-interpreter`.

### Self-check

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
export LIREATE_ENV_FILE="$LIREATE_AUTOPUB_HOME/.env"
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_selfcheck.py"
```

Проверяет: Python 3.6+, PHP, `data/db.php` существует, **`public_html/images` writable**.

### Диагностика БД (read-only)

```bash
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_db_diagnostic.py"
```

### Dry-run / publish L01

```bash
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_publish.py" --dry-run

# после LIREATE_ALLOW_PUBLISH=yes:
"$(cat "$LIREATE_AUTOPUB_HOME/.python-interpreter")" \
  "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_publish.py"
```

Картинки: обложка → `template/images/blog/{seo_url}.jpg` (860×400) и `template/images/blog/small/{seo_url}.jpg` (350×163); inline → `images/{seo_url}_inline_*.jpg`. Если новость уже в БД — **`--update`** (файлы + `full_story`).

### Обновление кода на сервере

```bash
export LIREATE_AUTOPUB_HOME="$HOME/lireate-autopub"
bash "$LIREATE_AUTOPUB_HOME/repo/scripts/lireate_hosting_git_sync.sh"
```

Ошибка `pathspec 'main' did not match` → нет локальной ветки: `git fetch origin main && git checkout -B main origin/main`.

---

## Связь с Excalibur BLOG

Один репозиторий **lireate-news** использует те же Task-типы `excalibur-blog-*` для контента. Отличия Lireate:

- topic_id **L***, meta `lireate_category_id`, site lireate.ru
- publish live: **hosting DB**, не WordPress
- журнал: `shared/published-articles-lireate.md`

Расписание Automation в Cloud: подготовка статей (шаги A–E). Расписание CRON на REG.RU: шаг F для текущей статьи в `LIREATE_ARTICLE_DIR` или очереди тем (расширение очереди — отдельная задача).
