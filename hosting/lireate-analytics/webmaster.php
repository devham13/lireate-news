<?php
declare(strict_types=1);

/**
 * Protected JSON feed for Yandex Webmaster export (outside docroot data).
 * Deploy: scripts/lireate_hosting_webmaster_export.py --deploy-php
 */

const LIREATE_AUTOPUB_HOME = '{{LIREATE_AUTOPUB_HOME}}';
const LIREATE_ENV_FILE = LIREATE_AUTOPUB_HOME . '/.env';
const LIREATE_WEBMASTER_JSON = LIREATE_AUTOPUB_HOME . '/analytics/webmaster.json';

header('Cache-Control: no-store, no-cache, must-revalidate');
header('X-Content-Type-Options: nosniff');

$provided = $_SERVER['HTTP_X_LIREATE_KEY'] ?? '';
if ($provided === '' || !is_readable(LIREATE_ENV_FILE)) {
    http_response_code(403);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => 'forbidden'], JSON_UNESCAPED_UNICODE);
    exit;
}

$expected = '';
foreach (file(LIREATE_ENV_FILE, FILE_IGNORE_NEW_LINES) ?: [] as $line) {
    $line = trim($line);
    if ($line === '' || $line[0] === '#') {
        continue;
    }
    if (strpos($line, 'LIREATE_ANALYTICS_KEY=') === 0) {
        $expected = trim(substr($line, strlen('LIREATE_ANALYTICS_KEY=')), " \t\"'");
        break;
    }
}

if ($expected === '' || !hash_equals($expected, $provided)) {
    http_response_code(403);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => 'forbidden'], JSON_UNESCAPED_UNICODE);
    exit;
}

if (!is_readable(LIREATE_WEBMASTER_JSON)) {
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => 'export_not_ready'], JSON_UNESCAPED_UNICODE);
    exit;
}

header('Content-Type: application/json; charset=utf-8');
readfile(LIREATE_WEBMASTER_JSON);
