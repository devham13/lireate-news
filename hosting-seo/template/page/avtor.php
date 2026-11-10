<?php
/**
 * /avtor — страница автора (Юрий Горбачев).
 */
$inc = $_SERVER['DOCUMENT_ROOT'] . '/pages/avtor-page.inc.php';
if (is_file($inc)) {
    require $inc;
    if (function_exists('lireate_avtor_jsonld')) {
        $base = function_exists('lireate_seo_schema_public_base')
            ? lireate_seo_schema_public_base()
            : 'https://example.invalid';
        $json = json_encode(lireate_avtor_jsonld($base), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        echo '<script type="application/ld+json">' . $json . "</script>\n";
    }
} else {
    echo '<section><h1>Автор</h1><p>Страница в настройке.</p></section>';
}
