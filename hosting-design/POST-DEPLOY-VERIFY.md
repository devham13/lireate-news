# post_deploy_verify

- Маркеры ищутся только в открывающем теге `<body …>`, не по всей HTML.
- Cache-bust: заголовок `X-Lireate-Deploy-Verify` (без `?lireate_verify=` в URL — иначе ломаются `preg_match` по `REQUEST_URI`).
- При провале body: в stderr (и опционально `LIREATE_VERIFY_BODY_LOG`) строка `VERIFY_BODY_TAG` с фактическим `<body …>`.
- Перед verify apply вызывает `lireate_design_main_uri_regex_query_upgrade.py` (`(?:[/?]|$)` в preg_match).
- Opcache: `opcache_invalidate` в начале и каждую 3-ю попытку body-check.
