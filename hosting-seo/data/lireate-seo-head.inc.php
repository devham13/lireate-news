<?php
/** Echo canonical + robots meta when lireate_seo_init_globals() ran. */
if (!function_exists('lireate_seo_render_head_tags')) {
    function lireate_seo_render_head_tags()
    {
        if (!empty($GLOBALS['lireate_canonical_url']) && strpos($GLOBALS['lireate_canonical_url'], '/404') === false) {
            $c = htmlspecialchars($GLOBALS['lireate_canonical_url'], ENT_QUOTES, 'UTF-8');
            echo '<link rel="canonical" href="' . $c . "\" />\n";
        }
        if (!empty($GLOBALS['lireate_robots_noindex'])) {
            echo '<meta name="robots" content="noindex, follow" />' . "\n";
        }
    }
}
