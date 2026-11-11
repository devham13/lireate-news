<?php
/** Главная: тёмный hero v4 (без фонового фото). Подключается из template/main.php */
require_once __DIR__ . '/lireate-home-url.inc.php';
$_lx_tg = 'https://t.me/lireate_patent';
/* Те же пути, что в модалках «Подробнее» (lurl): reg-tz-main, patent_prom_obr; programs/dogovory — посадочные услуг */
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
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><path fill="currentColor" d="M4 4h16v4H4V4zm0 6h10v3H4v-3zm0 5h16v5H4v-5zm12-5h4v3h-4v-3z"/></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Товарный знак</span>
    </a>
    <a class="lireate-hero-v4__service" href="<?php echo htmlspecialchars(lireate_home_abs_url('/patent_prom_obr'), ENT_QUOTES, 'UTF-8'); ?>">
      <span class="lireate-hero-v4__service-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><path fill="currentColor" d="M12 2l2.2 6.8H21l-5.5 4 2.1 6.7L12 16.8 6.4 19.5l2.1-6.7L3 8.8h6.8L12 2z"/></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Патенты</span>
    </a>
    <a class="lireate-hero-v4__service" href="<?php echo htmlspecialchars(lireate_home_abs_url('/patent'), ENT_QUOTES, 'UTF-8'); ?>">
      <span class="lireate-hero-v4__service-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><path fill="currentColor" d="M6 3h12v2H6V3zm-1 4h14l-1 14H7L6 7zm4 3v9h2v-9h-2zm4 0v9h2v-9h-2z"/></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Программы ЭВМ</span>
    </a>
    <a class="lireate-hero-v4__service" href="<?php echo htmlspecialchars(lireate_home_abs_url('/docs'), ENT_QUOTES, 'UTF-8'); ?>">
      <span class="lireate-hero-v4__service-ico" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="28" height="28" focusable="false"><path fill="currentColor" d="M4 6h16v12H4V6zm2 2v8h12V8H6zm2 2h8v2H8v-2zm0 3h5v2H8v-2z"/></svg>
      </span>
      <span class="lireate-hero-v4__service-txt">Договоры</span>
    </a>
  </nav>
  <ul class="lireate-hero-v4__facts">
    <li>
      <span class="lireate-hero-v4__fact-num">2015</span>
      <span class="lireate-hero-v4__fact-lbl">с 2015 года</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num" data-lx-count-to="15">15</span>
      <span class="lireate-hero-v4__fact-lbl">специалистов</span>
    </li>
    <li>
      <span class="lireate-hero-v4__fact-num" data-lx-count-to="15">15</span>
      <span class="lireate-hero-v4__fact-lbl">ответ за 15 минут</span>
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
