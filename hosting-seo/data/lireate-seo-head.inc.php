<?php
/**
 * Canonical, robots, Open Graph, home Organization JSON-LD (articles: JSON-LD in layout tail).
 */

if (!function_exists('lireate_seo_bootstrap')) {
    function lireate_seo_bootstrap()
    {
        static $done = false;
        if ($done) {
            return;
        }
        $dataDir = dirname(__FILE__);
        $runtime = $dataDir . '/lireate-seo-runtime.php';
        $schema = $dataDir . '/lireate-seo-schema.inc.php';
        if (is_file($runtime)) {
            require_once $runtime;
        }
        if (is_file($schema)) {
            require_once $schema;
        }
        if (function_exists('lireate_seo_init_globals')) {
            lireate_seo_init_globals();
        }
        $done = true;
    }
}

if (!function_exists('lireate_seo_render_head_tags')) {
    function lireate_seo_render_head_tags()
    {
        lireate_seo_bootstrap();

        if (!empty($GLOBALS['lireate_canonical_url']) && strpos($GLOBALS['lireate_canonical_url'], '/404') === false) {
            $c = htmlspecialchars($GLOBALS['lireate_canonical_url'], ENT_QUOTES, 'UTF-8');
            echo '<link rel="canonical" href="' . $c . "\" />\n";
        }
        if (!empty($GLOBALS['lireate_robots_noindex'])) {
            echo '<meta name="robots" content="noindex, follow" />' . "\n";
        }

        $og = !empty($GLOBALS['lireate_seo_og']) && is_array($GLOBALS['lireate_seo_og'])
            ? $GLOBALS['lireate_seo_og']
            : null;

        $path = function_exists('lireate_seo_request_path') ? lireate_seo_request_path() : '/';
        $isHome = ($path === '/' || $path === '');
        if ($og === null && $isHome) {
            $base = function_exists('lireate_seo_schema_public_base')
                ? lireate_seo_schema_public_base()
                : 'https://example.invalid';
            $og = array(
                'type' => 'website',
                'title' => 'ООО «ЛИРЕЙТ» — регистрация товарных знаков',
                'description' => 'Патентное бюро в Зеленодольске: регистрация и защита товарных знаков, международные заявки, сопровождение в Роспатенте.',
                'url' => $base . '/',
                'image' => $base . '/images/OG_image.jpg',
            );
        }

        if ($og !== null) {
            $GLOBALS['lireate_seo_og_done'] = true;
            $type = isset($og['type']) ? $og['type'] : 'website';
            $title = isset($og['title']) ? $og['title'] : '';
            $desc = isset($og['description']) ? $og['description'] : '';
            $url = isset($og['url']) ? $og['url'] : '';
            $image = isset($og['image']) ? $og['image'] : '';
            if ($url !== '') {
                echo '<meta property="og:url" content="' . htmlspecialchars($url, ENT_QUOTES, 'UTF-8') . "\" />\n";
            }
            echo '<meta property="og:type" content="' . htmlspecialchars($type, ENT_QUOTES, 'UTF-8') . "\" />\n";
            if ($title !== '') {
                echo '<meta property="og:title" content="' . htmlspecialchars($title, ENT_QUOTES, 'UTF-8') . "\" />\n";
            }
            if ($desc !== '') {
                echo '<meta property="og:description" content="' . htmlspecialchars($desc, ENT_QUOTES, 'UTF-8') . "\" />\n";
            }
            if ($image !== '') {
                $image = preg_replace('#^http:#i', 'https:', $image);
                echo '<meta property="og:image" content="' . htmlspecialchars($image, ENT_QUOTES, 'UTF-8') . "\" />\n";
            }
            if ($type === 'article' && !empty($GLOBALS['lireate_seo_article']['date_iso'])) {
                echo '<meta property="article:published_time" content="' . htmlspecialchars(
                    $GLOBALS['lireate_seo_article']['date_iso'],
                    ENT_QUOTES,
                    'UTF-8'
                ) . "\" />\n";
            }
        }

        if ($isHome && function_exists('lireate_seo_home_organization')) {
            $json = lireate_seo_jsonld_encode(lireate_seo_home_organization());
            if ($json !== '') {
                echo '<script type="application/ld+json">' . $json . "</script>\n";
            }
        }
    }
}
