<?php
/**
 * Lireate news publish via MySQL (same host as public_html).
 *
 *   php lireate_db_publish.php diagnostic <DOCROOT>
 *   cat payload.json | php lireate_db_publish.php publish <DOCROOT>
 *
 * Parses <DOCROOT>/data/db.php as text (does not require/execute it).
 * Honors LIREATE_ALLOW_PUBLISH=yes for real INSERT; otherwise publish prints planned row only.
 */

if (php_sapi_name() !== 'cli') {
    fwrite(STDERR, "CLI only\n");
    exit(2);
}

function lireate_out($data, $exit = 0)
{
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . "\n";
    exit($exit);
}

function lireate_truthy_env($name)
{
    $v = strtolower(trim((string) getenv($name)));
    return in_array($v, array('1', 'yes', 'true', 'on'), true);
}

function lireate_parse_db_constants($dbFile)
{
    $text = @file_get_contents($dbFile);
    if ($text === false) {
        lireate_out(array('ok' => false, 'error' => 'cannot read db.php', 'path' => $dbFile), 2);
    }
    $keys = array('DB_SERVER', 'DB_USER', 'DB_PASS', 'DB_NAME');
    $out = array();
    foreach ($keys as $key) {
        $pattern = '/define\s*\(\s*["\']' . $key . '["\']\s*,\s*["\']([^"\']*)["\']\s*\)/i';
        if (!preg_match($pattern, $text, $m)) {
            lireate_out(array(
                'ok' => false,
                'error' => 'define not found in db.php',
                'constant' => $key,
                'path' => $dbFile,
            ), 2);
        }
        $out[$key] = $m[1];
    }
    return $out;
}

function lireate_mysqli_connect($cfg)
{
    $mysqli = @new mysqli($cfg['DB_SERVER'], $cfg['DB_USER'], $cfg['DB_PASS'], $cfg['DB_NAME']);
    if ($mysqli->connect_errno) {
        lireate_out(array(
            'ok' => false,
            'error' => 'mysqli connect failed',
            'errno' => $mysqli->connect_errno,
            'message' => $mysqli->connect_error,
        ), 2);
    }
    if (!$mysqli->set_charset('utf8mb4')) {
        $mysqli->set_charset('utf8');
    }
    return $mysqli;
}

function lireate_translit_fallback($str)
{
    $str = (string) $str;
    $map = array(
        'А' => 'A', 'Б' => 'B', 'В' => 'V', 'Г' => 'G', 'Д' => 'D', 'Е' => 'E', 'Ё' => 'E',
        'Ж' => 'Zh', 'З' => 'Z', 'И' => 'I', 'Й' => 'Y', 'К' => 'K', 'Л' => 'L', 'М' => 'M',
        'Н' => 'N', 'О' => 'O', 'П' => 'P', 'Р' => 'R', 'С' => 'S', 'Т' => 'T', 'У' => 'U',
        'Ф' => 'F', 'Х' => 'H', 'Ц' => 'Ts', 'Ч' => 'Ch', 'Ш' => 'Sh', 'Щ' => 'Sch',
        'Ъ' => '', 'Ы' => 'Y', 'Ь' => '', 'Э' => 'E', 'Ю' => 'Yu', 'Я' => 'Ya',
        'а' => 'a', 'б' => 'b', 'в' => 'v', 'г' => 'g', 'д' => 'd', 'е' => 'e', 'ё' => 'e',
        'ж' => 'zh', 'з' => 'z', 'и' => 'i', 'й' => 'y', 'к' => 'k', 'л' => 'l', 'м' => 'm',
        'н' => 'n', 'о' => 'o', 'п' => 'p', 'р' => 'r', 'с' => 's', 'т' => 't', 'у' => 'u',
        'ф' => 'f', 'х' => 'h', 'ц' => 'ts', 'ч' => 'ch', 'ш' => 'sh', 'щ' => 'sch',
        'ъ' => '', 'ы' => 'y', 'ь' => '', 'э' => 'e', 'ю' => 'yu', 'я' => 'ya',
    );
    $str = strtr($str, $map);
    $str = preg_replace('/[^a-zA-Z0-9\-_]+/u', '-', $str);
    $str = preg_replace('/-+/', '-', $str);
    $str = trim($str, '-');
    return strtolower($str);
}

function lireate_seo_url($name, $explicit)
{
    if ($explicit !== null && $explicit !== '') {
        return trim(str_replace('/', '', (string) $explicit));
    }
    if (function_exists('Translit')) {
        $u = Translit($name);
    } else {
        $u = lireate_translit_fallback($name);
    }
    return trim(str_replace('/', '', (string) $u));
}

function lireate_story($html)
{
    $html = (string) $html;
    if (function_exists('get_quotes')) {
        $html = get_quotes($html);
    }
    $allowed = '<p><br><a><strong><em><ul><ol><li><h2><h3><h4><img><blockquote><table><thead><tbody><tr><th><td><div><span>';
    return strip_tags($html, $allowed);
}

function lireate_mysqli($docroot)
{
    $dbFile = rtrim($docroot, '/') . '/data/db.php';
    if (!is_file($dbFile)) {
        lireate_out(array('ok' => false, 'error' => 'missing db.php', 'path' => $dbFile), 2);
    }
    $cfg = lireate_parse_db_constants($dbFile);
    return lireate_mysqli_connect($cfg);
}

function lireate_table_columns($mysqli, $table)
{
    $cols = array();
    $res = $mysqli->query('DESCRIBE `' . $mysqli->real_escape_string($table) . '`');
    if (!$res) {
        return $cols;
    }
    while ($row = $res->fetch_assoc()) {
        $cols[] = $row['Field'];
    }
    $res->free();
    return $cols;
}

function lireate_snippet($text, $len)
{
    $text = (string) $text;
    if (function_exists('mb_substr')) {
        return mb_substr($text, 0, $len, 'UTF-8');
    }
    return substr($text, 0, $len);
}

function lireate_cmd_diagnostic($docroot)
{
    date_default_timezone_set('Europe/Moscow');
    $mysqli = lireate_mysqli($docroot);
    $out = array('ok' => true, 'mode' => 'diagnostic', 'docroot' => $docroot, 'timezone' => date_default_timezone_get());

    $describe = array();
    $res = $mysqli->query('DESCRIBE `news`');
    if ($res) {
        while ($row = $res->fetch_assoc()) {
            $describe[] = $row;
        }
        $res->free();
    } else {
        $out['describe_news_error'] = $mysqli->error;
    }
    $out['describe_news'] = $describe;

    $rows = array();
    $res = $mysqli->query(
        'SELECT `id`,`category`,`name`,`seo_url`,`title`,`active`,`datetime` FROM `news` ORDER BY `id` DESC LIMIT 3'
    );
    if ($res) {
        while ($row = $res->fetch_assoc()) {
            $rows[] = $row;
        }
        $res->free();
    } else {
        $out['latest_news_error'] = $mysqli->error;
    }
    $out['latest_news'] = $rows;

    $story = array();
    $res = $mysqli->query(
        'SELECT `id`,`short_story`,`full_story` FROM `news` ORDER BY `id` DESC LIMIT 1'
    );
    if ($res && ($row = $res->fetch_assoc())) {
        $story = array(
            'id' => $row['id'],
            'short_story_head' => lireate_snippet($row['short_story'], 400),
            'full_story_head' => lireate_snippet($row['full_story'], 400),
        );
        $res->free();
    }
    $out['latest_story_snippets'] = $story;

    $categories = array();
    foreach (array('category', 'categories', 'news_category') as $tbl) {
        $res = $mysqli->query('SHOW TABLES LIKE \'' . $mysqli->real_escape_string($tbl) . '\'');
        if ($res && $res->num_rows > 0) {
            $res->free();
            $q = $mysqli->query('SELECT * FROM `' . $tbl . '` LIMIT 50');
            if ($q) {
                while ($row = $q->fetch_assoc()) {
                    $categories[] = array('table' => $tbl, 'row' => $row);
                }
                $q->free();
            }
            break;
        }
        if ($res) {
            $res->free();
        }
    }
    $out['categories'] = $categories;
    $out['translit_source'] = 'lireate_translit_fallback (db.php not executed)';
    $out['get_quotes'] = false;
    $mysqli->close();
    lireate_out($out, 0);
}

function lireate_cmd_publish($docroot)
{
    date_default_timezone_set('Europe/Moscow');
    $raw = stream_get_contents(STDIN);
    $payload = json_decode($raw, true);
    if (!is_array($payload)) {
        lireate_out(array('ok' => false, 'error' => 'invalid JSON on stdin'), 2);
    }

    $allow = lireate_truthy_env('LIREATE_ALLOW_PUBLISH');
    $forceDry = !empty($payload['dry_run']);
    $dry = $forceDry || !$allow;

    $name = isset($payload['name']) ? trim((string) $payload['name']) : '';
    if ($name === '') {
        lireate_out(array('ok' => false, 'error' => 'payload.name required'), 2);
    }

    $title = isset($payload['title']) ? trim((string) $payload['title']) : $name;
    $seoTitle = isset($payload['seo_title']) ? trim((string) $payload['seo_title']) : $name;
    $seoKeywords = isset($payload['seo_keywords']) ? trim((string) $payload['seo_keywords']) : '';
    $seoDescription = isset($payload['seo_description']) ? trim((string) $payload['seo_description']) : '';
    $explicitSeo = isset($payload['seo_url']) ? (string) $payload['seo_url'] : '';
    $seoUrl = lireate_seo_url($name, $explicitSeo);
    $category = isset($payload['category']) ? (int) $payload['category'] : 9;
    $shortStory = lireate_story(isset($payload['short_story']) ? $payload['short_story'] : '');
    $fullStory = lireate_story(isset($payload['full_story']) ? $payload['full_story'] : '');
    $active = isset($payload['active']) ? (int) $payload['active'] : 1;
    $datetime = date('Y-m-d H:i:s');

    $row = array(
        'name' => $name,
        'short_story' => $shortStory,
        'full_story' => $fullStory,
        'title' => $title,
        'seo_url' => $seoUrl,
        'seo_title' => $seoTitle,
        'seo_keywords' => $seoKeywords,
        'seo_description' => $seoDescription,
        'category' => $category,
        'datetime' => $datetime,
        'active' => $active,
    );

    $mysqli = lireate_mysqli($docroot);

    $stmt = $mysqli->prepare('SELECT `id` FROM `news` WHERE `seo_url` = ? OR `name` = ? LIMIT 1');
    if ($stmt) {
        $stmt->bind_param('ss', $seoUrl, $name);
        $stmt->execute();
        $stmt->bind_result($dupId);
        if ($stmt->fetch()) {
            $stmt->close();
            $mysqli->close();
            lireate_out(array(
                'ok' => true,
                'mode' => 'publish',
                'dry_run' => $dry,
                'duplicate' => true,
                'existing_id' => $dupId,
                'detail' => 'skip duplicate seo_url or name',
                'row' => $row,
            ), 0);
        }
        $stmt->close();
    }

    if ($dry) {
        $mysqli->close();
        lireate_out(array(
            'ok' => true,
            'mode' => 'publish',
            'dry_run' => true,
            'would_insert' => $row,
            'allow_publish' => $allow,
        ), 0);
    }

    $cols = lireate_table_columns($mysqli, 'news');
    $insertCols = array('name', 'short_story', 'full_story', 'title', 'seo_url', 'seo_title', 'seo_keywords', 'seo_description', 'category', 'datetime');
    if (in_array('active', $cols, true)) {
        $insertCols[] = 'active';
    }

    $placeholders = implode(',', array_fill(0, count($insertCols), '?'));
    $colList = '`' . implode('`,`', $insertCols) . '`';
    $sql = 'INSERT INTO `news` (' . $colList . ') VALUES (' . $placeholders . ')';
    $stmt = $mysqli->prepare($sql);
    if (!$stmt) {
        lireate_out(array('ok' => false, 'error' => 'prepare failed', 'mysqli' => $mysqli->error, 'sql' => $sql), 2);
    }

    $types = '';
    $values = array();
    foreach ($insertCols as $c) {
        if ($c === 'category' || $c === 'active') {
            $types .= 'i';
            $values[] = (int) $row[$c];
        } else {
            $types .= 's';
            $values[] = (string) $row[$c];
        }
    }

    $bind = array($types);
    foreach ($values as $i => $v) {
        $bind[] = &$values[$i];
    }
    call_user_func_array(array($stmt, 'bind_param'), $bind);

    $ok = $stmt->execute();
    $newId = $stmt->insert_id;
    $err = $stmt->error;
    $stmt->close();
    $mysqli->close();

    if (!$ok) {
        lireate_out(array('ok' => false, 'error' => 'insert failed', 'mysqli' => $err, 'row' => $row), 2);
    }

    lireate_out(array(
        'ok' => true,
        'mode' => 'publish',
        'dry_run' => false,
        'insert_id' => $newId,
        'row' => $row,
    ), 0);
}

$argc = $_SERVER['argc'];
$argv = $_SERVER['argv'];
if ($argc < 3) {
    lireate_out(array(
        'ok' => false,
        'error' => 'usage: php lireate_db_publish.php diagnostic|publish <DOCROOT>',
    ), 2);
}

$cmd = strtolower($argv[1]);
$docroot = $argv[2];
if (!is_dir($docroot)) {
    lireate_out(array('ok' => false, 'error' => 'DOCROOT not a directory', 'path' => $docroot), 2);
}

if ($cmd === 'diagnostic') {
    lireate_cmd_diagnostic($docroot);
}
if ($cmd === 'publish') {
    lireate_cmd_publish($docroot);
}

lireate_out(array('ok' => false, 'error' => 'unknown command', 'command' => $cmd), 2);
