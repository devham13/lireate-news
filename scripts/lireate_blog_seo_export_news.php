<?php
/**
 * Export active news rows for SEO wave planning (CLI).
 *
 *   php lireate_blog_seo_export_news.php DOCROOT > news-export.json
 */
if (php_sapi_name() !== 'cli') {
    exit(2);
}

$GLOBALS['lireate_db_publish_embedded'] = true;
require_once __DIR__ . '/lireate_db_publish.php';

$docroot = isset($argv[1]) ? $argv[1] : '';
if ($docroot === '' || !is_dir($docroot)) {
    fwrite(STDERR, "usage: php lireate_blog_seo_export_news.php DOCROOT\n");
    exit(2);
}

$mysqli = lireate_mysqli($docroot);
$sql = 'SELECT `id`,`seo_url`,`name`,`seo_title`,`seo_description`,`category`,`datetime`'
    . ' FROM `news` WHERE `active`=1 ORDER BY `datetime` DESC';
$res = $mysqli->query($sql);
$rows = array();
if ($res) {
    while ($row = $res->fetch_assoc()) {
        $rows[] = array(
            'id' => (int) $row['id'],
            'seo_url' => (string) $row['seo_url'],
            'name' => (string) $row['name'],
            'seo_title' => (string) $row['seo_title'],
            'seo_description' => (string) $row['seo_description'],
            'category' => (int) $row['category'],
            'datetime' => (int) $row['datetime'],
            'seo_title_len' => strlen((string) $row['seo_title']),
            'seo_description_len' => strlen((string) $row['seo_description']),
        );
    }
    $res->free();
}

echo json_encode(
    array(
        'version' => 1,
        'exported_at' => gmdate('c'),
        'count' => count($rows),
        'articles' => $rows,
    ),
    JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT
);
echo "\n";