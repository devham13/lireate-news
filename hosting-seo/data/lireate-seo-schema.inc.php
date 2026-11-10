<?php
/**
 * JSON-LD + article context for LIREATE SEO (used with lireate-seo-head.inc.php).
 */

if (!function_exists('lireate_seo_schema_h')) {
    function lireate_seo_schema_h($s)
    {
        return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
    }
}

if (!function_exists('lireate_seo_schema_public_base')) {
    function lireate_seo_schema_public_base()
    {
        if (function_exists('lireate_seo_public_base')) {
            return lireate_seo_public_base();
        }
        $host = isset($_SERVER['HTTP_HOST']) ? (string) $_SERVER['HTTP_HOST'] : 'example.invalid';
        $host = preg_replace('/^www\./i', '', $host);
        return 'https://' . $host;
    }
}

if (!function_exists('lireate_seo_datetime_to_iso')) {
    function lireate_seo_datetime_to_iso($unix, $displayFallback = '')
    {
        $unix = (int) $unix;
        if ($unix > 0) {
            return gmdate('Y-m-d', $unix) . 'T12:00:00+03:00';
        }
        $displayFallback = trim((string) $displayFallback);
        if ($displayFallback !== '' && preg_match('/^(\d{2})\.(\d{2})\.(\d{4})$/', $displayFallback, $m)) {
            return $m[3] . '-' . $m[2] . '-' . $m[1] . 'T12:00:00+03:00';
        }
        return '';
    }
}

if (!function_exists('lireate_seo_extract_faq_pairs')) {
    function lireate_seo_extract_faq_pairs($html)
    {
        $html = (string) $html;
        if ($html === '') {
            return array();
        }
        $section = $html;
        if (preg_match('/<h2[^>]*>\s*Частые вопросы\s*<\/h2>(.*)$/isu', $html, $m)) {
            $section = $m[1];
        } else {
            return array();
        }
        $pairs = array();
        if (!preg_match_all('/<h3[^>]*>(.*?)<\/h3>\s*<(p|div)[^>]*>(.*?)<\/\2>/isu', $section, $matches, PREG_SET_ORDER)) {
            return array();
        }
        foreach ($matches as $match) {
            $q = trim(strip_tags($match[1]));
            $a = trim(strip_tags($match[3]));
            if ($q === '' || $a === '') {
                continue;
            }
            $pairs[] = array('question' => $q, 'answer' => $a);
            if (count($pairs) >= 12) {
                break;
            }
        }
        return $pairs;
    }
}

if (!function_exists('lireate_seo_first_https_image')) {
    function lireate_seo_first_https_image($html, $coverHtml = '')
    {
        $candidates = array((string) $coverHtml, (string) $html);
        foreach ($candidates as $chunk) {
            if ($chunk === '') {
                continue;
            }
            if (preg_match('/<img[^>]+src=["\']([^"\']+)["\']/iu', $chunk, $m)) {
                $src = trim($m[1]);
                if ($src === '') {
                    continue;
                }
                if (preg_match('#^https?://#i', $src)) {
                    return preg_replace('#^http:#i', 'https:', $src);
                }
                $base = lireate_seo_schema_public_base();
                return $base . '/' . ltrim($src, '/');
            }
        }
        return '';
    }
}

if (!function_exists('lireate_seo_jsonld_encode')) {
    function lireate_seo_jsonld_encode($data)
    {
        $json = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        if ($json === false) {
            return '';
        }
        json_decode($json);
        if (json_last_error() !== JSON_ERROR_NONE) {
            return '';
        }
        return $json;
    }
}

if (!function_exists('lireate_seo_home_organization')) {
    function lireate_seo_home_organization()
    {
        $base = lireate_seo_schema_public_base();
        return array(
            '@context' => 'https://schema.org',
            '@graph' => array(
                array(
                    '@type' => 'Organization',
                    '@id' => $base . '/#organization',
                    'name' => 'ООО «ЛИРЕЙТ»',
                    'legalName' => 'ООО «ЛИРЕЙТ»',
                    'url' => $base . '/',
                    'email' => 'info@' . 'lireate' . '.' . 'ru',
                    'telephone' => array('+7-499-938-45-95', '+7-960-048-49-57'),
                    'address' => array(
                        '@type' => 'PostalAddress',
                        'streetAddress' => 'ул. Карла Маркса, 24, оф. 1',
                        'addressLocality' => 'Зеленодольск',
                        'addressCountry' => 'RU',
                    ),
                ),
                array(
                    '@type' => 'LegalService',
                    '@id' => $base . '/#legalservice',
                    'name' => 'ЛИРЕЙТ — патентное бюро',
                    'url' => $base . '/',
                    'provider' => array('@id' => $base . '/#organization'),
                    'areaServed' => 'RU',
                    'address' => array(
                        '@type' => 'PostalAddress',
                        'streetAddress' => 'ул. Королёва, 11Б, помещ. 30-1005',
                        'addressLocality' => 'Зеленодольск',
                        'addressCountry' => 'RU',
                    ),
                ),
            ),
        );
    }
}

if (!function_exists('lireate_seo_bind_news_article')) {
    function lireate_seo_bind_news_article($row, $seo = array())
    {
        if (!is_array($row)) {
            return;
        }
        $base = lireate_seo_schema_public_base();
        $seoUrl = isset($row['seo_url']) ? trim((string) $row['seo_url']) : '';
        $canonical = $seoUrl !== '' ? $base . '/' . trim($seoUrl, '/') . '/' : '';
        if (!empty($GLOBALS['lireate_canonical_url'])) {
            $canonical = $GLOBALS['lireate_canonical_url'];
        }
        $title = isset($seo['seo_title']) ? $seo['seo_title'] : (isset($row['seo_title']) ? $row['seo_title'] : (isset($row['name']) ? $row['name'] : ''));
        $desc = isset($seo['seo_description']) ? $seo['seo_description'] : (isset($row['seo_description']) ? $row['seo_description'] : '');
        $displayDate = !empty($row['datetime']) ? date('d.m.Y', (int) $row['datetime']) : '';
        $iso = lireate_seo_datetime_to_iso(isset($row['datetime']) ? $row['datetime'] : 0, $displayDate);
        $body = isset($row['full_story']) ? (string) $row['full_story'] : '';
        $image = lireate_seo_first_https_image($body, '');
        $GLOBALS['lireate_seo_article'] = array(
            'title' => $title,
            'description' => $desc,
            'canonical' => $canonical,
            'date_iso' => $iso,
            'date_modified_iso' => $iso,
            'image' => $image,
            'body_html' => $body,
            'author' => defined('LIREATE_BLOG_AUTHOR_NAME') ? LIREATE_BLOG_AUTHOR_NAME : 'Юрий Горбачев',
            'author_role' => defined('LIREATE_BLOG_AUTHOR_ROLE') ? LIREATE_BLOG_AUTHOR_ROLE : 'Генеральный директор',
            'author_url' => $base . '/avtor/',
        );
        $GLOBALS['lireate_seo_og'] = array(
            'type' => 'article',
            'title' => $title,
            'description' => $desc,
            'url' => $canonical,
            'image' => $image !== '' ? $image : $base . '/images/OG_image.jpg',
        );
    }
}

if (!function_exists('lireate_seo_build_article_graph')) {
    function lireate_seo_build_article_graph($meta)
    {
        $base = lireate_seo_schema_public_base();
        $canonical = isset($meta['canonical']) ? $meta['canonical'] : '';
        $title = isset($meta['title']) ? $meta['title'] : '';
        $desc = isset($meta['description']) ? $meta['description'] : '';
        $iso = isset($meta['date_iso']) ? $meta['date_iso'] : '';
        $modified = isset($meta['date_modified_iso']) ? $meta['date_modified_iso'] : $iso;
        $image = isset($meta['image']) ? $meta['image'] : '';
        if ($image === '' && isset($meta['body_html'])) {
            $image = lireate_seo_first_https_image($meta['body_html'], isset($meta['cover_html']) ? $meta['cover_html'] : '');
        }
        $author = isset($meta['author']) ? $meta['author'] : 'Юрий Горбачев';
        $authorRole = isset($meta['author_role']) ? $meta['author_role'] : '';
        $authorUrl = isset($meta['author_url']) ? $meta['author_url'] : ($base . '/avtor/');
        $article = array(
            '@type' => 'Article',
            '@id' => $canonical !== '' ? $canonical . '#article' : null,
            'headline' => $title,
            'description' => $desc,
            'author' => array_filter(array(
                '@type' => 'Person',
                'name' => $author,
                'jobTitle' => $authorRole !== '' ? $authorRole : null,
                'url' => $authorUrl,
            )),
            'datePublished' => $iso !== '' ? $iso : null,
            'dateModified' => $modified !== '' ? $modified : null,
            'mainEntityOfPage' => $canonical !== '' ? array('@type' => 'WebPage', '@id' => $canonical) : null,
            'image' => $image !== '' ? array($image) : null,
            'publisher' => array(
                '@type' => 'Organization',
                'name' => 'ООО «ЛИРЕЙТ»',
                'url' => $base . '/',
            ),
        );
        $article = array_filter($article, function ($v) {
            return $v !== null && $v !== '';
        });
        $graph = array(
            '@context' => 'https://schema.org',
            '@graph' => array(
                array_filter(array(
                    '@type' => 'WebPage',
                    '@id' => $canonical,
                    'url' => $canonical,
                    'name' => $title,
                    'description' => $desc,
                    'isPartOf' => array('@type' => 'WebSite', 'url' => $base . '/', 'name' => 'ЛИРЕЙТ'),
                )),
                $article,
            ),
        );
        if ($canonical !== '') {
            $graph['@graph'][] = array(
                '@type' => 'BreadcrumbList',
                'itemListElement' => array(
                    array('@type' => 'ListItem', 'position' => 1, 'name' => 'Главная', 'item' => $base . '/'),
                    array('@type' => 'ListItem', 'position' => 2, 'name' => 'Блог', 'item' => $base . '/news'),
                    array('@type' => 'ListItem', 'position' => 3, 'name' => $title, 'item' => $canonical),
                ),
            );
        }
        $faqSource = isset($meta['body_html']) ? $meta['body_html'] : '';
        $faq = lireate_seo_extract_faq_pairs($faqSource);
        if (!empty($faq)) {
            $mainEntity = array();
            foreach ($faq as $pair) {
                $mainEntity[] = array(
                    '@type' => 'Question',
                    'name' => $pair['question'],
                    'acceptedAnswer' => array(
                        '@type' => 'Answer',
                        'text' => $pair['answer'],
                    ),
                );
            }
            $graph['@graph'][] = array(
                '@type' => 'FAQPage',
                'mainEntity' => $mainEntity,
            );
        }
        return $graph;
    }
}

if (!function_exists('lireate_seo_render_article_schema_scripts')) {
    function lireate_seo_render_article_schema_scripts($meta)
    {
        if (!empty($GLOBALS['lireate_seo_schema_rendered'])) {
            return;
        }
        if (!empty($meta['body_html']) && empty($meta['image'])) {
            $meta['image'] = lireate_seo_first_https_image(
                $meta['body_html'],
                isset($meta['cover_html']) ? $meta['cover_html'] : ''
            );
        }
        $graph = lireate_seo_build_article_graph($meta);
        $json = lireate_seo_jsonld_encode($graph);
        if ($json === '') {
            return;
        }
        echo '<script type="application/ld+json">' . $json . "</script>\n";
        $GLOBALS['lireate_seo_schema_rendered'] = true;
    }
}
