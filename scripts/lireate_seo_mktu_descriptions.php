<?php
/**
 * Set seo_description on mktu classes 1–45 (120–160 chars meaningful).
 * CLI: php lireate_seo_mktu_descriptions.php <DOCROOT> [--apply]
 */
if (php_sapi_name() !== 'cli') {
    exit(2);
}
$docroot = isset($argv[1]) ? $argv[1] : '';
$apply = in_array('--apply', $argv, true);
if ($docroot === '') {
    fwrite(STDERR, "usage: php lireate_seo_mktu_descriptions.php <DOCROOT> [--apply]\n");
    exit(2);
}
require $docroot . '/data/db.php';
$mysqli = new mysqli(DB_SERVER, DB_USER, DB_PASS, DB_NAME);
if ($mysqli->connect_errno) {
    fwrite(STDERR, "connect failed\n");
    exit(2);
}
$mysqli->set_charset('utf8mb4');

function lireate_mktu_trim_desc($text, $min = 120, $max = 160)
{
    $text = trim(preg_replace('/\s+/u', ' ', strip_tags(html_entity_decode($text, ENT_QUOTES, 'UTF-8'))));
    if ($text === '') {
        return '';
    }
    if (function_exists('mb_strlen') && mb_strlen($text, 'UTF-8') <= $max) {
        if (mb_strlen($text, 'UTF-8') >= $min) {
            return $text;
        }
    } elseif (strlen($text) <= $max) {
        if (strlen($text) >= $min) {
            return $text;
        }
    }
    $cut = function_exists('mb_substr') ? mb_substr($text, 0, $max - 1, 'UTF-8') : substr($text, 0, $max - 1);
    $cut = preg_replace('/\s+\S*$/u', '', $cut);
    if ($cut === '') {
        $cut = function_exists('mb_substr') ? mb_substr($text, 0, $max, 'UTF-8') : substr($text, 0, $max);
    }
    return rtrim($cut, '.,;:- ') . '…';
}

$res = $mysqli->query("SELECT id, seo_url, name, full_story, seo_description FROM mktu WHERE seo_url REGEXP '^[0-9]+$' ORDER BY CAST(seo_url AS UNSIGNED)");
$updates = array();
while ($row = $res->fetch_assoc()) {
    $n = (int) $row['seo_url'];
    if ($n < 1 || $n > 45) {
        continue;
    }
    $fromStory = lireate_mktu_trim_desc($row['full_story']);
    if ($fromStory === '') {
        $fromStory = lireate_mktu_trim_desc($row['seo_description']);
    }
    if ($fromStory === '') {
        $fromStory = lireate_mktu_trim_desc('Класс ' . $n . ' МКТУ-13: виды товаров и услуг для заявки на товарный знак — перечень Роспатента и примеры позиций.');
    }
    if ($fromStory !== $row['seo_description']) {
        $updates[] = array('id' => (int) $row['id'], 'seo_url' => $row['seo_url'], 'new' => $fromStory);
    }
}
echo json_encode(array('mode' => $apply ? 'apply' : 'dry-run', 'count' => count($updates), 'updates' => $updates), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . "\n";
if ($apply && !empty($updates)) {
    $st = $mysqli->prepare('UPDATE mktu SET seo_description=? WHERE id=?');
    foreach ($updates as $u) {
        $st->bind_param('si', $u['new'], $u['id']);
        $st->execute();
    }
}
