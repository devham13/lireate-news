# Excalibur BLOG — Cover Agent (полный skill)

## Когда запускаться

После **GEO QA PASS**. Вход: `article.html`, `article.meta.json`, handoff `ready_for: excalibur-blog-cover`.

Параллельно с `excalibur-blog-schema`. **Не** править schema и body longread.

---

## Lireate NEWS (`site: lireate` / `lireate.ru`) — collage-v1 (новые L06+, не L01–L05)

**Переопределяет** quad/MCP/KIE для **новых** папок. Канон: `memory/blog/cover-collage-v1.md`, контракт шаблона: `shared/lireate-collage-v1-template-contract.md`.

```text
Writer/visual: cover/inline-specs.json (1–3 макета bad_good | process | checklist)
  → scripts/lireate_collage_pipeline.py --article-dir memory/blog/articles/Lxx-…
  → cover.png 860×400 + inline-01..03 + inject figures
  → meta cover_style: collage-v1
```

1. Задать `cover_headline`, `cover_highlight` (опционально), `cover/inline-specs.json`.
2. `python3 scripts/lireate_collage_pipeline.py --article-dir ...`
3. QA: `cover/cover-collage-qa.md`, превью 396×300, кириллица без опечаток.

**Не трогать** L01–L05 и каталоги с `kie-raw.png` без `cover_style: collage-v1`.

**Fallback KIE** (`memory/blog/cover-action-selfie.md`) только если в meta `"cover_fallback": "kie"` и нет collage-v1.

---

## Архитектура Excalibur (не Lireate)

```text
reference PNG → reference_url_hosted
       ↓
quad-manifest.json (agent fills hooks + scene_hint)
       ↓
quad-mcp-batch.json (1 job, input_urls)
       ↓
ONE MCP gpt-image-2 i2i → canvas-quad.png 2048×1152
       ↓
split → cover.png + inline-01..03.png (1200×675)
       ↓
inject <figure> after H2 in article.html
```

**Запрещено:** 4 отдельных MCP на cover + inline.

---

## Контракты и конфиги

| Путь | Назначение |
|------|------------|
| `shared/blog-cover-quad-canvas-contract.md` | канонический контракт |
| `agents/excalibur-blog-cover.md` | agent-md (этот skill дублирует runbook) |
| `memory/cover/blog-hero.json` | visual_lock, outfit_rule, reference_url_hosted |
| `memory/cover/assets/blog-hero-reference.png` | локальный эталон лица |
| `memory/cover/cover-design-code.json` | human hook collage, fake скрины, мемы |
| `memory/cover/quad-style-digital-meme-collage-ru.json` | style preset + design_code link |
| `memory/cover/inline-visual-types.json` | типы inline-панелей |
| `memory/brief/site-brief.md` | blog_hero_id, обложка = крючок |

---

## Панели quad 2×2

| Квадрант | Слот | Содержание |
|----------|------|------------|
| top-left | cover | hook + meme_caption_ru + **герой (reference face)** + design code |
| top-right | inline_1 | visual_type по H2 #1, **без героя** |
| bottom-left | inline_2 | visual_type по H2 #2 |
| bottom-right | inline_3 | visual_type по H2 #3 |

---

## Герой (blog-host)

**Lock (reference i2i):** героиня — молодая женщина, длинные волнистые чёрные волосы с прямой чёлкой, карие глаза; лицо строго с `memory/cover/assets/blog-hero-reference.png` (см. `blog-hero.json`).  
**Ретушь:** чистый ровный тон кожи, мягкий свет.  
**Мимика:** дружелюбная улыбка, экспертка по ИС.  
**Поза:** указывает на график, таблицу, скрин реестра или ключевую цифру на коллаже.  
**Одежда:** деловой образ юриста по ИС (пиджак, блуза) — **не** копировать casual outfit с reference-фото.  
**Inline-панели:** без лица героя (только top-left cover).

### Текст на обложке Excalibur (не Lireate)

- Для **Excalibur WP** — quad + при необходимости PIL (`lireate_cover_text_overlay.py` legacy).
- Для **Lireate** — текст на обложке **рисует kie** (см. блок выше).

---

## Design code — открываемость

Из `cover-design-code.json`:

1. Fake UI: Wordstat, Metrica, Telegram, отзывы ★☆☆☆☆
2. DIY: torn paper, scotch tape, pink sticky notes, marker arrows
3. Highlight: розовый маркер на ключевом слове hook
4. Memes: **разные** реакции (cat, facepalm…) — max 1 Drake на холст
5. Формат **16:9**, не Instagram carousel 9:16
6. Inline: полезный UI + лёгкий human layer (стикер, tape)

---

## Пошаговый runbook

### Шаг 0 — прочитать статью

- H2 (до FAQ): первые 3 → inline anchors
- lead, primary query → cover_hook
- `article.meta.json`: h1, topic_id

### Шаг 1 — reference URL

```bash
python scripts/excalibur_blog_hero_reference_url.py
```

Проверить `memory/cover/blog-hero.json` → `reference_url_hosted`.  
Fallback env: `BLOG_HERO_REFERENCE_URL`.

### Шаг 2 — manifest

```bash
python scripts/excalibur_blog_quad_manifest.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --merge
```

**Руками** доработать `cover/quad-manifest.json`:

- `cover_hook` — провокация
- `slots.cover.meme_caption_ru` — 2–6 слов
- `slots.cover.scene_hint` — fake скрины + мемы + outfit агента
- `slots.inline_*.scene_hint` — конкретика H2
- `alt` — осмысленные, не «seo картинка»

### Шаг 3 — prompt + batch

```bash
python scripts/excalibur_blog_cover_quad_prompt.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --write-batch
```

Проверить `cover/quad-mcp-batch.json`: **jobs.length === 1**, `input_urls` не пуст.

### Шаг 4 — ONE MCP

`CallMcpTool` → `user-mcp-kv` / `gpt-image-2`  
Аргументы = `jobs[0].mcp_args` из batch.

Ожидание: Image to Image, 1 входное фото, aspect 16:9, 2K.

### Шаг 5 — apply

```bash
python scripts/excalibur_blog_quad_apply.py \
  --article-dir memory/blog/articles/<topic_id>-<slug> \
  --url "<MCP result url>" \
  --inject-html
```

Требует Pillow. Выход: cover, inline PNG, registry, inject в article.html.

### Шаг 6 — fragment

`.cursor/excalibur-blog-fragments/cover.md` — шаблон в `agents/excalibur-blog-cover.md`.

---

## visual_type (inline)

| type | Когда |
|------|-------|
| `comparison_table_ui` | SEO vs GEO, сравнение |
| `workflow_diagram` | структура, шаги, longread |
| `checklist_board` | чеклист, публикация |
| `schema_faq_ui` | FAQ, schema, JSON-LD |
| `tool_screenshot` | Wordstat, инструменты |
| `infographic_card` | цифры, факты |

Keywords + автовыбор: `inline-visual-types.json` + `quad_manifest.py`.

---

## QA перед ✅

- [ ] 1 MCP, не 4
- [ ] input_urls в MCP
- [ ] cover.png + 3 inline существуют
- [ ] alt в registry для всех 4
- [ ] inline привязаны к H2 (`h2_anchor`)
- [ ] cover: hook + meme caption видны на PNG
- [ ] inline: без лица героя
- [ ] fragment cover.md записан

---

## Blockers → verdict ❌

- нет reference_url_hosted
- MCP text-only (без input_urls)
- 4 отдельные генерации
- QUAD SPLIT fail
- inline = meme с ведущим вместо UI

---

## Deprecated scripts

Не вызывать:

- `excalibur_blog_visual_prompts.py`
- `excalibur_blog_visual_apply.py`
- `excalibur_blog_visual_manifest.py`

См. `shared/blog-visual-pipeline-contract.md`.

---

## Эталон (B01)

`memory/blog/articles/B01-primer-seo-stati/cover/` — reference implementation после design code v1.
