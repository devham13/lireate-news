<?php
/**
 * Protected JSON feed for Yandex Webmaster export (outside docroot data).
 * PHP 5.4+ (Apache mod_php on REG.RU may be older than CLI PHP 8).
 * Deploy: scripts/lireate_hosting_webmaster_export.py --deploy-php
 */

if (!function_exists('hash_equals')) {
    /**
     * Constant-time string compare (PHP < 5.6).
     *
     * @param string $known_string
     * @param string $user_string
     * @return bool
     */
    function hash_equals($known_string, $user_string)
    {
        if (!is_string($known_string) || !is_string($user_string)) {
            return false;
        }
        $len = strlen($known_string);
        if ($len !== strlen($user_string)) {
            return false;
        }
        $res = 0;
        for ($i = 0; $i < $len; $i++) {
            $res |= ord($known_string[$i]) ^ ord($user_string[$i]);
        }
        return $res === 0;
    }
}

define('LIREATE_AUTOPUB_HOME', '{{LIREATE_AUTOPUB_HOME}}');
define('LIREATE_ENV_FILE', LIREATE_AUTOPUB_HOME . '/.env');
define('LIREATE_WEBMASTER_JSON', LIREATE_AUTOPUB_HOME . '/analytics/webmaster.json');

header('Cache-Control: no-store, no-cache, must-revalidate');
header('X-Content-Type-Options: nosniff');

$provided = isset($_SERVER['HTTP_X_LIREATE_KEY']) ? (string) $_SERVER['HTTP_X_LIREATE_KEY'] : '';
if ($provided === '' || !is_readable(LIREATE_ENV_FILE)) {
    http_response_code(403);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(array('error' => 'forbidden'), JSON_UNESCAPED_UNICODE);
    exit;
}

$expected = '';
$env_lines = file(LIREATE_ENV_FILE, FILE_IGNORE_NEW_LINES);
if ($env_lines === false) {
    $env_lines = array();
}
foreach ($env_lines as $line) {
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
    echo json_encode(array('error' => 'forbidden'), JSON_UNESCAPED_UNICODE);
    exit;
}

if (!is_readable(LIREATE_WEBMASTER_JSON)) {
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(array('error' => 'export_not_ready'), JSON_UNESCAPED_UNICODE);
    exit;
}

header('Content-Type: application/json; charset=utf-8');
readfile(LIREATE_WEBMASTER_JSON);
