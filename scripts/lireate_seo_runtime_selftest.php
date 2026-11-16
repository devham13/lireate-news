<?php
/**
 * CLI assertions for hosting-seo/data/lireate-seo-runtime.php (PHP 5.6+).
 */
$root = dirname(__DIR__);
$runtime = $root . '/hosting-seo/data/lireate-seo-runtime.php';
if (!is_file($runtime)) {
    fwrite(STDERR, "missing runtime: $runtime\n");
    exit(1);
}

$failures = 0;

/**
 * @param string $label
 * @param string $uri
 * @param array $get
 * @param bool|null $preset_noindex
 * @param string $expect_canonical
 * @param bool $expect_noindex
 */
function lireate_seo_selftest_case($label, $uri, $get, $preset_noindex, $expect_canonical, $expect_noindex)
{
    global $failures;

    $_SERVER['HTTP_HOST'] = 'example.test';
    $_SERVER['REQUEST_URI'] = $uri;
    $_SERVER['QUERY_STRING'] = '';
    if (!empty($get)) {
        $_SERVER['QUERY_STRING'] = http_build_query($get);
    }
    $_GET = $get;
    $GLOBALS['lireate_robots_noindex'] = $preset_noindex ? true : false;
    unset($GLOBALS['lireate_canonical_url']);

    lireate_seo_init_globals();

    $canonical = isset($GLOBALS['lireate_canonical_url']) ? (string) $GLOBALS['lireate_canonical_url'] : '';
    $noindex = !empty($GLOBALS['lireate_robots_noindex']);

    if ($canonical !== $expect_canonical || $noindex !== $expect_noindex) {
        fwrite(STDERR, "FAIL [$label]\n");
        fwrite(STDERR, "  canonical: got [$canonical] want [$expect_canonical]\n");
        fwrite(STDERR, "  noindex:   got [" . ($noindex ? 'true' : 'false') . "] want [" . ($expect_noindex ? 'true' : 'false') . "]\n");
        $failures++;
        return;
    }
    fwrite(STDOUT, "OK   [$label]\n");
}

$_SERVER['HTTP_HOST'] = 'example.test';
$_SERVER['REQUEST_URI'] = '/news';
$_GET = array();
require $runtime;

$base = 'https://example.test';

lireate_seo_selftest_case('news index', '/news', array(), null, $base . '/news', false);
lireate_seo_selftest_case('news page 2 query', '/news?page=2', array('page' => '2'), null, $base . '/news?page=2', false);
lireate_seo_selftest_case('news filtered page', '/news?page=27&category=x', array('page' => '27', 'category' => 'x'), null, $base . '/news', false);
lireate_seo_selftest_case('news invalid page abc', '/news?page=abc', array('page' => 'abc'), null, $base . '/news', true);
lireate_seo_selftest_case('news invalid page zero', '/news?page=0', array('page' => '0'), null, $base . '/news', true);
lireate_seo_selftest_case('news invalid page preset noindex', '/news?page=abc', array('page' => 'abc'), true, $base . '/news', true);
lireate_seo_selftest_case('news path pagination', '/news/page/2/', array(), null, $base . '/news', true);
lireate_seo_selftest_case('article slug', '/some_article/', array(), null, $base . '/some_article/', false);

exit($failures === 0 ? 0 : 1);