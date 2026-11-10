<?php
/**
 * Replace outdated «от 20 000 рублей» fee copy with 35 000 ₽ (ПП РФ № 941).
 * CLI: php lireate_seo_fee_update.php <DOCROOT> [--apply] [--dump row.sql]
 */
if (php_sapi_name() !== 'cli') {
    exit(2);
}
$docroot = isset($argv[1]) ? $argv[1] : '';
$apply = in_array('--apply', $argv, true);
$dumpPath = '';
foreach ($argv as $i => $arg) {
    if ($arg === '--dump' && isset($argv[$i + 1])) {
        $dumpPath = $argv[$i + 1];
    }
}
if ($docroot === '') {
    fwrite(STDERR, "usage: php lireate_seo_fee_update.php <DOCROOT> [--apply] [--dump file.sql]\n");
    exit(2);
}
require $docroot . '/data/db.php';
$mysqli = new mysqli(DB_SERVER, DB_USER, DB_PASS, DB_NAME);
$mysqli->set_charset('utf8mb4');

$patterns = array(
    'от 20 000 рублей' => 'от 35 000 ₽ за один класс МКТУ (пп. 2.1+2.4+2.11, ПП РФ № 941)',
    'от 20&nbsp;000 рублей' => 'от 35 000 ₽ за один класс МКТУ (пп. 2.1+2.4+2.11, ПП РФ № 941)',
    'от 20 000 руб.' => 'от 35 000 ₽ за один класс МКТУ',
    'от 20000 рублей' => 'от 35 000 ₽ за один класс МКТУ',
    'составляет от 20 000' => 'составляет от 35 000 ₽ за класс',
);

$tables = array(
    array('table' => 'pages', 'slug' => 'registracija_torgovyh_marok_i_logotipov', 'col' => 'full_story'),
    array('table' => 'news', 'slug' => null, 'col' => 'full_story'),
);

$report = array('hits' => array(), 'updated' => array());
foreach ($tables as $spec) {
    if ($spec['slug'] !== null) {
        $st = $mysqli->prepare("SELECT id, seo_url, full_story FROM `{$spec['table']}` WHERE seo_url=? LIMIT 1");
        $st->bind_param('s', $spec['slug']);
        $st->execute();
        $rows = $st->get_result()->fetch_all(MYSQLI_ASSOC);
    } else {
        $q = $mysqli->query(
            "SELECT id, seo_url, full_story FROM news WHERE full_story LIKE '%20 000%'"
            . " OR full_story LIKE '%20&nbsp;000%' OR full_story LIKE '%20000%'"
        );
        $rows = array();
        while ($r = $q->fetch_assoc()) {
            $rows[] = $r;
        }
    }
    foreach ($rows as $row) {
        $body = $row['full_story'];
        $newBody = $body;
        foreach ($patterns as $from => $to) {
            if (strpos($newBody, $from) !== false) {
                $newBody = str_replace($from, $to, $newBody);
            }
        }
        if ($newBody !== $body) {
            $report['hits'][] = array('table' => $spec['table'], 'id' => $row['id'], 'seo_url' => $row['seo_url']);
            if ($apply) {
                if ($dumpPath !== '' && $spec['table'] === 'pages' && $row['seo_url'] === 'registracija_torgovyh_marok_i_logotipov') {
                    file_put_contents($dumpPath, $mysqli->real_escape_string($body));
                }
                $up = $mysqli->prepare("UPDATE `{$spec['table']}` SET full_story=? WHERE id=?");
                $up->bind_param('si', $newBody, $row['id']);
                $up->execute();
                $report['updated'][] = $row['seo_url'];
            }
        }
    }
}
echo json_encode($report, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . "\n";
