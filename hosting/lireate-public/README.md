# Патч лендинга `/news` (lireate.ru)

Шаблон ленты блога и `data/db.php` в этом репозитории **не хранятся**. Выкладка на REG.RU: docroot `public_html` на `server324.hosting.reg.ru` (см. `memory/hosting/lireate-reg-ru-production.md`).

## Задача

Снизить отказы на `/news` (~70% по Метрике): сверху показать материалы с лучшей вовлечённостью и явный призыв написать в мессенджер.

## Файлы

| Файл | Куда залить на сервере |
|------|-------------------------|
| `inc/news-featured-top.php` | `public_html/inc/news-featured-top.php` |
| `news-landing.css` | `public_html/inc/news-landing.css` |

## Подключение

1. Найти PHP-шаблон страницы списка блога (в HTML есть текст «Свежий материал» и блок «Блог LIREATE»). Обычно это модуль `news` в `public_html` (рядом с `admin/`).
2. После заголовка страницы и **до** цикла вывода последних постов из таблицы `news` добавить:

```php
<link rel="stylesheet" href="/inc/news-landing.css">
<?php require_once $_SERVER['DOCUMENT_ROOT'] . '/inc/news-featured-top.php'; ?>
```

3. Проверить `/news`: сверху блок с двумя ссылками (франчайзинг, сроки авторских прав) и кнопки Telegram / WhatsApp.
4. Хронологическая лента «Свежий материал» может остаться ниже без изменений SQL.

## Настройка без деплоя кода

Ссылки и тексты правятся в массиве `$lireate_featured` в `news-featured-top.php`. При смене ЧПУ статей обновите поле `url`.
