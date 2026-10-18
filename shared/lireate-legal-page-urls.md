# Lireate — канонические URL политики и согласия

Проверено владельцем: страницы отдают **HTTP 200** на публичном домене сайта (см. Cloud Secret / env для публикации Lireate). Другие пути **не придумывать** (в т.ч. `/privacy/` на том же домене → **404**).

| Документ | Path (от корня сайта) |
|----------|------------------------|
| Политика конфиденциальности | `/politika_konfidencialnosti` |
| Согласие на обработку персональных данных | `/private_data` |

Полный URL: `{LIREATE_PUBLIC_SITE_URL}` без завершающего слэша + path (например для проверки link-verify: `--site-base` = значение env).

## Запрещённые шаблоны ссылок

- `/privacy`, `/privacy/`, `/policy`, `/policy/` и любые варианты с тем же path на любом хосте
- Выдуманные URL политики (англоязычные заглушки, чужие домены без согласования)

## Проверка в CI и локально

```bash
python3 scripts/lireate_privacy_link_policy.py --all-lireate
python3 scripts/excalibur_blog_html_linter.py memory/blog/articles/L01-.../article.html
python3 scripts/excalibur_blog_link_verify.py ... --site-base "$LIREATE_PUBLIC_SITE_URL"
```

Логика: `scripts/lireate_privacy_link_policy.py` (подключается в HTML- и link-verify линтерах).
