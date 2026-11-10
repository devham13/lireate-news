<?php
/**
 * Страница автора: /avtor — Юрий Горбачев. Подключить из CMS-роута по seo_url avtor.
 */
if (!function_exists('lireate_avtor_jsonld')) {
    function lireate_avtor_jsonld($site)
    {
        $site = rtrim((string) $site, '/');
        return array(
            '@context' => 'https://schema.org',
            '@type' => 'Person',
            'name' => 'Юрий Горбачев',
            'jobTitle' => 'Генеральный директор',
            'worksFor' => array(
                '@type' => 'Organization',
                'name' => 'ООО «ЛИРЕЙТ»',
                'url' => $site . '/',
            ),
            'url' => $site . '/avtor/',
        );
    }
}
?>
<section class="lx-avtor-page">
  <h1>Юрий Горбачев</h1>
  <p>Генеральный директор ООО «ЛИРЕЙТ». Руководит патентным бюро по регистрации товарных знаков и защите интеллектуальной собственности для бизнеса.</p>
  <p><a href="/team/">Команда Лирейт</a> · <a href="/kontaktyi">Контакты</a></p>
</section>
