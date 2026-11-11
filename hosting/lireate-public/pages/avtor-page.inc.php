<?php
/**
 * Страница автора: /avtor — Горбачев Юрий Александрович.
 */
if (!function_exists('lireate_avtor_h')) {
    function lireate_avtor_h($s)
    {
        return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
    }
}

if (!function_exists('lireate_avtor_jsonld')) {
    function lireate_avtor_jsonld($site)
    {
        $site = rtrim((string) $site, '/');
        return array(
            '@context' => 'https://schema.org',
            '@type' => 'Person',
            '@id' => $site . '/avtor/#person',
            'name' => 'Горбачев Юрий Александрович',
            'alternateName' => 'Юрий Горбачев',
            'jobTitle' => 'Директор, управляющий партнёр',
            'url' => $site . '/avtor/',
            'image' => $site . '/template/images/team/person/11.jpg',
            'worksFor' => array(
                '@type' => 'Organization',
                'name' => 'LIREATE',
                'legalName' => 'ООО «ЛИРЕЙТ»',
                'url' => $site . '/',
                'taxID' => '1648040894',
                'telephone' => '+7-960-048-49-57',
                'email' => 'info@' . 'lireate' . '.' . 'ru',
                'sameAs' => array('https://vk.com/lireate', 'https://t.me/lireate_patent'),
            ),
            'knowsAbout' => array(
                'Товарные знаки',
                'Патентное право',
                'Авторское право',
                'Программы для ЭВМ',
                'Споры об интеллектуальной собственности',
            ),
            'sameAs' => array(
                'https://vc.ru/id694569',
                'https://t-j.ru/user2640218/',
                'https://www.klerk.ru/author/6739/',
                'https://tenchat.ru/gorbachev_yuriy',
                'https://www.cossa.ru/profile/?ID=259138',
            ),
        );
    }
}

$lu_lib = $_SERVER['DOCUMENT_ROOT'] . '/template/page/uslugi/lireate-uslugi-lib.php';
if (is_file($lu_lib)) {
    require_once $lu_lib;
}
$lu_v = defined('LIREATE_USLUGI_VERSION') ? LIREATE_USLUGI_VERSION : '2026-11-11-avtor';
$lu_h = function_exists('lireate_uslugi_h') ? 'lireate_uslugi_h' : 'lireate_avtor_h';
?>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/template/page/uslugi/lireate-uslugi.css?v=<?php echo call_user_func($lu_h, $lu_v); ?>">
<link rel="stylesheet" href="/template/page/avtor/lireate-avtor.css?v=<?php echo call_user_func($lu_h, $lu_v); ?>">
<script>
(function () {
  function applyLireateAvtorBodyClass() {
    document.documentElement.classList.add('lireate-avtor-html');
    if (document.body) {
      document.body.classList.add('lireate-avtor-body');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyLireateAvtorBodyClass);
  } else {
    applyLireateAvtorBodyClass();
  }
})();
</script>
<div id="lireate-avtor" class="lu-page">
  <div class="lu-glow" aria-hidden="true"></div>
  <div class="lu-wrap">
    <nav class="lu-crumbs" aria-label="Хлебные крошки">
      <ol>
        <li><a href="/">Главная</a></li>
        <li><span aria-current="page">Автор</span></li>
      </ol>
    </nav>

    <header class="la-hero" aria-labelledby="la-h1">
      <div class="la-hero-text">
        <p class="lu-eyebrow">LIREATE · патентное бюро · автор статей</p>
        <h1 class="lu-h1" id="la-h1">Горбачев Юрий Александрович</h1>
        <p class="la-role"><strong>Директор и управляющий партнёр ООО «ЛИРЕЙТ», патентное бюро «Лирейт»</strong></p>
      </div>
      <figure class="la-photo">
        <picture>
          <source srcset="/template/images/team/person/11.webp" type="image/webp">
          <img src="/template/images/team/person/11.jpg" alt="Горбачев Юрий Александрович" width="350" height="525" loading="eager" decoding="async">
        </picture>
      </figure>
    </header>

    <section class="lu-section" aria-labelledby="la-about">
      <h2 class="lu-h2" id="la-about">Чем занимается</h2>
      <div class="la-prose">
        <p>Юрий Горбачев руководит патентным бюро «Лирейт» из Зеленодольска (Республика Татарстан). Бюро регистрирует и защищает товарные знаки, патенты и авторские права. Он директор ООО «ЛИРЕЙТ» с января 2021 года и один из двух совладельцев компании.</p>
        <p>Основные направления его работы:</p>
        <ul class="la-list">
          <li>товарные знаки: проверка обозначений, регистрация, споры;</li>
          <li>патентное право: изобретения, полезные модели, промышленные образцы;</li>
          <li>авторское право, смежные права и программы для ЭВМ;</li>
          <li>договоры отчуждения и лицензии на объекты интеллектуальной собственности;</li>
          <li>представительство в спорах, в том числе в суде;</li>
          <li>реклама и недобросовестная конкуренция.</li>
        </ul>
      </div>
    </section>

    <section class="lu-section" aria-labelledby="la-company">
      <h2 class="lu-h2" id="la-company">Компания и цифры</h2>
      <ul class="la-list">
        <li>ООО «ЛИРЕЙТ» зарегистрировано 6 июля 2015 года. Основной вид деятельности по ЕГРЮЛ — деятельность в области права.</li>
        <li>По данным компании, она работает в сфере охраны интеллектуальной собственности с 2005 года. Начинала в составе юридической компании «Энтер».</li>
        <li>В команде 15 специалистов: юристы по регистрации ИС и сотрудники патентного отдела.</li>
        <li>В группе ВКонтакте с ноября 2024 по ноябрь 2026 года опубликовано 133 разбора дел бюро: регистрация знаков, защита от претензий и исков, взыскание компенсаций, патенты.</li>
      </ul>
    </section>

    <section class="lu-section" aria-labelledby="la-pubs">
      <h2 class="lu-h2" id="la-pubs">Публикации</h2>
      <p class="lu-section-lead">Юрий Горбачев пишет для предпринимателей о товарных знаках, патентах и авторском праве. Его материалы выходят здесь:</p>
      <div class="la-pub-grid">
        <a class="la-pub-card lu-card" href="https://vc.ru/id694569" target="_blank" rel="noopener">
          <strong>vc.ru</strong>
          <span>Например обзор дела СИП-236/2026 о знаке «Капитал»</span>
        </a>
        <a class="la-pub-card lu-card" href="https://t-j.ru/user2640218/" target="_blank" rel="noopener">
          <strong>Т—Ж, «Сообщество Про»</strong>
          <span>В том числе статья «Регистрация ООО не защищает название бизнеса как бренд»</span>
        </a>
        <a class="la-pub-card lu-card" href="https://t-j.ru/law-practice-registratsiia-ooo-ne-zashchishchaet-nazvanie/" target="_blank" rel="noopener">
          <strong>Т—Ж — регистрация ООО и бренд</strong>
          <span>law-practice-registratsiia-ooo-ne-zashchishchaet-nazvanie</span>
        </a>
        <a class="la-pub-card lu-card" href="https://www.klerk.ru/author/6739/" target="_blank" rel="noopener">
          <strong>Клерк.ру</strong>
          <span>Страница автора</span>
        </a>
        <a class="la-pub-card lu-card" href="https://habr.com/ru/articles/813959/" target="_blank" rel="noopener">
          <strong>Хабр</strong>
          <span>Разработка и регистрация товарных знаков</span>
        </a>
        <a class="la-pub-card lu-card" href="https://habr.com/ru/articles/894612/" target="_blank" rel="noopener">
          <strong>Хабр — сторонние компоненты в ПО</strong>
          <span>Статья на Habr</span>
        </a>
        <a class="la-pub-card lu-card" href="https://tenchat.ru/gorbachev_yuriy" target="_blank" rel="noopener">
          <strong>TenChat</strong>
          <span>Профиль Юрия Горбачева</span>
        </a>
        <a class="la-pub-card lu-card" href="https://vk.com/lireate" target="_blank" rel="noopener">
          <strong>ВКонтакте — «Лирейт — патентное бюро»</strong>
          <span>Кейсы бюро</span>
        </a>
      </div>
    </section>

    <section class="lu-section" aria-labelledby="la-contacts">
      <h2 class="lu-h2" id="la-contacts">Контакты компании</h2>
      <div class="la-contacts la-prose">
        <p>ООО «ЛИРЕЙТ», ИНН 1648040894, ОГРН 1151673001578</p>
        <p>Телефон: <a href="tel:+79600484957">+7 (960) 048-49-57</a><br>
        E-mail: <?php $la_mail = 'info@' . 'lireate' . '.' . 'ru'; ?>
        <a href="mailto:<?php echo lireate_avtor_h($la_mail); ?>"><?php echo lireate_avtor_h($la_mail); ?></a></p>
        <p class="la-nav-links">
          <a href="/team/">Команда</a><span aria-hidden="true">·</span>
          <a href="/docs">Документы и реквизиты</a><span aria-hidden="true">·</span>
          <a href="/kontaktyi">Контакты</a>
        </p>
      </div>
    </section>
  </div>
<?php
if (function_exists('lireate_uslugi_render_footer')) {
    lireate_uslugi_render_footer();
}
?>
</div>
