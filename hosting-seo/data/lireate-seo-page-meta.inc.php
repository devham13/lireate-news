<?php
/**
 * Статический title / description / og:image для CMS-страниц (когда правка БД отложена или для канона).
 */
if (!function_exists('lireate_seo_static_page_meta')) {
    function lireate_seo_static_page_meta($slug)
    {
        $slug = trim((string) $slug, '/');
        $pages = array(
            'avtor' => array(
                'title' => 'Горбачев Юрий Александрович — директор бюро «Лирейт»',
                'description' => 'Юрий Горбачев — директор и управляющий партнёр ООО «ЛИРЕЙТ»: товарные знаки, патенты, авторское право и споры. Статьи на vc.ru, в Т—Ж, на Клерке и Хабре.',
                'image' => '/template/images/team/person/11.jpg',
            ),
        );
        return isset($pages[$slug]) ? $pages[$slug] : null;
    }
}

if (!function_exists('lireate_seo_apply_static_page_meta_to_cfg')) {
    /**
     * Вызывать из lireate-seo-pre-template.inc.php (после сборки $cfg из index.php).
     *
     * @param string $slug
     * @param array  $cfg       ссылка на $cfg
     * @param string $seo_title ссылка
     * @param string $seo_description ссылка
     */
    function lireate_seo_apply_static_page_meta_to_cfg($slug, &$cfg, &$seo_title, &$seo_description)
    {
        $meta = lireate_seo_static_page_meta($slug);
        if (!is_array($meta)) {
            return false;
        }
        if (!empty($meta['title'])) {
            $cfg['title'] = $meta['title'];
            $seo_title = $meta['title'];
        }
        if (!empty($meta['description'])) {
            $cfg['description'] = $meta['description'];
            $seo_description = $meta['description'];
        }
        return true;
    }
}
