<?php
/**
 * LIREATE SEO runtime: canonical + noindex from REQUEST_URI (not $page — CMS sets $page=pages|404).
 */
if (!function_exists('lireate_seo_public_base')) {
    function lireate_seo_public_base()
    {
        $host = isset($_SERVER['HTTP_HOST']) ? (string) $_SERVER['HTTP_HOST'] : 'example.invalid';
        $host = preg_replace('/^www\./i', '', $host);
        return 'https://' . $host;
    }
}

if (!function_exists('lireate_seo_request_path')) {
    function lireate_seo_request_path()
    {
        $uri = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '/';
        $path = parse_url($uri, PHP_URL_PATH);
        if ($path === false || $path === null || $path === '') {
            return '/';
        }
        return $path;
    }
}

if (!function_exists('lireate_seo_cms_slashless')) {
    function lireate_seo_cms_slashless()
    {
        return array(
            'news', 'kontaktyi', 'docs', 'team', 'mktu', 'patent', 'patent_prom_obr',
            'reviews', 'portfolio', 'o_kompanii', 'partners', 'payment', 'personalArea',
            'spasibo', 'reg-tz-main',
        );
    }
}

if (!function_exists('lireate_seo_service_with_slash')) {
    function lireate_seo_service_with_slash()
    {
        return array(
            'registraciya_tovarnogo_znaka',
            'registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat',
            'findtz',
            'prodlenie_tovarnogo_znaka',
            'poisk_tovarnyh_znakov',
            'ekspertiza_tovarnogo_znaka',
            'mezhdunarodnaja_registracija_tovarnogo_znaka',
            'registracija_torgovyh_marok_i_logotipov',
            'avtor',
        );
    }
}

if (!function_exists('lireate_seo_noindex_paths')) {
    function lireate_seo_noindex_paths()
    {
        return array(
            '/test', '/test2', '/test3', '/tester', '/check', '/docs2',
            '/personalArea', '/payment', '/pdf_book_1', '/blog', '/spasibo',
            '/goods/8', '/goods/8/', '/goods/11', '/goods/11/',
        );
    }
}

if (!function_exists('lireate_seo_canonical_from_path')) {
    function lireate_seo_canonical_from_path($request_path)
    {
        $base = lireate_seo_public_base();
        $path = (string) $request_path;
        $trimmed = trim($path, '/');
        if ($trimmed === '') {
            return $base . '/';
        }

        $segments = explode('/', $trimmed);
        $first = $segments[0];

        if ($first === '404' || $first === 'pages') {
            return '';
        }

        if (count($segments) === 1 && in_array($first, lireate_seo_cms_slashless(), true)) {
            return $base . '/' . $first;
        }

        if (count($segments) === 1 && in_array($first, lireate_seo_service_with_slash(), true)) {
            return $base . '/' . $first . '/';
        }

        // Sitemap articles and legacy slugs: single path segment + trailing slash.
        if (count($segments) === 1 && preg_match('/^[a-zA-Z0-9_\-]+$/', $first)) {
            return $base . '/' . $first . '/';
        }

        return $base . '/' . $trimmed . '/';
    }
}

if (!function_exists('lireate_seo_https_url')) {
    function lireate_seo_https_url($url)
    {
        $url = trim((string) $url);
        if ($url === '') {
            return '';
        }
        return preg_replace('#^http:#i', 'https:', $url);
    }
}

if (!function_exists('lireate_seo_page_kind')) {
    /**
     * @return string home|cms|service|article|other
     */
    function lireate_seo_page_kind($request_path = null)
    {
        $path = $request_path !== null ? (string) $request_path : lireate_seo_request_path();
        $trimmed = trim($path, '/');
        if ($trimmed === '') {
            return 'home';
        }
        $segments = explode('/', $trimmed);
        $first = $segments[0];
        if (count($segments) === 1) {
            if (in_array($first, lireate_seo_cms_slashless(), true)) {
                return 'cms';
            }
            if (in_array($first, lireate_seo_service_with_slash(), true)) {
                return 'service';
            }
            if (preg_match('/^[a-zA-Z0-9_\-]+$/', $first)) {
                return 'article';
            }
        }
        return 'other';
    }
}

if (!function_exists('lireate_seo_default_og_image')) {
    function lireate_seo_default_og_image()
    {
        return lireate_seo_https_url(lireate_seo_public_base() . '/images/OG_image.jpg');
    }
}

if (!function_exists('lireate_seo_init_globals')) {
    function lireate_seo_init_globals()
    {
        $path = lireate_seo_request_path();
        $path_norm = rtrim($path, '/');
        if ($path_norm === '') {
            $path_norm = '/';
        }

        $GLOBALS['lireate_robots_noindex'] = false;
        foreach (lireate_seo_noindex_paths() as $ni) {
            $ni_norm = rtrim($ni, '/');
            if ($path_norm === $ni_norm || $path === $ni || $path === $ni . '/') {
                $GLOBALS['lireate_robots_noindex'] = true;
                break;
            }
        }

        $qs = isset($_SERVER['QUERY_STRING']) ? (string) $_SERVER['QUERY_STRING'] : '';
        if (preg_match('/(^|&)test($|=)/i', $qs) || preg_match('/(^|&)mode=/i', $qs)) {
            $GLOBALS['lireate_robots_noindex'] = true;
        }

        $GLOBALS['lireate_canonical_url'] = lireate_seo_canonical_from_path($path);
    }
}

if (!function_exists('lireate_seo_ob_filter_html')) {
    function lireate_seo_ob_filter_html($html)
    {
        $html = preg_replace_callback(
            '/\s*(<meta\s+property="og:image"[^>]*>\s*)'
            . '(?:<meta\s+property="og:image:type"[^>]*>\s*)?'
            . '(?:<meta\s+property="og:image:width"[^>]*>\s*)?'
            . '(?:<meta\s+property="og:image:height"[^>]*>\s*)?/is',
            function ($m) {
                if (stripos($m[0], 'http://') !== false) {
                    return "\n";
                }
                return $m[0];
            },
            $html
        );

        $path = function_exists('lireate_seo_request_path') ? lireate_seo_request_path() : '';
        if ($path === '/avtor' || $path === '/avtor/') {
            $_meta_inc = dirname(__FILE__) . '/lireate-seo-page-meta.inc.php';
            if (is_file($_meta_inc)) {
                require_once $_meta_inc;
            }
            $static = function_exists('lireate_seo_static_page_meta')
                ? lireate_seo_static_page_meta('avtor')
                : null;
            if (is_array($static)) {
                if (!empty($static['title'])) {
                    $t = htmlspecialchars((string) $static['title'], ENT_QUOTES, 'UTF-8');
                    $html = preg_replace('/<title>[^<]*<\\/title>/i', '<title>' . $t . '</title>', $html, 1);
                }
                if (!empty($static['description'])) {
                    $d = htmlspecialchars((string) $static['description'], ENT_QUOTES, 'UTF-8');
                    $html = preg_replace(
                        '/<meta\\s+name="description"\\s+content="[^"]*"/i',
                        '<meta name="description" content="' . $d . '"',
                        $html,
                        1
                    );
                }
            }

            // Fallback when template/main.php omits page_container (other deploy in flight).
            if (stripos($html, 'id="lireate-avtor"') === false) {
                $inc = isset($_SERVER['DOCUMENT_ROOT'])
                    ? $_SERVER['DOCUMENT_ROOT'] . '/pages/avtor-page.inc.php'
                    : '';
                if ($inc !== '' && is_file($inc)) {
                    ob_start();
                    require $inc;
                    if (function_exists('lireate_avtor_jsonld')) {
                        $base = function_exists('lireate_seo_schema_public_base')
                            ? lireate_seo_schema_public_base()
                            : lireate_seo_public_base();
                        $json = json_encode(
                            lireate_avtor_jsonld($base),
                            JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES
                        );
                        echo '<script type="application/ld+json">' . $json . "</script>\n";
                    }
                    $block = (string) ob_get_clean();
                    $needle = '<div class="container text-center content" style="padding-right: 0px;">';
                    $pos = stripos($html, $needle);
                    if ($pos !== false && $block !== '') {
                        $insertAt = $pos + strlen($needle);
                        $wrap = "\n<div class=\"row\"><div class=\"col-xs-12\"><div class=\"page_container\">\n"
                            . $block
                            . "\n</div></div></div>\n";
                        $html = substr($html, 0, $insertAt) . $wrap . substr($html, $insertAt);
                    }
                }
            }

        }

        return $html;
    }
}

lireate_seo_init_globals();

if (PHP_SAPI !== 'cli' && empty($GLOBALS['lireate_seo_outer_ob'])) {
    $GLOBALS['lireate_seo_outer_ob'] = true;
    ob_start('lireate_seo_ob_filter_html');
}
