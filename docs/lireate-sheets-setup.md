# Google Sheets: автожурнал опубликованных статей
Источник: Google-таблица `lireate_blog_articles`, вкладка `Статьи блога`, столбцы `№ | Название | Ссылка | О чём статья`. Исходную таблицу не загружать в репозиторий: используется ее оригинал в Google Drive.

1. В Google Sheets откройте **Расширения → Apps Script** именно у исходной таблицы. Вставьте содержимое `integrations/google-apps-script/lireate_articles.gs`.
2. В **Project Settings → Script properties** задайте `SPREADSHEET_ID` (ID оригинала из URL), `SHEET_NAME=Статьи блога`, `WEBHOOK_SECRET` (случайные 32+ символов). Не добавляйте эти значения в GitHub.
3. **Deploy → New deployment → Web app**: Execute as **Me**, Who has access **Anyone** (для вызова с REG.RU), подтвердите разрешения. Доступ защищён секретом в теле запроса, но Web App URL публичен, поэтому используйте длинный случайный секрет.
4. На хостинге REG.RU в `$HOME/lireate-autopub/.env` задайте `LIREATE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/.../exec` и `LIREATE_SHEETS_WEBHOOK_SECRET` с тем же секретом.
5. При успешной публикации `scripts/lireate_hosting_publish.py` автоматически записывает событие в outbox и пытается отправить его. При сбое Google событие останется в `state/sheets-outbox` и повторится при следующем CRON запуске. Вызов `python3 scripts/lireate_sheets_sync.py` вручную повторит доставку.
6. Проверка: опубликуйте новую статью (обычный CRON), убедитесь в появлении **одной** строки внизу, с правильным заголовком, живой ссылкой, кратким содержанием. Повторный запрос не добавляет вторую строку.

Важно: настройка развертывания и секретов обязательна. Сам коммит в GitHub **не даёт** доступа к Google Sheets. Не записывайте статьи в таблицу до подтверждения публикации (HTTP 200). Если таблица расширяет список колонок, измените проверку headers и схему в Apps Script осознанно.
