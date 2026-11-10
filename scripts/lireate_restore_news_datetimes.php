<?php
/**
 * One-time: restore news.datetime (datePublished) from mapping JSON after erroneous --update.
 * Does not touch full_story or other columns. CLI only.
 *
 *   php lireate_restore_news_datetimes.php dry-run <DOCROOT> <mapping.json>
 *   LIREATE_ALLOW_PUBLISH=yes php lireate_restore_news_datetimes.php apply <DOCROOT> <mapping.json>
 */
if (php_sapi_name() !== 'cli') {
    exit(2);
}

// Minimal DB bootstrap (cannot require lireate_db_publish.php — it parses argv).
function lireate_restore_mysqli($docroot)
{
    $dbFile = rtrim($docroot, '/') . '/data/db.php';
    if (!is_file($dbFile)) {
        fwrite(STDERR, "missing db.php\n");
        exit(2);
    }
    $text = file_get_contents($dbFile);
    $keys = array('DB_SERVER', 'DB_USER', 'DB_PASS', 'DB_NAME');
  $cfg = array();
    foreach ($keys as $key) {
        if (!preg_match('/define\s*\(\s*["\']' . $key . '["\']\s*,\s*["\']([^"\']*)["\']\s*\)/i', $text, $m)) {
            fwrite(STDERR, "define $key missing\n");
            exit(2);
        }
        $cfg[$key] = $m[1];
    }
    $mysqli = @new mysqli($cfg['DB_SERVER'], $cfg['DB_USER'], $cfg['DB_PASS'], $cfg['DB_NAME']);
    if ($mysqli->connect_errno) {
        fwrite(STDERR, "connect failed\n");
        exit(2);
    }
    $mysqli->set_charset('utf8mb4');
    return $mysqli;
}

function lireate_restore_truthy($name)
{
    $v = strtolower(trim((string) getenv($name)));
    return in_array($v, array('1', 'yes', 'true', 'on'), true);
}

function lireate_restore_usage()
{
    fwrite(STDERR, "usage: php lireate_restore_news_datetimes.php dry-run|apply <DOCROOT> <mapping.json>\n");
    exit(2);
}

$argc = $_SERVER['argc'];
$argv = $_SERVER['argv'];
if ($argc < 4) {
    lireate_restore_usage();
}

$mode = strtolower($argv[1]);
$docroot = $argv[2];
$mapFile = $argv[3];
if (!in_array($mode, array('dry-run', 'apply'), true)) {
    lireate_restore_usage();
}
if (!is_dir($docroot) || !is_file($mapFile)) {
    fwrite(STDERR, "missing docroot or mapping file\n");
    exit(2);
}

$map = json_decode(file_get_contents($mapFile), true);
if (!is_array($map)) {
    fwrite(STDERR, "invalid mapping json\n");
    exit(2);
}

$mysqli = lireate_restore_mysqli($docroot);
$allow = lireate_restore_truthy('LIREATE_ALLOW_PUBLISH');
$updated = array();
$skipped = array();

foreach ($map as $seoUrl => $dateStr) {
    $seoUrl = trim(str_replace('/', '', (string) $seoUrl));
    $ts = strtotime((string) $dateStr . ' 12:00:00 Europe/Moscow');
    if ($seoUrl === '' || $ts === false) {
        $skipped[] = array('seo_url' => $seoUrl, 'reason' => 'bad date');
        continue;
    }
    $stmt = $mysqli->prepare('SELECT `id`, `datetime` FROM `news` WHERE `seo_url` = ? LIMIT 1');
    $stmt->bind_param('s', $seoUrl);
    $stmt->execute();
    $stmt->bind_result($id, $cur);
    if (!$stmt->fetch()) {
        $skipped[] = array('seo_url' => $seoUrl, 'reason' => 'not found');
        $stmt->close();
        continue;
    }
    $stmt->close();
    if ($mode === 'dry-run') {
        $updated[] = array('id' => $id, 'seo_url' => $seoUrl, 'from' => $cur, 'to' => $ts, 'date' => $dateStr);
        continue;
    }
    if (!$allow) {
        fwrite(STDERR, "LIREATE_ALLOW_PUBLISH not set for apply\n");
        exit(1);
    }
    $up = $mysqli->prepare('UPDATE `news` SET `datetime`=? WHERE `id`=?');
    $up->bind_param('ii', $ts, $id);
    $up->execute();
    $up->close();
    $updated[] = array('id' => $id, 'seo_url' => $seoUrl, 'from' => $cur, 'to' => $ts);
}

$mysqli->close();
echo json_encode(array('mode' => $mode, 'updated' => $updated, 'skipped' => $skipped), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . "\n";
