# Lireate NEWS: collage-v1 cover + inline (2026-10-19)

**Канал для новых статей L06+** (не L01–L05): детерминированный HTML/CSS + Chromium.

```text
derive spec from article.meta.json (+ cover/inline-specs.json)
  → scripts/lireate_collage_pipeline.py
  → cover.png 860×400 + inline-01..03.png 1200×675
  → inject lx-article-cover + inline-collage figures
```

Скрипты:

| Скрипт | Назначение |
|--------|------------|
| `lireate_cover_collage.py` | обложка списка |
| `lireate_inline_collage.py` | иллюстрации по `inline-specs.json` |
| `lireate_collage_inject.py` | figure в `article.html` |
| `lireate_collage_pipeline.py` | всё вместе |
| `lireate_collage_samples.py` | артефакты для QA |

**KIE** (`lireate_cover_kie.py`) — только fallback при `"cover_fallback": "kie"` и без `cover_style: collage-v1`.

Контракт для шаблона сайта: `shared/lireate-collage-v1-template-contract.md`.
