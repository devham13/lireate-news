# Быстрая индексация Lireate (после публикации)

Применять к агентам, которые доводят статью Lireate до **live** на lireate.ru (хостинг REG.RU, `lireate_hosting_publish.py`).

## Автоматика на хостинге

После `STATUS: PUBLISHED` cron уже вызывает:

- пересборку `sitemap.xml` из MySQL (`news`, read-only);
- IndexNow в Яндекс (`INDEXNOW_KEY` в `$HOME/lireate-autopub/.env`).

Агент **не** подменяет этот шаг ручными правками sitemap на FTP.

## Чеклист агента после публикации

1. **Sitemap** — в `lireate-publish-result.json` → `fast_indexing.sitemap.ok` = true; на сайте `{LIREATE_PUBLIC_SITE_URL}/sitemap.xml` отдаёт 200, URL новой статьи **со слэшем** и актуальный `lastmod`.
2. **IndexNow** — `fast_indexing.indexnow.http_status` в **200** или **202** (или `skipped`, если ключ ещё не настроен владельцем; тогда напомнить про `docs/lireate-indexnow-hosting.ru.md`).
3. **Страница** — live URL статьи: HTTP **200**.
4. **Canonical** — в HTML есть `<link rel="canonical" …>` на **тот же** URL **со слэшем** в конце.
5. **Лента** — статья видна в `/news/` (карточка в списке новостей).

## Запреты

- Не менять `data/db.php` ради индексации.
- Не ломать публикацию при ошибках IndexNow/sitemap (они только в логе).
- Не добавлять в sitemap чужие домены.

## Документация для владельца

`docs/lireate-indexnow-hosting.ru.md` — ключ, `.env`, `--deploy-indexnow-key`.  
`docs/proposals/robots.lireate.ru.txt` — предложение по robots.txt (ручное применение).
