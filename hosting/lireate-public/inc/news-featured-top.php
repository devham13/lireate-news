<?php
/**
 * Блок для страницы /news на lireate.ru (вставить в шаблон ленты блога).
 *
 * Размещение на сервере: public_html/inc/news-featured-top.php
 * В шаблоне списка новостей (файл с подписью «Свежий материал») сразу после H1:
 *   <?php require_once __DIR__ . '/inc/news-featured-top.php'; ?>
 *
 * Не трогает data/db.php. Ссылки можно править здесь без правки БД.
 */
$lireate_featured = [
    [
        'title' => 'Всё, что нужно знать о договоре франчайзинга',
        'url' => '/vsyo_chto_nuzhno_znat_o_dogovore_franchayzinga_',
        'badge' => 'Читают чаще всего',
        'teaser' => 'Договор коммерческой концессии: что проверить до подписания и как не потерять права на бренд.',
    ],
    [
        'title' => 'Сроки действия авторских прав',
        'url' => '/sroki_deystviya_avtorskix_prav_na_kakoy_srok_predostavlyayutsya_avtorskie_prava_i_chto_proisxodit_posle_ix_istecheniya',
        'badge' => 'Популярный разбор',
        'teaser' => 'Когда произведение переходит в общественное достояние и что можно делать с текстом и изображениями после истечения срока.',
    ],
];
?>
<section class="lireate-news-hero" aria-label="Популярные материалы и связь с экспертами">
  <div class="lireate-news-cta">
    <h2 class="lireate-news-cta__title">Нужна помощь по товарному знаку, авторскому праву или бренду?</h2>
    <p class="lireate-news-cta__text">Задайте вопрос патентному бюро Лирейт - ответим по сути, без обещаний «гарантированной победы в суде».</p>
    <p class="lireate-news-cta__links">
      <a class="lireate-btn lireate-btn--tg" href="https://t.me/lireate_patent" rel="noopener noreferrer" target="_blank">Telegram</a>
      <a class="lireate-btn lireate-btn--wa" href="https://wa.me/79600484957" rel="noopener noreferrer" target="_blank">WhatsApp</a>
    </p>
  </div>
  <div class="lireate-news-featured">
    <h2 class="lireate-news-featured__title">Сначала полезное: что читают на сайте</h2>
    <ul class="lireate-news-featured__list">
      <?php foreach ($lireate_featured as $item): ?>
      <li class="lireate-news-featured__item">
        <span class="lireate-news-featured__badge"><?php echo htmlspecialchars($item['badge'], ENT_QUOTES, 'UTF-8'); ?></span>
        <a href="<?php echo htmlspecialchars($item['url'], ENT_QUOTES, 'UTF-8'); ?>"><?php echo htmlspecialchars($item['title'], ENT_QUOTES, 'UTF-8'); ?></a>
        <p><?php echo htmlspecialchars($item['teaser'], ENT_QUOTES, 'UTF-8'); ?></p>
      </li>
      <?php endforeach; ?>
    </ul>
  </div>
</section>
