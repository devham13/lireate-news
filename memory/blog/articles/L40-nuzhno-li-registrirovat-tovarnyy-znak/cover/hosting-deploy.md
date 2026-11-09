# L40 — выкладка inline-04 на REG.RU

## Причина 404

Коллаж-пайплайн и gate знают слот `inline_4` (`inline-04.png`), но `scripts/lireate_hosting_images.py` и `lireate_publish_bundle.py` обрабатывают только **01–03**. При публикации в `full_story` переписываются пути только для трёх первых картинок; **четвёртая** остаётся `cover/inline-04.png` (404), файл `_inline_04.jpg` на диск не копируется.

## Что в репозитории

| Файл | Назначение |
|------|------------|
| `cover/inline-0N.png` | Исходники collage-v1 (перерендер без L01 в макетах) |
| `cover/hosting-sftp/*.jpg` | Готовые имена для `$LIREATE_DOCROOT/images/` |
| `article.html` | У 4-й фигуры `src` уже канонический `/images/nuzhno-li-registrirovat-tovarnyy-znak_inline_04.jpg` |

## До правки скриптов (разово)

```bash
# на хостинге, после merge
cp cover/hosting-sftp/nuzhno-li-registrirovat-tovarnyy-znak_inline_04.jpg \
  "$LIREATE_DOCROOT/images/"
# при необходимости обновить 01–03 теми же именами из hosting-sftp/
lireate_hosting_publish.py --update   # L40
```

## После правки `_HOSTING_INLINE_FILES` (+04)

Вернуть в `article.html` для inline-04 `src="cover/inline-04.png"` (как у 01–03) и полагаться на `transform_html_paths`.
