# Lireate collage-v1 — контракт для шаблона lireate (devham13/lireate)

Обложки и inline-иллюстрации **новых** статей L* (не L01–L05) рендерятся детерминированно (`scripts/lireate_collage_*`).

## Маркеры в HTML статьи

### Главная обложка в теле (опционально, для превью в репо)

```html
<figure class="lx-article-cover" data-cover-style="collage-v1">
  <img src="cover/cover.png" alt="…" loading="eager" width="860" height="400">
</figure>
```

Шаблон на сайте: если в `article.meta.json` есть `"cover_style": "collage-v1"`, показывать **большое** изображение из `/template/images/blog/{seo_url}.jpg` в шапке материала вместо текстового hero (imgBlock). Дополнительно можно искать первый `<figure class="lx-article-cover" data-cover-style="collage-v1">` в `full_story`.

### Inline-иллюстрации

```html
<figure class="inline-collage" data-inline-style="collage-v1" data-template="bad_good|process|checklist">
  <img src="cover/inline-01.png" alt="…" loading="lazy" width="1200" height="675">
  <figcaption>…</figcaption>
</figure>
```

`data-template` — тип макета (a/b/c из спецификации).

## Meta JSON

В `article.meta.json` для новых статей:

| Поле | Значение |
|------|----------|
| `cover_style` | `"collage-v1"` |
| `cover_renderer` | `"html_chromium"` (опционально) |
| `cover_headline` | короткий hook 2–5 слов |
| `cover_highlight` | слово/фраза для розовой подсветки (опционально) |

Inline: файл `cover/inline-specs.json` (см. `memory/cover/collage-v1/inline-spec.schema.json`).

## Размеры файлов (совместимость с publish)

| Файл | Размер |
|------|--------|
| `cover/cover.png` | 860×400 |
| `cover/cover-small.png` | 350×163 |
| `cover/cover-preview-396x300.png` | 396×300 |
| `cover/inline-0N.png` | 1200×675 |

Пути и имена не меняются — `scripts/lireate_hosting_publish.py` / `lireate_hosting_images.py`.

## Layout QA (`layout_check.py`)

После Chromium-скриншота Playwright проверяет:

- запрещённые пересечения слотов (headline × sticky и т.д.);
- **safe-area:** каждый `[data-layout-slot]` внутри `[data-layout-paper]` с отступом **20px**;
- **cover:** зазор **≥16px** между `slot-arrow` и `slot-headline`;
- минимальные размеры шрифтов и плотность квадрантов.

## Fallback

`scripts/lireate_cover_kie.py` остаётся **только** если в meta `"cover_fallback": "kie"` и нет `cover_style: collage-v1`. Для L01–L05 и уже опубликованных папок collage-скрипты **не запускаются**.
