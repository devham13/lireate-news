<?php
/**
 * Shorten news.seo_title > 70 chars (legacy articles). Does not touch datetime or full_story.
 * CLI: php lireate_db_shorten_seo_titles.php <DOCROOT> [--dry-run]
 */
if (php_sapi_name() !== 'cli') {
    exit(2);
}

$docroot = isset($argv[1]) ? $argv[1] : '';
$dry = in_array('--dry-run', $argv, true);
if ($docroot === '') {
    fwrite(STDERR, "usage: php lireate_db_shorten_seo_titles.php DOCROOT [--dry-run]\n");
    exit(2);
}

$dbFile = rtrim($docroot, '/') . '/data/db.php';
$text = @file_get_contents($dbFile);
if ($text === false) {
    echo json_encode(array('ok' => false, 'error' => 'db.php'), JSON_UNESCAPED_UNICODE) . "\n";
    exit(2);
}
$keys = array('DB_SERVER', 'DB_USER', 'DB_PASS', 'DB_NAME');
$cfg = array();
foreach ($keys as $key) {
    if (!preg_match('/define\s*\(\s*["\']' . $key . '["\']\s*,\s*["\']([^"\']*)["\']\s*\)/i', $text, $m)) {
        echo json_encode(array('ok' => false, 'error' => $key), JSON_UNESCAPED_UNICODE) . "\n";
        exit(2);
    }
    $cfg[$key] = $m[1];
}
$mysqli = @new mysqli($cfg['DB_SERVER'], $cfg['DB_USER'], $cfg['DB_PASS'], $cfg['DB_NAME']);
if ($mysqli->connect_errno) {
    echo json_encode(array('ok' => false, 'error' => 'connect'), JSON_UNESCAPED_UNICODE) . "\n";
    exit(2);
}
$mysqli->set_charset('utf8mb4');

$max = 70;
$res = $mysqli->query('SELECT `id`,`seo_url`,`seo_title` FROM `news` WHERE `active`=1');
$updated = 0;
while ($row = $res->fetch_assoc()) {
    $title = (string) $row['seo_title'];
    $len = function_exists('mb_strlen') ? mb_strlen($title, 'UTF-8') : strlen($title);
    if ($len <= $max) {
        continue;
    }
    $new = function_exists('mb_substr') ? mb_substr($title, 0, $max - 1, 'UTF-8') : substr($title, 0, $max - 1);
    $new = rtrim($new, " ,.-:;");
    if ($new === $title) {
        continue;
    }
    if (!$dry) {
        $st = $mysqli->prepare('UPDATE `news` SET `seo_title`=? WHERE `id`=?');
        $id = (int) $row['id'];
        $st->bind_param('si', $new, $id);
        $st->execute();
        $st->close();
    }
    $updated++;
}
$res->free();
$mysqli->close();
echo json_encode(array('ok' => true, 'updated' => $updated, 'dry_run' => $dry), JSON_UNESCAPED_UNICODE) . "\n";
