<?php
/** Общие факт-плашки hero (patent / patent_prom_obr). PHP 7 */
?>
<div class="lireate-hero-v4__bg" aria-hidden="true">
  <span class="lireate-hero-v4__orb lireate-hero-v4__orb--a"></span>
  <span class="lireate-hero-v4__orb lireate-hero-v4__orb--b"></span>
  <span class="lireate-hero-v4__orb lireate-hero-v4__orb--c"></span>
  <span class="lireate-hero-v4__grid"></span>
</div>
<div class="lireate-hero-v4__inner lireate-cms-hero__inner">
  <header class="lireate-hero-v4__head">
    <h1><?php echo htmlspecialchars($lx_hero_h1, ENT_QUOTES, 'UTF-8'); ?></h1>
    <?php if (!empty($lx_hero_h2)) : ?>
    <h2 class="lireate-hero-v4__lead"><?php echo htmlspecialchars($lx_hero_h2, ENT_QUOTES, 'UTF-8'); ?></h2>
    <?php endif; ?>
    <?php if (!empty($lx_hero_h3)) : ?>
    <p class="lireate-cms-hero__note"><?php echo htmlspecialchars($lx_hero_h3, ENT_QUOTES, 'UTF-8'); ?></p>
    <?php endif; ?>
  </header>
  <ul class="lireate-hero-v4__facts">
    <li>
      <span class="lireate-hero-v4__fact-num">2015</span>
      <span class="lireate-hero-v4__fact-lbl">работаем с этого года</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num">15</span>
      <span class="lireate-hero-v4__fact-lbl">специалистов</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num">15</span>
      <span class="lireate-hero-v4__fact-lbl">минут до ответа</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num lireate-hero-v4__fact-num--text" aria-hidden="true">✓</span>
      <span class="lireate-hero-v4__fact-lbl">оплата за результат</span>
    </li>
  </ul>
  <div class="lireate-hero-v4__cta">
    <div class="lireate-hero-v4__cta-row">
      <div class="btn main-button js-modal-form lireate-hero-v4__btn lireate-hero-v4__btn--primary" data-toggle="modal" data-frm="name,tel" data-mtitle="Оставьте заявку и мы свяжемся с вами в ближайшее время" data-tomail="<?php echo htmlspecialchars($lx_hero_cta_mail, ENT_QUOTES, 'UTF-8'); ?>" data-success="Мы перезвоним Вам в ближайшее время." data-btn="Отправить заявку"><?php echo htmlspecialchars($lx_hero_cta_label, ENT_QUOTES, 'UTF-8'); ?></div>
      <a class="lireate-hero-v4__btn lireate-hero-v4__btn--ghost" href="https://t.me/lireate_patent" target="_blank" rel="noopener noreferrer" data-lx-ym-goal="perehod_v_telegramm">Написать в Telegram</a>
    </div>
  </div>
</div>
