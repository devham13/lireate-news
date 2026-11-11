<?php
/** Главная: тёмный hero v4 (без фонового фото). Подключается из template/main.php */
require_once __DIR__ . '/lireate-home-url.inc.php';
$_lx_tg = 'https://t.me/lireate_patent';
$_lx_mtitle = 'Оставьте заявку и мы свяжемся с вами в ближайшее время';
$_lx_success = 'Мы перезвоним Вам в ближайшее время.';
$_lx_btn = 'Отправить заявку';
?>
<div class="lireate-hero-v4__bg" aria-hidden="true">
  <span class="lireate-hero-v4__orb lireate-hero-v4__orb--a"></span>
  <span class="lireate-hero-v4__orb lireate-hero-v4__orb--b"></span>
  <span class="lireate-hero-v4__orb lireate-hero-v4__orb--c"></span>
  <span class="lireate-hero-v4__grid"></span>
</div>
<div class="lireate-hero-v4__inner">
  <header class="lireate-hero-v4__head">
    <h1>Патентное бюро «Лирейт»</h1>
    <h2 class="lireate-hero-v4__lead">Регистрация и защита интеллектуальной собственности</h2>
  </header>
  <nav class="lireate-hero-v4__services" aria-label="Основные услуги">
    <a class="lireate-hero-v4__service" href="<?php echo htmlspecialchars(lireate_home_abs_url('/reg-tz-main'), ENT_QUOTES, 'UTF-8'); ?>">
      <span class="lireate-hero-v4__service-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><text x="12" y="17" text-anchor="middle" font-size="16" font-weight="700" fill="currentColor">®</text></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Товарный знак</span>
    </a>
    <a class="lireate-hero-v4__service" href="<?php echo htmlspecialchars(lireate_home_abs_url('/patent_prom_obr'), ENT_QUOTES, 'UTF-8'); ?>">
      <span class="lireate-hero-v4__service-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><path fill="currentColor" d="M9 18h6v-7H9v7zm2-9h2V6h2l-5-4-5 4h2v3zm-1 11H8v2h8v-2h-2v-1h-4v1z"/></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Патенты</span>
    </a>
    <a class="lireate-hero-v4__service lireate-hero-v4__service--form js-modal-form" href="#"
      data-toggle="modal" data-frm="name,tel"
      data-mtitle="<?php echo htmlspecialchars($_lx_mtitle, ENT_QUOTES, 'UTF-8'); ?>"
      data-tomail="Программы ЭВМ"
      data-success="<?php echo htmlspecialchars($_lx_success, ENT_QUOTES, 'UTF-8'); ?>"
      data-btn="<?php echo htmlspecialchars($_lx_btn, ENT_QUOTES, 'UTF-8'); ?>"
      role="button">
      <span class="lireate-hero-v4__service-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><path fill="currentColor" d="M8 6l-4 4 4 4v-3h6V9H8V6zm8 12l4-4-4-4v3H10v2h6v3z"/></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Программы ЭВМ</span>
    </a>
    <a class="lireate-hero-v4__service lireate-hero-v4__service--form js-modal-form" href="#"
      data-toggle="modal"
      data-frm="name,tel"
      data-mtitle="<?php echo htmlspecialchars($_lx_mtitle, ENT_QUOTES, 'UTF-8'); ?>"
      data-tomail="Договоры"
      data-success="<?php echo htmlspecialchars($_lx_success, ENT_QUOTES, 'UTF-8'); ?>"
      data-btn="<?php echo htmlspecialchars($_lx_btn, ENT_QUOTES, 'UTF-8'); ?>"
      role="button">
      <span class="lireate-hero-v4__service-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><path fill="currentColor" d="M6 2h9l5 5v15H6V2zm8 1v5h5M8 12h8v2H8v-2zm0 4h6v2H8v-2zm10-9.5 3.5 3.5"/></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Договоры</span>
    </a>
  </nav>
  <ul class="lireate-hero-v4__facts">
    <li>
      <span class="lireate-hero-v4__fact-num">2015</span>
      <span class="lireate-hero-v4__fact-lbl">работаем с этого года</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num" data-lx-count-to="15">15</span>
      <span class="lireate-hero-v4__fact-lbl">специалистов</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num" data-lx-count-to="15">15</span>
      <span class="lireate-hero-v4__fact-lbl">минут до ответа</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num lireate-hero-v4__fact-num--text" aria-hidden="true">✓</span>
      <span class="lireate-hero-v4__fact-lbl">оплата за результат</span>
    </li>
  </ul>
  <div class="lireate-hero-v4__cta">
    <div class="lireate-hero-v4__cta-row">
      <div class="btn main-button js-modal-form lireate-hero-v4__btn lireate-hero-v4__btn--primary" data-toggle="modal" data-frm="name,tel" data-mtitle="Оставьте заявку и мы свяжемся с вами в ближайшее время" data-tomail="Заказать обратный звонок" data-success="Мы перезвоним Вам в ближайшее время." data-btn="Отправить заявку">Бесплатная консультация</div>
      <a class="lireate-hero-v4__btn lireate-hero-v4__btn--ghost" href="<?php echo htmlspecialchars($_lx_tg, ENT_QUOTES, 'UTF-8'); ?>" target="_blank" rel="noopener noreferrer" data-lx-ym-goal="perehod_v_telegramm">Написать в Telegram</a>
    </div>
    <p class="lireate-hero-v4__note">Через 15 минут вы получите ответ на свой вопрос</p>
  </div>
</div>
