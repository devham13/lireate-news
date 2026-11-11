#!/usr/bin/env python3
"""Render standalone LU service landing HTML (index.php) from page config."""
from __future__ import annotations

import html
import json
import os
import sys
from pathlib import Path
from typing import Any

SITE = os.environ.get("LIREATE_PUBLIC_SITE_URL", "https://lireate.invalid").rstrip("/")
DUES_TABLE = "https://rospatent.gov.ru/ru/activities/dues/table"
CSS_SHARED = "assets/lireate-shared/lireate-service-dark.css?v=20261111svc"
BAR_CSS = "/template/css/lireate-service-mobile-bar.css?v=20261111svc3"
BAR_JS = "/template/js/lireate-service-mobile-bar.js?v=20261111svc3"
METRIKA_JS = "/template/js/lireate-service-metrika-goals.js?v=20261111svc3"

BREADCRUMB_SERVICES = [
    ("/findtz/", "Проверка товарного знака"),
    ("/registraciya_tovarnogo_znaka/", "Регистрация товарного знака"),
    ("/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/", "Регистрация с оплатой за результат"),
    ("/prodlenie_tovarnogo_znaka/", "Продление товарного знака"),
    ("/registraciya_tovarnogo_znaka_v_kitae/", "Регистрация товарного знака в Китае"),
    ("/vozrazhenie_protiv_registracii_tovarnogo_znaka/", "Возражение против регистрации ТЗ"),
    ("/zashchita_avtorskih_prav/", "Защита авторских прав"),
    ("/dogovory/", "Договоры в сфере ИС"),
    ("/registraciya_programm_evm/", "Регистрация программ для ЭВМ"),
]

SHARED_SCRIPTS = [
    "assets/lireate-shared/lireate-motion-init.js?v=1792348203",
    "assets/lireate-shared/lireate-reveal.js?v=1792337403",
    "assets/lireate-shared/lireate-hero-panel.js?v=1792348203",
    "assets/lireate-shared/lireate-carousel.js?v=1792348203",
    "assets/lireate-shared/lireate-steps-walk.js?v=1792348203",
    "assets/lireate-shared/lireate-mascot.js?v=1792348203",
    "assets/lireate-shared/lireate-service-extras.js?v=1792348203",
    "assets/lireate-shared/lireate-breadcrumbs.js?v=1794297797",
]


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _breadcrumb_items(current_label: str) -> str:
    items = []
    for href, label in BREADCRUMB_SERVICES:
        items.append(
            f'                <li role="none">\n'
            f'          <a role="menuitem" href="{_esc(href)}">\n'
            f"            {html.escape(label)}          </a>\n"
            f"        </li>\n"
        )
    menu = "".join(items)
    return f"""<nav class="lx-breadcrumbs lx-breadcrumbs--in-page" aria-label="Хлебные крошки">
  <ol>
    <li><a href="/">Главная</a></li>
    <li class="lx-breadcrumb-services">
      <button
        type="button"
        class="lx-breadcrumb-services-trigger"
        id="lx-breadcrumb-services-trigger"
        aria-expanded="false"
        aria-haspopup="true"
        aria-controls="lx-breadcrumb-services-menu"
      >Услуги</button>
      <ul
        class="lx-breadcrumb-services-menu"
        id="lx-breadcrumb-services-menu"
        role="menu"
        aria-labelledby="lx-breadcrumb-services-trigger"
        hidden
      >
{menu}      </ul>
    </li>
    <li aria-current="page">{html.escape(current_label)}</li>
  </ol>
</nav>"""


def _schema_graph(cfg: dict[str, Any]) -> str:
    path = cfg["path"]
    url = f"{SITE}{path}"
    faq_entities = [
        {
            "@type": "Question",
            "name": q["q"],
            "acceptedAnswer": {"@type": "Answer", "text": q["a"]},
        }
        for q in cfg["faq"]
    ]
    graph = [
        {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": cfg["h1"],
            "url": url,
            "description": cfg["description"],
            "areaServed": "RU",
            "provider": {"@id": f"{url}#organization"},
        },
        {
            "@type": ["LegalService", "Organization"],
            "@id": f"{url}#organization",
            "name": "LIREATE",
            "url": f"{SITE}/",
            "telephone": "+7-960-048-49-57",
            "sameAs": [
                "https://t.me/lireate_patent",
                "https://wa.me/79600484957",
                "https://max.ru/u/f9LHodD0cOI8jsPagjibEve2cn5_xPW0X1sf3PhbS5TMijA78DnUeDEpUAI",
            ],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Услуги"},
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": cfg["h1"],
                    "item": url,
                },
            ],
        },
        {"@type": "FAQPage", "mainEntity": faq_entities},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def _faq_block(faq: list[dict[str, str]]) -> str:
    parts = []
    for item in faq:
        parts.append(
            f'  <details class="lx-faq"><summary>{html.escape(item["q"])}</summary>'
            f"<p>{item['a']}</p></details>"
        )
    return "\n".join(parts)


def _contact_form(cfg: dict[str, Any]) -> str:
    return f"""<section class="lx-section lx-reveal" id="contact">
  <div class="lx-contact">
    <div>
      <span class="lx-section-label">Контакт</span>
      <h2>Заявка и мессенджеры</h2>
      <p>Телефон: <a href="tel:+79600484957">+7 (960) 048-49-57</a></p>
      <p class="lx-contact-facts">Работаем с 2015 года · 15 патентных поверенных · ответим за 15 минут</p>
      <div class="lx-msg-grid">
        <a class="lx-msg-btn" id="link-telegram" href="https://t.me/lireate_patent" target="_blank" rel="noopener noreferrer" data-lx-icon="telegram" data-lx-ym-goal="perehod_v_telegramm"><span>Telegram</span></a>
        <a class="lx-msg-btn" id="link-whatsapp" href="https://wa.me/79600484957" target="_blank" rel="noopener noreferrer" data-lx-icon="whatsapp" data-lx-ym-goal="perehod_v_messendzher"><span>WhatsApp</span></a>
        <a class="lx-msg-btn lx-msg-btn--max" id="link-max" href="https://max.ru/u/f9LHodD0cOI8jsPagjibEve2cn5_xPW0X1sf3PhbS5TMijA78DnUeDEpUAI" target="_blank" rel="noopener noreferrer" data-lx-icon="max" data-lx-ym-goal="perehod_v_messendzher"><span>MAX</span></a>
      </div>
    </div>
    <div class="lx-form-panel">
      <form
        id="lireate-lead-form"
        class="lx-mail-lead-form"
        method="POST"
        action="/mail.php"
        data-lx-mail-action="/mail.php"
        data-lead-topic="{_esc(cfg['lead_topic'])}"
        data-lx-success-text="Спасибо, заявка принята."
        novalidate
      >
        <input type="hidden" name="mail_token" value="503066424d5f7b5ad2097703ef3404d2">
        <input type="hidden" name="fuck_spamers" value="a1d379da8c7d147abd42f3bda4028bce">
        <input type="hidden" name="mail" value="mailorder">
        <input type="hidden" name="form-type" value="order">
        <input type="hidden" name="tomail" value="{_esc(cfg['tomail'])}">
        <input type="hidden" name="consent_form" value="{_esc(cfg['consent_form'])}">
        <label for="lf-name">Имя</label>
        <input id="lf-name" name="name" type="text" required autocomplete="name" placeholder="Как к вам обращаться">
        <label for="lf-phone">Телефон</label>
        <input id="lf-phone" name="tel" type="tel" required autocomplete="tel" placeholder="+7 …" inputmode="tel">
        <label class="lx-consent"><input type="checkbox" id="lf-consent" required> Согласен на <a href="/private_data" target="_blank" rel="noopener noreferrer">обработку персональных данных</a> и с <a href="/politika_konfidencialnosti" target="_blank" rel="noopener noreferrer">политикой конфиденциальности</a>.</label>
        <button type="submit" class="lx-btn lx-btn-primary lx-form-submit" style="width:100%;margin-top:12px;">Рассчитать стоимость за 15 минут</button>
        <div class="lx-form-alt">
          <span class="lx-form-alt-label">или напишите нам</span>
          <div class="lx-form-alt-icons">
            <a id="form-alt-telegram" class="lx-form-alt-link" href="https://t.me/lireate_patent" target="_blank" rel="noopener noreferrer" data-lx-icon="telegram" data-lx-ym-goal="perehod_v_telegramm" aria-label="Telegram"></a>
            <a id="form-alt-whatsapp" class="lx-form-alt-link" href="https://wa.me/79600484957" target="_blank" rel="noopener noreferrer" data-lx-icon="whatsapp" data-lx-ym-goal="perehod_v_messendzher" aria-label="WhatsApp"></a>
            <a id="form-alt-max" class="lx-form-alt-link lx-form-alt-link--max" href="https://max.ru/u/f9LHodD0cOI8jsPagjibEve2cn5_xPW0X1sf3PhbS5TMijA78DnUeDEpUAI" target="_blank" rel="noopener noreferrer" data-lx-icon="max-white" data-lx-ym-goal="perehod_v_messendzher" aria-label="MAX"></a>
          </div>
        </div>
        <p class="lx-form-success" id="lf-success" role="status" aria-live="polite"></p>
        <p class="lx-form-error" id="lf-error" role="alert" hidden></p>
      </form>
    </div>
  </div>
</section>"""


def render(cfg: dict[str, Any]) -> str:
    url = f"{SITE}{cfg['path']}"
    nav_links = "".join(
        f'      <a href="{_esc(a["href"])}">{html.escape(a["label"])}</a>\n' for a in cfg["nav"]
    )
    tags = "".join(f"<span>{html.escape(t)}</span>" for t in cfg["tags"])
    mini_stats = "".join(
        f'      <div class="lx-mini-stat"><strong class="lx-stat-value">{html.escape(m["v"])}</strong>'
        f"<span>{html.escape(m['l'])}</span></div>\n"
        for m in cfg["mini_stats"]
    )
    kpi = "".join(
        f'      <div class="lx-kpi"><b class="lx-stat-value">{html.escape(k["b"])}</b>'
        f"<small>{html.escape(k['s'])}</small></div>\n"
        for k in cfg["kpi"]
    )
    feed = "".join(f"      <li>{html.escape(li)}</li>\n" for li in cfg["feed"])
    script_tags = "\n".join(f'<script src="{s}"></script>' for s in SHARED_SCRIPTS)
    script_tags += """
<script>window.lireateMailSpamGuard="a1d379da8c7d147abd42f3bda4028bce";</script>
<script src="/template/js/lireate-utm.js?v=20261031"></script>
<script src="assets/lireate-shared/lireate-lead-mail.js?v=1794303344"></script>
<script src="assets/lireate-shared/lireate-contact.js?v=1794338289"></script>"""

    return f"""<!DOCTYPE html>
<html lang="ru" data-lireate-telegram="https://t.me/lireate_patent" data-lireate-whatsapp="https://wa.me/79600484957" data-lireate-max="https://max.ru/u/f9LHodD0cOI8jsPagjibEve2cn5_xPW0X1sf3PhbS5TMijA78DnUeDEpUAI">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(cfg["title"])}</title>
  <meta name="description" content="{_esc(cfg["description"])}">
  <link rel="canonical" href="{_esc(url)}">
  <meta property="og:title" content="{_esc(cfg["title"])}">
  <meta property="og:description" content="{_esc(cfg["description"])}">
  <meta property="og:url" content="{_esc(url)}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}/local/templates/lireate/images/og-default.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="robots" content="index,follow">
  <link rel="stylesheet" href="{CSS_SHARED}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <script type="application/ld+json">{_schema_graph(cfg)}</script>
</head>
<body class="lireate-svc-body lireate-service-mobile-dock">
<div class="lx-bg-glow" aria-hidden="true"></div>
<div class="lx-nav-shell">
  <header class="lx-nav-pill" role="banner">
    <a class="lx-logo" href="/">LIREATE</a>
    <nav class="lx-nav-links" aria-label="Разделы страницы">
{nav_links}    </nav>
    <a class="lx-btn lx-btn-primary" href="#contact">Консультация</a>
  </header>
</div>

<main id="primary" class="lireate-svc-page {html.escape(cfg['page_class'])}" role="main" tabindex="-1">

<style id="lx-breadcrumb-critical">
.lireate-svc-page .lx-breadcrumb-services-menu[hidden],
.lireate-svc-page .lx-breadcrumb-services:not(.is-open) .lx-breadcrumb-services-menu{{display:none!important}}
.lireate-svc-page .lx-breadcrumb-services-menu,
.lireate-svc-page .lx-breadcrumb-services-menu li{{list-style:none!important;margin:0;padding-left:0!important}}
.lireate-svc-page .lx-breadcrumb-services-menu li::after{{content:none!important}}
.lireate-svc-page button.lx-breadcrumb-services-trigger{{-webkit-appearance:none;appearance:none;border:1px solid rgba(125,211,252,.45);border-radius:8px;background:rgba(15,23,42,.35)}}
</style>
{_breadcrumb_items(cfg["h1"])}

<section class="lx-hero" id="top">
  <div class="lx-hero-mascot-slot" data-lx-mascot="{html.escape(cfg.get("mascot", "default"))}"></div>
  <div>
    <p class="lx-eyebrow">{html.escape(cfg["eyebrow"])}</p>
    <h1>{html.escape(cfg["h1"])}</h1>
    <p class="lx-hero-lead">{cfg["lead"]}</p>
    <div class="lx-tags" aria-label="Темы услуги">{tags}</div>
    <div class="lx-hero-cta">
      <a class="lx-btn lx-btn-primary" href="#contact">Оставить заявку</a>
      <a class="lx-btn lx-btn-ghost lx-btn--with-icon" id="hero-telegram" href="https://t.me/lireate_patent" target="_blank" rel="noopener noreferrer" data-lx-icon="telegram"><span>Написать в Telegram</span></a>
      <a class="lx-btn lx-btn-ghost lx-btn--with-icon" id="hero-max" href="https://max.ru/u/f9LHodD0cOI8jsPagjibEve2cn5_xPW0X1sf3PhbS5TMijA78DnUeDEpUAI" target="_blank" rel="noopener noreferrer" data-lx-icon="max"><span>Написать в Max</span></a>
    </div>
    <div class="lx-hero-mini">
{mini_stats}    </div>
  </div>
  <div class="lx-glass lx-glass-anim" aria-label="Краткий маршрут">
    <div class="lx-panel-head"><span>{html.escape(cfg["panel_title"])}</span><span class="lx-live">LIREATE</span></div>
    <div class="lx-kpi-row">
{kpi}    </div>
    <ul class="lx-feed">
{feed}    </ul>
  </div>
</section>

{cfg["body_sections"]}

{_contact_form(cfg)}

{cfg.get("related_section", "")}

</main>

<footer class="lx-site-footer" role="contentinfo">
  <div class="lx-site-footer-inner">
    <p class="lx-site-footer-title">LIREATE • Товарные знаки • Интеллектуальная собственность</p>
    <p class="lx-site-footer-lead">Регистрация и защита товарных знаков, патентов и авторских прав.</p>
    <p class="lx-site-footer-meta">ООО «ЛИРЕЙТ»</p>
    <p class="lx-site-footer-meta">ИНН 1648040894 • КПП 164801001 • ОГРН 1151673001578</p>
    <p class="lx-site-footer-contact">
      <a href="mailto:info@lireate.invalid">info@lireate.invalid</a>
      <span class="lx-site-footer-dot" aria-hidden="true">•</span>
      <a href="tel:+79600484957">+7 (960) 048-49-57</a>
      <span class="lx-site-footer-dot" aria-hidden="true">•</span>
      <a href="https://t.me/lireate_patent" target="_blank" rel="noopener noreferrer">Telegram</a>
    </p>
    <div class="lx-site-footer-nav">
      <a href="/politika_konfidencialnosti">Политика конфиденциальности</a>
      <a href="/private_data">Согласие на обработку персональных данных</a>
      <a href="/news/">Блог</a>
    </div>
    <p class="lx-site-footer-copy">© 2026 LIREATE</p>
  </div>
</footer>

{script_tags}
<aside class="lx-mobile-bar" data-lx-svc-mobile-bar="canonical" aria-label="Быстрый звонок и мессенджеры">
  <a class="lx-mobile-bar-btn lx-mobile-bar-btn--call" href="tel:+79600484957">Позвонить</a>
  <a class="lx-mobile-bar-btn" href="https://t.me/lireate_patent" target="_blank" rel="noopener noreferrer" data-lx-icon="telegram" aria-label="Telegram"></a>
  <a class="lx-mobile-bar-btn lx-mobile-bar-btn--max" href="https://max.ru/u/f9LHodD0cOI8jsPagjibEve2cn5_xPW0X1sf3PhbS5TMijA78DnUeDEpUAI" target="_blank" rel="noopener noreferrer" data-lx-icon="max-white" aria-label="MAX"></a>
  <a class="lx-mobile-bar-btn lx-mobile-bar-btn--primary" href="#contact" data-lx-svc-lead="1">Заявка</a>
</aside>
  <link rel="stylesheet" href="{BAR_CSS}" />
  <script defer src="{METRIKA_JS}"></script>
  <script defer src="{BAR_JS}"></script>
</body>
</html>
"""


DOGOVORY_BODY = f"""
<section class="lx-section lx-reveal" id="included">
  <span class="lx-section-label">Состав услуги</span>
  <h2>Что входит в сопровождение договоров</h2>
  <div class="lx-card-grid">
    <article class="lx-card" id="licenziya"><h3>Лицензионный договор</h3><p>Разовая или исключительная лицензия, территория, срок, вознаграждение, отчётность.</p></article>
    <article class="lx-card" id="franchise"><h3>Договор коммерческой концессии</h3><p>Франчайзинг: пакет прав, обучение, контроль качества, регистрация в Роспатенте при необходимости.</p></article>
    <article class="lx-card" id="otchuzhdenie"><h3>Договор отчуждения</h3><p>Передача исключительного права на программу, произведение, знак — с учётом требований ГК РФ.</p></article>
    <article class="lx-card" id="avtorskij-zakaz"><h3>Договор авторского заказа</h3><p>Права на код, дизайн, текст: сроки, результат, переход прав заказчику (ст. 1288 ГК РФ).</p></article>
    <article class="lx-card" id="registraciya-dogovora"><h3>Регистрация договора в Роспатенте</h3><p>Госрегистрация распоряжения исключительным правом, когда она обязательна по закону.</p></article>
  </div>
</section>

<section class="lx-section lx-reveal" id="when">
  <span class="lx-section-label">Для кого</span>
  <h2>Когда нужны договоры в сфере ИС</h2>
  <ul class="lx-checklist">
    <li>Передаёте права на софт, дизайн или контент подрядчику или партнёру</li>
    <li>Открываете франшизу или даёте лицензию на бренд</li>
    <li>Покупаете или продаёте исключительные права</li>
    <li>Заказываете разработку сайта, приложения, логотипа у фрилансера</li>
    <li>Нужна запись договора в Роспатенте для сделки с третьими лицами</li>
  </ul>
</section>

<section class="lx-section lx-reveal" id="program">
  <span class="lx-section-label">Этапы</span>
  <h2>Как проходит работа</h2>
  <ol class="lx-steps-walk-list">
    <li class="lx-steps-walk-step"><span class="lx-card-num">01</span><h3>Бриф</h3><p><strong>1 день.</strong> Объект ИС, стороны, цель сделки.</p></li>
    <li class="lx-steps-walk-step"><span class="lx-card-num">02</span><h3>Проект договора</h3><p><strong>2–5 дней.</strong> Условия по ГК РФ, риски, приложения.</p></li>
    <li class="lx-steps-walk-step"><span class="lx-card-num">03</span><h3>Согласование</h3><p><strong>по сторонам.</strong> Правки и финальная редакция.</p></li>
    <li class="lx-steps-walk-step"><span class="lx-card-num">04</span><h3>Регистрация в Роспатенте</h3><p><strong>если нужна.</strong> Подача, пошлины, сопровождение.</p></li>
  </ol>
</section>

<section class="lx-section lx-reveal" id="terms">
  <span class="lx-section-label">Сроки</span>
  <h2>Ориентиры по срокам</h2>
  <p>Подготовка договора — обычно <strong>3–7 рабочих дней</strong> после брифа. Госрегистрация распоряжения — по регламенту Роспатента (ориентир <strong>до 68 рабочих дней</strong> на услугу регистрации распоряжения; сверяйте на <a href="{DUES_TABLE}" target="_blank" rel="noopener noreferrer">rospatent.gov.ru</a>).</p>
</section>

<section class="lx-section lx-reveal" id="pricing">
  <span class="lx-section-label">Стоимость</span>
  <h2>Пошлины Роспатента и услуги LIREATE</h2>
  <div class="lx-price-grid">
    <div class="lx-price-card"><strong>за 15 минут</strong><span>Рассчитаем стоимость сопровождения после брифа — без фиктивных цен на сайте</span></div>
    <div class="lx-price-card"><strong>п. 3.10</strong><span>Регистрация лицензионного договора (в т.ч. коммерческая концессия): <strong>15&nbsp;000&nbsp;₽</strong> + <strong>13&nbsp;000&nbsp;₽</strong> за каждый дополнительный объект в заявлении — <a href="{DUES_TABLE}" target="_blank" rel="noopener noreferrer">таблица пошлин</a></span></div>
    <div class="lx-price-card"><strong>п. 3.11</strong><span>Регистрация договора об отчуждении: <strong>15&nbsp;000&nbsp;₽</strong> + <strong>13&nbsp;000&nbsp;₽</strong> за каждый дополнительный объект — <a href="{DUES_TABLE}" target="_blank" rel="noopener noreferrer">таблица пошлин</a></span></div>
  </div>
  <p class="lx-calc-note">Указаны только официальные госпошлины из приложения к ПП РФ № 941. Суммы сверяйте на момент оплаты. Услуги LIREATE оплачиваются отдельно.</p>
  <a class="lx-btn lx-btn-primary" href="#contact">Рассчитать стоимость за 15 минут</a>
</section>

<section class="lx-section lx-reveal" id="blog">
  <span class="lx-section-label">Блог</span>
  <h2>Материалы по договорам</h2>
  <div class="lx-related-grid">
    <a class="lx-related-card" href="/dogovor_avtorskogo_zakaza_chto_nuzhno_znat__/"><span class="lx-related-card-type">Статья</span><strong>Договор авторского заказа: что учесть</strong></a>
    <a class="lx-related-card" href="/vsyo_chto_nuzhno_znat_o_dogovore_franchayzinga_/"><span class="lx-related-card-type">Статья</span><strong>Договор франчайзинга</strong></a>
    <a class="lx-related-card" href="/avtorskiy_dogovor_na_sozdanie_logotipa/"><span class="lx-related-card-type">Статья</span><strong>Авторский договор на логотип</strong></a>
    <a class="lx-related-card" href="/zashchita_avtorskih_prav/"><span class="lx-related-card-type">Услуга</span><strong>Защита авторских прав</strong></a>
  </div>
</section>

<section class="lx-section lx-reveal" id="faq">
  <span class="lx-section-label">FAQ</span>
  <h2>Вопросы о договорах в сфере ИС</h2>
"""

EVM_BODY = f"""
<section class="lx-section lx-reveal" id="included">
  <span class="lx-section-label">Состав услуги</span>
  <h2>Что входит</h2>
  <div class="lx-card-grid">
    <article class="lx-card" id="registraciya-po"><h3>Регистрация программы для ЭВМ</h3><p>Заявление, реферат, депонируемые материалы, сопровождение в Роспатенте.</p></article>
    <article class="lx-card" id="registraciya-bd"><h3>Регистрация базы данных</h3><p>Описание структуры, объём, СУБД — отдельная заявка на каждую БД.</p></article>
    <article class="lx-card" id="zaschita-sajta"><h3>Защита сайта и приложений</h3><p>Договоры с разработчиками, регистрация кода, комплекс с товарным знаком при необходимости.</p></article>
  </div>
</section>

<section class="lx-section lx-reveal" id="when">
  <span class="lx-section-label">Для кого</span>
  <h2>Когда нужна регистрация программ и защита сайта</h2>
  <ul class="lx-checklist">
    <li>Выпускаете SaaS, мобильное приложение или внутренний софт</li>
    <li>Нужно зафиксировать права на код перед инвестициями или сделкой</li>
    <li>Собираете коммерческую базу данных клиентов или каталог</li>
    <li>Конкурент копирует функционал сайта или интерфейс</li>
    <li>Разработчик на аутсорсе — нужен договор с переходом прав</li>
  </ul>
</section>

<section class="lx-section lx-reveal" id="program">
  <span class="lx-section-label">Этапы</span>
  <h2>Этапы регистрации и защиты</h2>
  <ol class="lx-steps-walk-list">
    <li class="lx-steps-walk-step"><span class="lx-card-num">01</span><h3>Аудит</h3><p><strong>1–3 дня.</strong> Объект, авторы, договоры, риски.</p></li>
    <li class="lx-steps-walk-step"><span class="lx-card-num">02</span><h3>Пакет документов</h3><p><strong>3–7 дней.</strong> Реферат, фрагменты кода, заявление.</p></li>
    <li class="lx-steps-walk-step"><span class="lx-card-num">03</span><h3>Пошлины и подача</h3><p><strong>1–2 дня.</strong> Оплата, подача через портал Роспатента.</p></li>
    <li class="lx-steps-walk-step"><span class="lx-card-num">04</span><h3>Свидетельство</h3><p><strong>до 62 раб. дн.</strong> По регламенту госуслуги регистрации ПО/БД.</p></li>
  </ol>
</section>

<section class="lx-section lx-reveal" id="terms">
  <span class="lx-section-label">Сроки</span>
  <h2>Сроки Роспатента</h2>
  <p>Предельный срок госуслуги по регистрации программы или базы данных — <strong>62 рабочих дня</strong> с даты приёма заявки (страница услуги на <a href="https://rospatent.gov.ru/ru/stateservices/gosudarstvennaya-registraciya-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-i-vydacha-svidetelstv-o-gosudarstvennoy-registracii-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-ih-dublikatov" target="_blank" rel="noopener noreferrer">rospatent.gov.ru</a>).</p>
</section>

<section class="lx-section lx-reveal" id="pricing">
  <span class="lx-section-label">Стоимость</span>
  <h2>Пошлины и сопровождение LIREATE</h2>
  <div class="lx-price-grid">
    <div class="lx-price-card"><strong>за 15 минут</strong><span>Рассчитаем стоимость сопровождения — без выдуманных прайсов на сайте</span></div>
    <div class="lx-price-card"><strong>5&nbsp;000&nbsp;₽</strong><span>Госпошлина за регистрацию программы для ЭВМ или базы данных (сверьте пункт в <a href="{DUES_TABLE}" target="_blank" rel="noopener noreferrer">таблице пошлин</a> Роспатента на дату оплаты)</span></div>
    <div class="lx-price-card"><strong>1&nbsp;300&nbsp;₽</strong><span>Дубликат свидетельства — по сведениям на странице госуслуги Роспатента; точную сумму сверьте в <a href="{DUES_TABLE}" target="_blank" rel="noopener noreferrer">таблице</a></span></div>
  </div>
  <p class="lx-calc-note">Цифры пошлин — только с официальной таблицы. Услуги LIREATE не являются офертой.</p>
  <a class="lx-btn lx-btn-primary" href="#contact">Рассчитать стоимость за 15 минут</a>
</section>

<section class="lx-section lx-reveal" id="blog">
  <span class="lx-section-label">Блог</span>
  <h2>Материалы по программам и БД</h2>
  <div class="lx-related-grid">
    <a class="lx-related-card" href="/sposobyi_zaschityi_kompyuternoy_programmyi_ot_nezakonnogo_ispolzovaniya/"><span class="lx-related-card-type">Статья</span><strong>Защита программы от незаконного использования</strong></a>
    <a class="lx-related-card" href="/registraciya_programmnogo_koda_dlya_zaschityi_prilozheniya_ot_kopirovaniya/"><span class="lx-related-card-type">Статья</span><strong>Регистрация кода приложения</strong></a>
    <a class="lx-related-card" href="/zaschita_kompyuternoy_programmyi_i_bazyi_dannyix_pravovyie_metodyi/"><span class="lx-related-card-type">Статья</span><strong>Защита программы и БД</strong></a>
    <a class="lx-related-card" href="/zashchita_avtorskih_prav/"><span class="lx-related-card-type">Услуга</span><strong>Защита авторских прав</strong></a>
  </div>
</section>

<section class="lx-section lx-reveal" id="faq">
  <span class="lx-section-label">FAQ</span>
  <h2>Вопросы о программах для ЭВМ и базах данных</h2>
"""

PAGES: dict[str, dict[str, Any]] = {
    "dogovory": {
        "path": "/dogovory/",
        "page_class": "dogovory-page",
        "mascot": "contracts",
        "title": "Договоры в сфере интеллектуальной собственности — LIREATE",
        "description": "Лицензии, франчайзинг, отчуждение и авторский заказ: подготовка договоров и регистрация распоряжений в Роспатенте. Консультация LIREATE.",
        "h1": "Договоры в сфере интеллектуальной собственности",
        "lead": "Готовим договоры и сопровождаем регистрацию распоряжений — без обещаний исхода ведомства.",
        "eyebrow": "LIREATE · договоры · ГК РФ ч. 4",
        "tags": ["ст. 1234 ГК", "ст. 1488", "Роспатент"],
        "panel_title": "Договоры · маршрут",
        "kpi": [
            {"b": "лицензия", "s": "исключительная или обычная"},
            {"b": "п. 3.10", "s": "госрегистрация лицензии"},
            {"b": "п. 3.11", "s": "отчуждение права"},
        ],
        "feed": [
            "Анализ объекта и сторон",
            "Проект договора под вашу сделку",
            "Согласование условий",
            "Подача на регистрацию в Роспатент при необходимости",
        ],
        "mini_stats": [
            {"v": "2015", "l": "работаем с этого года"},
            {"v": "15", "l": "специалистов в команде"},
            {"v": "15 мин", "l": "ориентир на ответ"},
        ],
        "nav": [
            {"href": "#included", "label": "Состав"},
            {"href": "#when", "label": "Для кого"},
            {"href": "#program", "label": "Этапы"},
            {"href": "#pricing", "label": "Пошлины"},
            {"href": "#blog", "label": "Блог"},
            {"href": "#faq", "label": "FAQ"},
            {"href": "#contact", "label": "Заявка"},
        ],
        "lead_topic": "Заявка: договоры ИС",
        "tomail": "Договоры в сфере ИС — заявка с сайта",
        "consent_form": "lx-dogovory-is",
        "faq": [
            {
                "q": "Нужно ли регистрировать лицензию в Роспатенте?",
                "a": "Для ряда объектов (например, товарный знак) договор о распоряжении исключительным правом подлежит госрегистрации (ст. 1490, 1232 ГК РФ). Пошлина — п. 3.10 таблицы на rospatent.gov.ru.",
            },
            {
                "q": "Чем отличается лицензия от отчуждения?",
                "a": "Лицензия сохраняет правообладателя и даёт право использования. Отчуждение переводит исключительное право другой стороне; регистрация — по п. 3.11.",
            },
            {
                "q": "Сколько стоит подготовка договора в LIREATE?",
                "a": "Зависит от объекта и объёма. Рассчитаем за 15 минут после брифа — на сайте фиксированных цен нет.",
            },
            {
                "q": "Можно ли зарегистрировать договор авторского заказа?",
                "a": "Авторское право возникает с создания произведения; отдельная регистрация договора в Роспатенте для текста или дизайна обычно не требуется. Регистрация нужна, если распоряжаетесь зарегистрированным объектом (ПО, знак).",
            },
            {
                "q": "Какие пошлины за регистрацию распоряжения?",
                "a": "П. 3.10 и 3.11 приложения к ПП РФ № 941: 15 000 ₽ за первый объект и 13 000 ₽ за каждый дополнительный в одной заявлении. Сверяйте на https://rospatent.gov.ru/ru/activities/dues/table",
            },
        ],
        "body_sections": DOGOVORY_BODY,
    },
    "registraciya_programm_evm": {
        "path": "/registraciya_programm_evm/",
        "page_class": "registraciya-programm-evm-page",
        "mascot": "software",
        "title": "Регистрация программ для ЭВМ и баз данных — LIREATE",
        "description": "Регистрация программы для ЭВМ и базы данных в Роспатенте, защита сайта и приложений: документы, пошлины, сопровождение. LIREATE.",
        "h1": "Регистрация программ для ЭВМ и баз данных",
        "lead": "Собираем заявку в Роспатент и помогаем выстроить защиту кода и сайта — без гарантий регистрации.",
        "eyebrow": "LIREATE · ПО и БД · ст. 1262 ГК РФ",
        "tags": ["программа для ЭВМ", "база данных", "Роспатент"],
        "panel_title": "Регистрация · маршрут",
        "kpi": [
            {"b": "ст. 1262", "s": "госрегистрация по желанию"},
            {"b": "62 дн.", "s": "предельный срок услуги"},
            {"b": "5 000 ₽", "s": "ориентир пошлины — таблица"},
        ],
        "feed": [
            "Аудит прав на код и БД",
            "Реферат и депонируемые материалы",
            "Оплата госпошлины",
            "Свидетельство о регистрации",
        ],
        "mini_stats": [
            {"v": "2015", "l": "на рынке с"},
            {"v": "15", "l": "специалистов"},
            {"v": "15 мин", "l": "ответ на заявку"},
        ],
        "nav": [
            {"href": "#included", "label": "Состав"},
            {"href": "#when", "label": "Для кого"},
            {"href": "#program", "label": "Этапы"},
            {"href": "#pricing", "label": "Пошлины"},
            {"href": "#blog", "label": "Блог"},
            {"href": "#faq", "label": "FAQ"},
            {"href": "#contact", "label": "Заявка"},
        ],
        "lead_topic": "Заявка: регистрация ПО",
        "tomail": "Регистрация программ для ЭВМ — заявка с сайта",
        "consent_form": "lx-registraciya-po",
        "faq": [
            {
                "q": "Обязательно ли регистрировать программу в Роспатенте?",
                "a": "Нет. Исключительное право на программу возникает с момента создания (ст. 1262, 1259 ГК РФ). Регистрация добровольная, но даёт официальное свидетельство.",
            },
            {
                "q": "Сколько стоит госпошлина за регистрацию ПО?",
                "a": "На странице госуслуги Роспатента указана пошлина 5 000 ₽ за регистрацию программы или БД. Точный пункт и сумму сверьте в таблице пошлин на rospatent.gov.ru на дату оплаты.",
            },
            {
                "q": "Можно ли в одной заявке зарегистрировать программу и базу данных?",
                "a": "Нет. На каждую программу и каждую базу данных подаётся отдельная заявка.",
            },
            {
                "q": "Защищает ли регистрация ПО название приложения?",
                "a": "Нет. Имя и иконку на витрине обычно охраняют товарным знаком. См. регистрацию товарного знака на LIREATE.",
            },
            {
                "q": "Что входит в защиту сайта?",
                "a": "Договоры с разработчиками, регистрация кода, при необходимости знак и претензионная работа. Объём определяем после аудита.",
            },
            {
                "q": "Гарантируете ли регистрацию?",
                "a": "Нет. Решение принимает Роспатент после проверки материалов.",
            },
        ],
        "body_sections": EVM_BODY,
    },
}


def write_pages(root: Path) -> None:
    for slug, cfg in PAGES.items():
        out_dir = root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        html_out = render(cfg)
        # FAQ section fix: body includes open faq section; close and append details inside render
        # Dogovory/evm bodies end at faq h2 - details appended in render via _faq_block but duplicate id
        # Merge: body ends before faq details - append faq items before closing faq section
        faq_html = _faq_block(cfg["faq"])
        html_out = html_out.replace(
            "<section class=\"lx-section lx-reveal\" id=\"faq\" style=\"display:none\" aria-hidden=\"true\"></section>",
            "",
        )
        html_out = html_out.replace(
            "<h2>Вопросы о договорах в сфере ИС</h2>\n",
            "<h2>Вопросы о договорах в сфере ИС</h2>\n" + faq_html + "\n</section>\n\n",
            1,
        ) if slug == "dogovory" else html_out.replace(
            "<h2>Вопросы о программах для ЭВМ и базах данных</h2>\n",
            "<h2>Вопросы о программах для ЭВМ и базах данных</h2>\n" + faq_html + "\n</section>\n\n",
            1,
        )
        (out_dir / "index.php").write_text(html_out, encoding="utf-8")
        blocks = out_dir / "blocks"
        blocks.mkdir(exist_ok=True)
        sticky_src = root.parent / "blocks" / "lireate-sticky-mobile.inc.php"
        if sticky_src.is_file():
            (blocks / "lireate-sticky-mobile.inc.php").write_text(
                sticky_src.read_text(encoding="utf-8"), encoding="utf-8"
            )


def main() -> None:
    root = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).resolve().parents[1] / "hosting-design" / "service-landings"
    )
    write_pages(root)
    print("RENDER_OK", root, *PAGES.keys())


if __name__ == "__main__":
    main()
