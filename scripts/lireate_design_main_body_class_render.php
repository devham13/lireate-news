#!/usr/bin/env php
<?php
/**
 * Simulate rendered <body class="..."> from main.php inline body PHP (design verify selftest).
 * Usage: main_body_class_render.php MAIN.php PAGE REQUEST_URI
 */
if ($argc < 4) {
    fwrite(STDERR, "Usage: {$argv[0]} main.php page request_uri\n");
    exit(2);
}
$main = $argv[1];
$page = $argv[2];
$uri = $argv[3];
$text = file_get_contents($main);
if ($text === false) {
    fwrite(STDERR, "read fail\n");
    exit(1);
}
if (!preg_match('/<body\s+class="cms-default\s*<\?php([\s\S]*?)\?>\s*"/i', $text, $m)) {
    fwrite(STDERR, "BODY_INLINE_PHP_NOT_FOUND\n");
    exit(1);
}
$inline = $m[1];
$temp = array('page' => $page);
$_SERVER['REQUEST_URI'] = $uri;
ob_start();
eval($inline);
$extra = ob_get_clean();
echo "cms-default" . $extra;
