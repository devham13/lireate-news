# Excalibur BLOG Cloud Instructions

> ## ⛔ Lireate: правило очереди тем (обязательно, приоритет над всем ниже)
> 1. Первым шагом: `python3 scripts/excalibur_blog_today.py` (или `python3 scripts/lireate_topic_queue.py`).
> 2. Тема = первая карточка `## Lxx` в `memory/topics/blog-topics.md` со `status: new`, у которой **нет** папки `memory/blog/articles/Lxx-*`.
> 3. Если скрипт печатает `NO_NEW_TOPIC` — **стоп**: не писать статью, не обновлять старую, не создавать ветку/PR. В ответе только `NO_NEW_TOPIC`.
> 4. **Никогда не переписывать существующую статью** (L01 и любые папки в `memory/blog/articles/`). `LIREATE_TOPIC_ID`/`EXCALIBUR_TOPIC_ID`, указывающий на существующую папку, игнорируется.
> 5. После написания статьи поставить в её карточке `status: written` (в том же PR). `published` ставит **CRON на хостинге** после успешного INSERT (не Cloud Agent).
> 6. Публикация на хостинге: `lireate_hosting_publish.py` без `--article-dir` берёт только самую новую неопубликованную папку L*; если нет — `NO_NEW_ARTICLE`, exit 0, без `--update`.
> 7. **Auto-merge PR:** после PASS всех проверок репозитория (lint, SEO, GEO QA / fact-check, обложка с читаемыми русскими подписями через PIL-оверлей) — открыть **готовый** (не draft) PR в `main` и **самостоятельно смержить**, когда CI зелёный. Не ждать ручного одобрения владельца. Любой FAIL — PR **не** мержить, на хостинг ничего не уходит.
> 8. После merge в `main` live-публикацию выполняет **CRON REG.RU** (`lireate_hosting_cron.sh`), не Cloud Agent.


Язык работы: русский.

## Главное правило

Для полной SEO/GEO статьи **нельзя** выполнять весь пайплайн одним Cloud Agent.

Cloud Agent обязан оркестрировать через **Директора** (роль в чате, не Task) и запускать субагентов:

```text
shell today + research_start
  → excalibur-blog-research
  → excalibur-blog-writer
  → excalibur-blog-geo-qa
  → excalibur-blog-cover || excalibur-blog-schema
  → excalibur-blog-indexer
  → excalibur-blog-publish (автоматически после Indexer; skip только publish:no)
```

## Cloud Task fallback

Если Cloud API не принимает `excalibur-blog-research`, `excalibur-blog-writer`, … как Task types:

- **отдельный `Task(generalPurpose)` на каждую роль**;
- передай путь `.cursor/agents/<role>.md` и `.cursor/skills/<skill>/SKILL.md`;
- короткий контракт: входные файлы, маркер результата, запреты;
- один Task = одна роль;
- параллель `cover || schema` — **два отдельных Task** в одном сообщении.

Если недоступен даже `generalPurpose` Task:

`❌ БЛОКЕР: Cloud Agent не может запускать отдельные Task/subagents даже через generalPurpose. Single-agent pipeline запрещён.`

## Что считать ошибкой

- Parent сам пишет `article.html` вместо Task writer.
- Parent сам делает cover/schema вместо параллельных Task.
- Parent запускает cover||schema **до** GEO QA PASS.
- Publish без обновления `shared/published-articles.md`.

## Handoff и fragments

- Handoff: `.cursor/excalibur-blog-handoff.md`
- Параллельные роли (cover, schema) пишут во фрагменты:
  - `.cursor/excalibur-blog-fragments/cover.md`
  - `.cursor/excalibur-blog-fragments/schema.md`
- Директор переносит фрагменты в handoff.

Маркеры:

- `=== EXCALIBUR BLOG RESEARCH ===`
- `=== EXCALIBUR BLOG WRITER ===`
- `=== EXCALIBUR BLOG GEO QA ===`
- `=== EXCALIBUR BLOG COVER ===`
- `=== EXCALIBUR BLOG SCHEMA ===`
- `=== EXCALIBUR BLOG INDEXER ===`
- `=== EXCALIBUR BLOG PUBLISH ===`
- `=== EXCALIBUR BLOG (PIPELINE DONE) ===`

## Канонические пути

`<PROJECT_ROOT>` — корень репозитория (без `C:\Users\...`).

| Артефакт | Путь |
|----------|------|
| Плагин / контракты | `agents/`, `skills/`, `shared/`, `scripts/` |
| Runtime memory | `memory/` |
| Журнал публикаций | `shared/published-articles.md` |
| Cloud agents | `.cursor/agents/` |
| Cloud skills | `.cursor/skills/` |

Перед пайплайном прочитай `shared/agent-pipeline-pitfalls.md`.

## Preflight (обязательно)

```bash
python3 scripts/excalibur_blog_today.py
python3 scripts/excalibur_blog_research_start.py --topic-id B01
```

Используй `EXCALIBUR_RUN_DATE`, `EXCALIBUR_SUGGESTED_TOPIC_ID` из today.py.
Если `python` недоступен — `python3`.

## Секреты

Только Cloud Secrets / env vars. Не печатать FTP/API ключи в handoff, PR, ответах.

**lireate-news — только REG.RU в репо:** `LIREATE_SFTP_*`, `LIREATE_REMOTE_SITE_ROOT`, `LIREATE_PUBLIC_SITE_URL`, `LIREATE_ALLOW_PUBLISH`.  
Код и доки этого репозитория **не используют** `FTP_*` / `SFTP_*`; в Cloud Secrets их можно не трогать. См. `shared/lireate-reg-ru-connection.md`.

Проверка FTP: `python3 scripts/lireate_reg_ru_check.py`

- MCP через `${env:...}` в mcp.json

## Git hygiene

**Не коммитить:** `.cursor/excalibur-blog-handoff.md`, `shared/excalibur-blog-handoff.md`, `.cursor/excalibur-blog-fragments/`, `memory/site.env.local`, абсолютные пути Windows/macOS в отчётах.

**Коммитить после publish:** `shared/published-articles.md`, при необходимости артефакты статьи в `memory/blog/`.

## Субагенты (.cursor/agents)

| name | skill |
|------|-------|
| excalibur-blog-research | excalibur-research |
| excalibur-blog-writer | writer-excalibur-blog |
| excalibur-blog-geo-qa | excalibur-geo-qa |
| excalibur-blog-cover | cover-excalibur-blog |
| excalibur-blog-schema | schema-excalibur-blog |
| excalibur-blog-indexer | indexer-excalibur-blog |
| excalibur-blog-publish | excalibur-wp-publish |

Директор: `.cursor/agents/excalibur-blog-director.md` + `director-excalibur-blog` skill — **не Task**.

Полная настройка worker/automation: `CLOUD-AUTOMATION.md`.
