# Lireate NEWS: collage-v1 cover + inline (2026-10-19)

**Канал для новых статей L07+** (не L01–L06): детерминированный HTML/CSS + Chromium. L06 — legacy KIE на live; не перегенерировать без `--update` на хостинге.

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

**KIE** (`lireate_cover_kie.py`) — **запрещён** для L07+; только legacy L01–L06.

Перед merge/publish: `python3 scripts/lireate_collage_publish_gate.py --article-dir …` (или `--all-lireate` в CI).

Контракт для шаблона сайта: `shared/lireate-collage-v1-template-contract.md`.
