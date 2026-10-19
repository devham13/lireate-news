# LIREATE article cover: action selfie (mandatory, 2026-10-18)

**Новые статьи (L07+, не L01–L06):** обложка и inline — **только collage-v1** (`memory/blog/cover-collage-v1.md`, `scripts/lireate_collage_pipeline.py`). Gate: `lireate_collage_publish_gate.py`.

**Legacy (L01–L06):** kie.ai **nano-banana-2** (`scripts/lireate_cover_kie.py`). L07+ → скрипт завершается `COVER_BLOCKER`.

**Нет fallback** на PIL/quad/MCP для Lireate NEWS.

Эталон результата (владелец): steampunk-era selfie, крупный белый заголовок сверху, @LIREATE внизу — см. sample у оператора (не в git).

## API

| Шаг | Метод |
|-----|--------|
| Создать задачу | `POST https://api.kie.ai/api/v1/jobs/createTask` |
| Статус | `GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=` |
| Auth | `Authorization: Bearer $KIE_API_KEY` (Cloud Secret / `.env`, **не** в git) |
| Загрузка face ref (опц.) | `POST https://kieai.redpandaai.co/api/file-stream-upload` (form: `file`, `uploadPath`, `fileName`) → `downloadUrl` |

Тело createTask:

```json
{
  "model": "nano-banana-2",
  "input": {
    "prompt": "<filled from template below>",
    "image_input": ["<face_ref_url>"],
    "aspect_ratio": "16:9",
    "resolution": "2K",
    "output_format": "png"
  }
}
```

Face reference (по умолчанию):  
`http://lyratetrademark.ru/wp-content/uploads/2025/12/photo_2025-12-24_12-17-06.jpg`  
Локальная копия лица: `memory/cover/assets/blog-hero-reference.png`

Style samples (владелец):  
https://mayai.ru/wp-content/uploads/2025/11/c410cce6a3fa9f9d28915004e46e1c57.jpg  
https://mayai.ru/wp-content/uploads/2025/11/3557247553f3360809d41bb5c4ae311c.jpg

## Ротация эпох

В `article.meta.json` поле **`cover_era`** (строка из списка ниже).  
**Не повторять эпоху** среди **последних 10** L-статей.  
Проверка: `python3 scripts/lireate_cover_era_check.py --all-lireate`  
Подбор: `python3 scripts/lireate_cover_era_pick.py --topic-id Lxx --write-meta article.meta.json`

## Промпт (подставить THEME, ERA, HEADLINE)

```
Main Objective: Create a HYPER-REALISTIC ACTION SELFIE photo cover for an article.
Theme: {{THEME}}

STRICT VISUAL STYLE:
A photorealistic wide-angle selfie shot of the main hero (from reference), blending seamlessly with historical events/personalities based on the theme.
Captured with a 24mm wide-angle lens (simulating high-end smartphone or wide POV camera) to capture both the hero's face and the dynamic historical background.
The image must look like a real, candid moment captured in time, NOT an illustration.

SUBJECT & COMPOSITION:
The main hero young woman (from first reference image), making a funny/cool expression reacting to the historical event behind her.
- Clothing: Era-accurate costume blended with modern stylish elements.
- Face: Ultra-sharp focus on the hero's face. Visible skin pores, realistic eye reflections. IDENTITY LOCK: exactly the same person as the reference (face shape, eyes, brows, nose, lips, cheekbones, skin tone, long black hair with thick straight bangs).
- Glasses: Stylish eyewear reflecting the scene (accurate optical reflections).
- NO cap, NO hood.

ENVIRONMENT & CONTEXT (from theme + chosen era):
The background depicts a vivid, chaotic, or humorous historical scene relevant to: {{THEME}} in the era {{ERA}}.
- Action: Dynamic movement, historical figures reacting to the hero or the event.
- Visual Gag: Witty physical comedy happening in the background, linked to the article's legal topic.
- Props/Vehicles: 100% era-accurate details (materials, wear and tear, dust).

LIGHTING & ATMOSPHERE:
- Color Palette: Realistic, rich colors (Fujifilm Velvia simulation), NO vintage yellow filters, NO sepia.

TYPOGRAPHY & BRANDING:
- Headline: a SHORTENED title (2-5 words, NOT the full article title) "{{HEADLINE}}" in big white bold condensed Cyrillic across the top, possibly on a bright plaque, as in the owner samples. Readable when shrunk to 396x300: within central third horizontally; 2-3 lines if needed. Never cover the hero's face.
- Language: All visible text MUST be in Russian Cyrillic, spelled exactly as given.
- Footer: Subtle Telegram logo and handle @LIREATE at the very bottom (small, neutral).

TECHNICAL QUALITY TARGETS:
- 8k resolution, raw photo quality. ISO 100 grain (subtle).
- Depth of Field: Sharp face, slightly softer background but clearly legible details.
- Imperfections: Chromatic aberration on edges, motion blur on fast-moving background elements.

NEGATIVE PROMPT:
Drawing, painting, illustration, 3d render, cartoon, anime, sketch, plastic skin, smooth skin, doll-like, blurry face, bad eyes, distorted hands, watermark, latin letters (except @LIREATE), english text, misspelled Russian.
```

## ERA LIST

Каменный век; Древний Египет; Шумер; Античная Греция; Римская Империя; Помпеи до извержения; Вавилон; Древний Китай (Хань);
Эпоха викингов; Рыцарское Средневековье; Япония Эдо (самураи); Золотая Орда; Крестовые походы; Инквизиция; Чёрная смерть; Империя ацтеков;
Итальянский Ренессанс; Золотой век пиратства; Французский двор (рококо); Мушкетёры; Османская империя; Русское царство до Петра; Великие географические открытия;
Дикий Запад; Викторианский Лондон; Индустриальная революция (стимпанк); Наполеоновские войны; Золотая лихорадка; Гражданская война в США;
Титаник; Ревущие 20-е; Великая депрессия; Нуар 40-х; Вторая мировая; Американские 50-е; Хиппи 60-х; Космическая гонка; Диско 70-х; Неоновые 80-е; Гранж 90-х; Лихие 90-е (Россия); Y2K;
Высадка на Луну; Падение Берлинской стены; Чернобыль (ликвидаторы); Полёт братьев Райт; Коронация монарха; Вудсток; Сухой закон (США); Киберпанк.

## QA перед merge (чеклист в `cover/cover-kie-qa.md`)

1. Лицо узнаваемо (identity lock с reference).
2. Кириллица в заголовке без ошибок (как в `cover_headline` meta).
3. Заголовок **не** на лице; читаем при превью **396×300**.
4. Руки без артефактов.
5. Только @LIREATE латиницей внизу.

После генерации: crop/resize → `cover/cover.png` **860×400**, `cover/cover-small.png` **350×163** (сохранить верх кадра с заголовком и лицом).

### Центральная обрезка 396×300 (обязательная проверка)

Перед merge сделай **центральную** обрезку `cover.png` до **396×300** (как на карточках в ленте): по высоте весь кадр 400 px, по ширине — центральный фрагмент с соотношением 396:300, затем масштаб до 396×300. Сохрани артефакт `cover/cover-preview-396x300.png`.

**Правило композиции:** сокращённый заголовок на плашке должен **целиком** помещаться в **средней трети** ширины кадра (не уезжать в левый/правый край после центрального кропа). Если заголовок длинный — разбей на **2–3 строки** на плашке; **не** закрывай лицо героини.

**Проверка:** открой `cover-preview-396x300.png` и убедись, что текст заголовка **не обрезан** по краям и читаем; зафиксируй PASS в `cover/cover-kie-qa.md`.
