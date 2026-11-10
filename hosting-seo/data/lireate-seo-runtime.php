<?php
/**
 * LIREATE SEO runtime (2026-11-10): canonical URL + noindex flag for CMS template.
 * Included from index.php before template(); does not touch DB.
 */

if (!function_exists('lireate_seo_public_base')) {
    function lireate_seo_public_base()
    {
        $host = isset($_SERVER['HTTP_HOST']) ? (string) $_SERVER['HTTP_HOST'] : 'lireate.com';
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
    /** Pages where trailing slash breaks routing / title (not sitemap article slugs). */
    function lireate_seo_cms_slashless()
    {
        return array(
            'news', 'kontaktyi', 'docs', 'team', 'mktu', 'patent', 'patent_prom_obr',
            'reviews', 'portfolio', 'o_kompanii', 'partners', 'payment', 'personalArea',
            'spasibo', 'reg-tz-main', 'poisk_tovarnyh_znakov', 'ekspertiza_tovarnogo_znaka',
            'mezhdunarodnaja_registracija_tovarnogo_znaka',
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

if (!function_exists('lireate_seo_compute_canonical')) {
    /**
     * @param string $page CMS view slug (from $_GET['view'] or home)
     */
    function lireate_seo_compute_canonical($page, $request_path)
    {
        $base = lireate_seo_public_base();
        $page = trim((string) $page, '/');

        if ($request_path === '/' || $page === '' || $page === $GLOBALS['cfg']['home_url']) {
            return $base . '/';
        }

        if (in_array($page, lireate_seo_cms_slashless(), true)) {
            return $base . '/' . rawurlencode($page);
        }

        if (in_array($page, lireate_seo_service_with_slash(), true)) {
            return $base . '/' . $page . '/';
        }

        // Blog / news articles (sitemap: trailing slash).
        if (preg_match('/^[a-zA-Z0-9_\-]+$/', $page)) {
            return $base . '/' . $page . '/';
        }

        return $base . $request_path;
    }
}

if (!function_exists('lireate_seo_init_globals')) {
    function lireate_seo_init_globals($page)
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

        $GLOBALS['lireate_canonical_url'] = lireate_seo_compute_canonical($page, $path);
    }
}

if (isset($page)) {
    lireate_seo_init_globals($page);
}
