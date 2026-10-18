# Lireate NEWS — каталог стилей обложек

Канон для ротации: `memory/blog/cover-style-registry.json`. В `article.meta.json` и `cover/cover-registry.json` фиксируется объект **`cover_style`**.

## Зачем

Один и тот же шаблон (героиня слева + белая плашка справа сверху + карточка документа с красным badge) **запрещён** для новых статей. Каждая обложка визуально узнаваема как Lireate, но **композиция и палитра** меняются.

## Поля `cover_style`

| Поле | Описание |
|------|----------|
| `style_id` | ID из таблицы ниже |
| `layout_id` | Композиция кадра (см. стиль) |
| `caption_layout_id` | Размещение PIL-подписи (не повторять у соседней статьи) |
| `palette_id` | Цветовая схема |
| `hero_present` | `true` / `false` — есть ли героиня с reference-лицом |

## Правила ротации (обязательные)

1. **Не повторять `style_id`** среди **последних 3** опубликованных L-статей (по номеру Lxx).
2. **Не повторять `caption_layout_id`** у **предыдущей** L-статьи.
3. Русский текст на обложке — **только PIL** (`scripts/lireate_cover_text_overlay.py`), не image AI.
4. Героиня — эталон `memory/cover/assets/blog-hero-reference.png`; **поза, кадр, локация, роль** меняются; в стилях без человека — объект или типографика.

Проверка: `python3 scripts/lireate_cover_style_check.py --article-dir <dir>`  
Подбор стиля: `python3 scripts/lireate_cover_style_pick.py --topic-id L03`

---

## Стили (10 + legacy)

### 1. `editorial_magazine_photo` — Editorial magazine photo

| | |
|--|--|
| **Палитра** | `warm_editorial_ivory` — тёплый беж, мягкие тени, акцент тёмно-синий |
| **Композиция** | Герой 60–70% кадра, взгляд в объект/камеру; нижняя треть — полоса под заголовок |
| **Герой** | Да, крупный план или по пояс, деловой образ юриста |
| **Подпись PIL** | `caption_band_bottom_full` — широкая плашка снизу, крупный sans, тёмный текст |

### 2. `bold_color_typography` — Bold minimal typography on colour field

| | |
|--|--|
| **Палитра** | `electric_violet_white` — насыщенный фиолетовый/синий фон, белый текст |
| **Композиция** | Без фото; геометрический акцент (круг/полоса); центр пустой |
| **Герой** | Нет |
| **Подпись PIL** | `caption_center_stack` — 2–3 строки по центру, без плашки или тонкая обводка |

### 3. `flat_vector_trademark` — Flat vector (™ / shield)

| | |
|--|--|
| **Палитра** | `mint_charcoal_coral` |
| **Композиция** | Векторные знаки ТЗ, щит, документ; правило третей |
| **Герой** | Нет |
| **Подпись PIL** | `caption_left_column` — колонка слева 40% ширины |

### 4. `render_3d_symbol` — 3D render symbolic object

| | |
|--|--|
| **Палитра** | `studio_gray_gold` |
| **Композиция** | Весы / печать / ® на подставке, студийный свет |
| **Герой** | Нет |
| **Подпись PIL** | `caption_upper_left_compact` — тёмная плашка, светлый текст |

### 5. `isometric_scene` — Isometric scene

| | |
|--|--|
| **Палитра** | `sky_teal_white` |
| **Композиция** | Изометрия: маркетплейс, коробки, ноутбук |
| **Герой** | Опционально — мини-фигура в углу |
| **Подпись PIL** | `caption_split_sidebar` — вертикальная плашка справа |

### 6. `collage_paper_cut` — Collage / paper cut

| | |
|--|--|
| **Палитра** | `paper_craft_terracotta` |
| **Композиция** | Вырезанная бумага, слои, лицо героини слева небольшим |
| **Герой** | Да, уменьшенный портрет |
| **Подпись PIL** | `caption_diagonal_accent` — плашка по диагонали |

### 7. `dark_cinematic_closeup` — Dark cinematic close-up

| | |
|--|--|
| **Палитра** | `cinematic_navy_amber` |
| **Композиция** | Тёмный фон, контровой свет, героиня справа |
| **Герой** | Да, крупный план |
| **Подпись PIL** | `caption_lower_third_dark` — нижняя треть, светлый текст на тёмной плашке |

### 8. `split_screen_before_after` — Split screen before/after

| | |
|--|--|
| **Палитра** | `split_muted_green_red` |
| **Композиция** | Вертикальный сплит «проблема / решение» |
| **Герой** | Опционально на стороне «после» |
| **Подпись PIL** | `caption_band_bottom_full` |

### 9. `infographic_composition` — Infographic-style

| | |
|--|--|
| **Палитра** | `info_blue_gray` |
| **Композиция** | Пустые графики/иконки; героиня мелко снизу слева |
| **Герой** | Да, мелко |
| **Подпись PIL** | `caption_plate_top_right` — **запрещён подряд** после legacy |

### 10. `handdrawn_sketch` — Hand-drawn sketch

| | |
|--|--|
| **Палитра** | `sketch_pencil_ochre` |
| **Композиция** | Карандашный портрет героини, блокнот |
| **Герой** | Да, скетч-портрет |
| **Подпись PIL** | `caption_left_column` |

### Legacy (только история L01–L02)

**`legacy_hero_left_doc_card`** — героиня слева + UI-карточка документа справа + плашка заголовка сверху справа. **Не использовать** для новых статей.

---

## Пайплайн cover-агента (Lireate)

1. `python3 scripts/lireate_cover_style_pick.py --topic-id Lxx` → записать `cover_style` в `article.meta.json`.
2. Quad MCP prompt: `style_id` + `quad_prompt_hint` из registry (не legacy preset по умолчанию).
3. i2i → split → `lireate_cover_text_overlay.py` с `--style-id` и `caption_layout_id`.
4. `python3 scripts/lireate_cover_style_check.py --article-dir ...` → exit 0 или FAIL для CI.

См. также: `LIREATE-AUTOMATION.md`, `skills/cover-excalibur-blog/SKILL.md`.
