<?php
/**
 * Apply blog SEO meta updates from JSON (wave fixes). CLI only.
 *
 *   php lireate_blog_seo_apply.php <DOCROOT> <plan.json> [--dry-run] [--backup-dir DIR]
 *
 * Touches only: name, seo_title, seo_description, category (when set), short_story (when set).
 * Does not change datetime, seo_url, full_story unless plan row sets full_story (owner review).
 */
if (php_sapi_name() !== 'cli') {
    exit(2);
}

$GLOBALS['lireate_db_publish_embedded'] = true;
require_once __DIR__ . '/lireate_db_publish.php';

function lireate_blog_seo_apply_usage()
{
    fwrite(STDERR, "usage: php lireate_blog_seo_apply.php DOCROOT plan.json [--dry-run] [--backup-dir DIR]\n");
    exit(2);
}

$docroot = isset($argv[1]) ? $argv[1] : '';
$planFile = isset($argv[2]) ? $argv[2] : '';
if ($docroot === '' || $planFile === '' || !is_file($planFile)) {
    lireate_blog_seo_apply_usage();
}
$dry = in_array('--dry-run', $argv, true);
$backupDir = '';
foreach ($argv as $i => $arg) {
    if ($arg === '--backup-dir' && isset($argv[$i + 1])) {
        $backupDir = $argv[$i + 1];
    }
}

$plan = json_decode(file_get_contents($planFile), true);
if (!is_array($plan) || empty($plan['articles'])) {
    echo json_encode(array('ok' => false, 'error' => 'bad plan'), JSON_UNESCAPED_UNICODE) . "\n";
    exit(2);
}

$mysqli = lireate_mysqli($docroot);
$updated = 0;
$skipped = array();
$changes = array();

$backupFp = null;
if ($backupDir !== '' && !$dry) {
    if (!is_dir($backupDir)) {
        mkdir($backupDir, 0755, true);
    }
    $backupFp = fopen(rtrim($backupDir, '/') . '/news_seo_rollback.sql', 'w');
    fwrite($backupFp, "-- rollback generated " . date('c') . "\n");
}

foreach ($plan['articles'] as $row) {
    if (empty($row['seo_url'])) {
        continue;
    }
    $slug = trim(str_replace('/', '', (string) $row['seo_url']));
    $st = $mysqli->prepare('SELECT `id`,`name`,`seo_title`,`seo_description`,`category` FROM `news` WHERE `seo_url`=? AND `active`=1 LIMIT 1');
    $st->bind_param('s', $slug);
    $st->execute();
    $res = $st->get_result();
    $cur = $res ? $res->fetch_assoc() : null;
    $st->close();
    if (!$cur) {
        $skipped[] = array('seo_url' => $slug, 'reason' => 'not_found');
        continue;
    }
    $after = $cur;
    if (!empty($row['seo_title'])) {
        $after['seo_title'] = (string) $row['seo_title'];
    }
    if (!empty($row['seo_description'])) {
        $after['seo_description'] = (string) $row['seo_description'];
    }
    if (!empty($row['name'])) {
        $after['name'] = (string) $row['name'];
    }
    if (isset($row['category']) && (int) $row['category'] > 0) {
        $after['category'] = (int) $row['category'];
    }
    $same = ($after['seo_title'] === $cur['seo_title']
        && $after['seo_description'] === $cur['seo_description']
        && $after['name'] === $cur['name']
        && (int) $after['category'] === (int) $cur['category']);
    if ($same) {
        $skipped[] = array('seo_url' => $slug, 'reason' => 'no_change');
        continue;
    }
    $changes[] = array('id' => $cur['id'], 'seo_url' => $slug, 'before' => $cur, 'after' => $after);
    if ($backupFp) {
        $escName = $mysqli->real_escape_string($cur['name']);
        $escTitle = $mysqli->real_escape_string($cur['seo_title']);
        $escDesc = $mysqli->real_escape_string($cur['seo_description']);
        $id = (int) $cur['id'];
        fwrite(
            $backupFp,
            "UPDATE `news` SET `name`='{$escName}',`seo_title`='{$escTitle}',"
            . "`seo_description`='{$escDesc}',`category`=" . (int) $cur['category']
            . " WHERE `id`={$id};\n"
        );
    }
    if (!$dry) {
        $up = $mysqli->prepare('UPDATE `news` SET `name`=?, `seo_title`=?, `seo_description`=?, `category`=? WHERE `id`=? AND `seo_url`=?');
        $up->bind_param(
            'sssiss',
            $after['name'],
            $after['seo_title'],
            $after['seo_description'],
            $after['category'],
            $cur['id'],
            $slug
        );
        $up->execute();
        $up->close();
    }
    $updated++;
}

if ($backupFp) {
    fclose($backupFp);
}
$mysqli->close();

$report = array(
    'ok' => true,
    'dry_run' => $dry,
    'updated' => $updated,
    'skipped' => $skipped,
    'changes_count' => count($changes),
);
echo json_encode($report, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . "\n";