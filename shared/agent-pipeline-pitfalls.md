# Excalibur BLOG — типичные сбои пайплайна

## Cloud / Task

- Cloud не принимает `excalibur-blog-*` как Task types → fallback `Task(generalPurpose)` + `.cursor/agents/<role>.md` + skill path.
- Parent-agent сам пишет статью вместо `excalibur-blog-writer` → **блокер**, перезапуск writer Task.
- Объединение cover+schema в один Task → запрещено; только параллельные отдельные Task.

## Handoff / fragments

- Параллельные `cover` и `schema` пишут в `.cursor/excalibur-blog-fragments/cover.md` и `schema.md`, директор переносит в handoff.
- Не коммитить `.cursor/excalibur-blog-handoff.md` и fragments.

## Research / дата

- Перед пайплайном: `python3 scripts/excalibur_blog_today.py` и `python3 scripts/excalibur_blog_research_start.py --topic-id …`.
- Если `EXCALIBUR_RUN_DATE` нет в выводе today.py — старая ветка/код, **блокер**.

## Publish

- `EXCALIBUR_BLOG_ALLOW_PUBLISH=yes` только в Cloud Secrets, не в git.
- Publish без обновления `shared/published-articles.md` → следующий прогон может дублировать slug.

## Lireate (REG.RU)

- Cloud готовит контент в **git**; live INSERT только на хостинге (`lireate_hosting_publish.py`).
- PR не в `main` (не смержен) → CRON на сервере не видит новые `article.html`. Lireate: агент **сам мержит** готовый PR после зелёного CI; draft PR не использовать.
- Lireate cover: только `lireate_cover_kie.py` + `KIE_API_KEY`. `COVER_BLOCKER` → не мержить; PIL/quad fallback запрещён. `cover_era` не повторять в окне 10 статей.
- После первой публикации URL даёт **200** → обычный cron выходит `ALREADY_PUBLISHED` без обновления текста. Нужны `git pull` + `--update` (см. `scripts/lireate_hosting_cron.sh`).
- Повторные прогоны по той же L01 не создают вторую новость (тот же `seo_url`).

## QA

- Шаг cover||schema **только после** GEO QA PASS.
- MCP URLs в production article.html → fix перед publish.
