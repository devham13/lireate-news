from .base_css import _esc, chip_html, conclusion_html, icon_svg, shared_styles


def _sticky_block(sticky):
    if not sticky:
        return ""
    color = sticky.get("color") or "pink"
    bg = "#ff8fc8" if color == "pink" else "#f7e58c"
    text = sticky.get("text") or ""
    ul = sticky.get("underline") or ""
    if ul and ul in text:
        a, b = text.split(ul, 1)
        inner = '{0}<span class="sticky-ul">{1}</span>{2}'.format(_esc(a), _esc(ul), _esc(b))
    else:
        inner = _esc(text)
    return (
        '<div class="sticky hand slot-sticky-inline" data-layout-slot="slot-sticky" '
        'style="background:{bg}"><div class="sticky-tape-beige"></div><div>{txt}</div></div>'
    ).format(bg=bg, txt=inner)


def _header_section(headline, chips, sticky_html):
    chips_html = " ".join(chip_html(c) for c in (chips or [])[:3])
    return (
        '<header class="head-block">'
        '<h1 class="title" data-layout-slot="slot-headline">{hl}</h1>'
        '<div class="chips" data-layout-slot="slot-chips">{chips}</div>'
        '{sticky}</header>'.format(hl=_esc(headline), chips=chips_html, sticky=sticky_html)
    )


def _template_bad_good(item):
    bad = item.get("bad") or {}
    good = item.get("good") or {}
    checklist = item.get("side_checklist") or []

    def card(data, badge):
        lines = data.get("lines") or []
        body = "".join('<div class="mock-line">{0}</div>'.format(_esc(x)) for x in lines[:3])
        if not body:
            body = '<div class="mock-line dim"></div><div class="mock-line dim short"></div>'
        return (
            '<div class="compare-col">'
            '<div class="compare-head">{badge}<span>{hdr}</span></div>'
            '<div class="compare-card">{inner}</div></div>'
        ).format(badge=badge, hdr=_esc(data.get("header") or ""), inner=body)

    cols = card(bad, '<span class="badge-x">✕</span>') + card(
        good, '<span class="badge-ok">✓</span>'
    )
    check_html = ""
    for row in checklist[:4]:
        check_html += (
            '<div class="check-row"><span class="badge-ok small">✓</span><span>{0}</span></div>'.format(
                _esc(row)
            )
        )
    return (
        '<div class="body-grid bad-good" data-layout-slot="slot-body">'
        '<div class="compare-wrap">{cols}</div>'
        '<div class="side-check">{check}</div></div>'.format(cols=cols, check=check_html)
    )


def _template_process(item):
    steps = item.get("steps") or []
    cards = []
    for i, step in enumerate(steps[:4]):
        variant = step.get("variant") or "lines"
        inner = '<div class="mock-line"></div><div class="mock-line short"></div>'
        if variant == "toggles":
            inner = (
                '<div class="ui-row"><span>параметр A</span><span class="toggle on"></span></div>'
                '<div class="ui-row"><span>параметр B</span><span class="toggle on"></span></div>'
            )
        elif variant == "icon":
            inner = '<div class="step-icon">{0}</div>'.format(icon_svg("shield"))
        chip = step.get("chip") or ""
        chip_s = (
            '<div class="torn-chip white chip-mini">{0}</div>'.format(_esc(chip)) if chip else ""
        )
        cards.append(
            '<div class="step-card">'
            '<div class="step-num">{n}</div>'
            '<div class="step-title">{t}</div>'
            '<div class="step-sub">{s}</div>'
            '<div class="step-body">{inner}</div>{chip}</div>'.format(
                n=i + 1,
                t=_esc(step.get("title") or ""),
                s=_esc(step.get("subtitle") or ""),
                inner=inner,
                chip=chip_s,
            )
        )
    inner_cards = []
    for i, c in enumerate(cards):
        inner_cards.append(c)
        if i < len(cards) - 1:
            inner_cards.append('<div class="step-arrow">→</div>')
    return '<div class="body-grid process" data-layout-slot="slot-body"><div class="steps-row">{0}</div></div>'.format(
        "".join(inner_cards)
    )


def _template_checklist(item, conclusion_html_str=""):
    title = item.get("checklist_title") or "Чеклист"
    rows = item.get("checklist_rows") or []
    rows_html = ""
    for row in rows[:6]:
        icon = row.get("icon") or "doc"
        rows_html += (
            '<div class="cl-row">'
            '<span class="cl-check">✓</span>{icon}<span class="cl-text">{txt}</span>'
            '<span class="cl-bars"><i></i><i></i><i></i></span></div>'
        ).format(icon=icon_svg(icon), txt=_esc(row.get("text") or ""))
    return (
        '<div class="body-grid checklist" data-layout-slot="slot-body">'
        '<div class="cl-card"><h3>{title}</h3><div class="cl-sep"></div>{rows}</div>'
        '<div class="cl-conc">{conc}</div></div>'
    ).format(title=_esc(title), rows=rows_html, conc=conclusion_html_str)


def build_inline_html(item, width, height):
    tmpl = item.get("template")
    if tmpl == "bad_good":
        body = _template_bad_good(item)
    elif tmpl == "process":
        body = _template_process(item)
    elif tmpl == "checklist":
        body = _template_checklist(item, conclusion_html(item.get("conclusion") or {}))
        conc = ""
    else:
        body = ""
        conc = ""

    if tmpl != "checklist":
        conc = '<div data-layout-slot="slot-conclusion">' + conclusion_html(item.get("conclusion") or {}) + "</div>"
    title_px = max(32, int(height * 0.038))
    sheet_w = int(width * 0.96)
    sheet_h = int(height * 0.92)

    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{shared}
.sticky-ul {{ background: linear-gradient(transparent 55%, rgba(239,68,68,.5) 55%); }}
.sticky-tape-beige {{
  position: absolute; top: -9px; left: 50%; margin-left: -28px;
  width: 56px; height: 14px; background: rgba(235,220,185,.85);
}}
.stage {{ width: {w}px; height: {h}px; display: flex; align-items: center; justify-content: center; }}
.sheet {{
  width: {sw}px; height: {sh}px; position: relative;
  padding: 28px 32px 24px;
  display: flex; flex-direction: column;
}}
.head-block {{
  display: grid;
  grid-template-columns: 1fr 220px;
  grid-template-rows: auto auto;
  column-gap: 16px; row-gap: 8px;
  margin-bottom: 12px; flex-shrink: 0; align-items: start;
}}
.head-block .title {{ font-size: {title_px}px; font-weight: 800; line-height: 1.08; grid-column: 1; grid-row: 1; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 8px; grid-column: 1; grid-row: 2; }}
.chip {{ font-size: 15px; padding: 7px 14px; }}
.slot-sticky-inline {{
  grid-column: 2; grid-row: 1 / span 2;
  align-self: start; justify-self: end;
  width: 200px; position: relative;
  padding: 14px 12px; font-size: 18px; line-height: 1.15;
  transform: rotate(4deg); z-index: 4;
}}
.body-grid {{ flex: 1; display: flex; flex-direction: column; justify-content: center; min-height: 0; }}
.bad-good {{ display: grid; grid-template-columns: 1fr 170px; gap: 14px; align-items: stretch; }}
.compare-wrap {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.compare-head {{ background: #111; color: #fff; padding: 10px; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 8px; }}
.compare-card {{ border: 1px solid #e5e7eb; padding: 14px; min-height: 120px; background: #fff; font-size: 13px; }}
.mock-line {{ height: 11px; background: #e5e7eb; border-radius: 4px; margin: 9px 0; }}
.mock-line.short {{ width: 55%; }}
.mock-line.dim {{ opacity: .45; }}
.badge-x, .badge-ok {{
  display: inline-flex; width: 24px; height: 24px; border-radius: 50%;
  align-items: center; justify-content: center; font-size: 13px; font-weight: 800;
}}
.badge-x {{ background: #ef4444; color: #fff; }}
.badge-ok {{ background: #22c55e; color: #fff; }}
.badge-ok.small {{ width: 18px; height: 18px; font-size: 10px; }}
.check-row {{ display: flex; gap: 8px; font-size: 13px; margin: 10px 0; }}
.process .steps-row {{ display: flex; align-items: stretch; gap: 6px; width: 100%; }}
.step-card {{
  flex: 1; border: 1px solid #e5e7eb; padding: 12px 10px; background: #fff;
  display: flex; flex-direction: column;
}}
.step-num {{
  width: 30px; height: 30px; border-radius: 50%; background: #111; color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 800; margin-bottom: 6px;
}}
.step-title {{ font-weight: 700; font-size: 15px; }}
.step-sub {{ font-size: 12px; color: #64748b; margin-bottom: 6px; }}
.step-body {{ flex: 1; }}
.step-icon svg {{ width: 36px; height: 36px; }}
.step-arrow {{ font-size: 22px; align-self: center; padding-top: 36px; }}
.chip-mini {{ font-size: 11px; margin-top: 6px; display: inline-block; }}
.checklist {{ flex-direction: row; gap: 16px; align-items: stretch; }}
.cl-card {{ border: 1px solid #e5e7eb; padding: 14px 16px; flex: 1.2; background: #fff; min-width: 0; }}
.cl-conc {{ flex: 0.85; display: flex; align-items: flex-end; padding-bottom: 4px; }}
.cl-conc .conclusion-wrap {{ margin-top: 0; }}
.cl-card h3 {{ font-size: 16px; font-weight: 700; margin-bottom: 8px; }}
.cl-sep {{ height: 1px; background: #e5e7eb; margin-bottom: 10px; }}
.cl-row {{ display: flex; align-items: center; gap: 10px; margin: 8px 0; font-size: 14px; }}
.cl-row svg {{ width: 18px; height: 18px; flex-shrink: 0; }}
.cl-text {{ flex: 1; min-width: 0; }}
.cl-check {{
  width: 20px; height: 20px; background: #ff2d78; color: #fff; border-radius: 4px;
  display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 800;
}}
.cl-bars {{ margin-left: auto; display: flex; gap: 4px; }}
.cl-bars i {{ display: block; width: 28px; height: 7px; background: #e5e7eb; border-radius: 2px; }}
.toggle {{ width: 36px; height: 20px; border-radius: 999px; background: #e5e7eb; position: relative; display: inline-block; }}
.toggle.on {{ background: #ff2d78; }}
.toggle.on::after {{
  content: ''; position: absolute; right: 3px; top: 3px; width: 14px; height: 14px;
  background: #fff; border-radius: 50%;
}}
.ui-row {{ display: flex; justify-content: space-between; align-items: center; font-size: 12px; margin: 4px 0; }}
.conclusion-wrap {{ margin-top: 8px; flex-shrink: 0; }}
.tape-corner {{
  position: absolute; width: 44px; height: 16px;
  background: linear-gradient(135deg, rgba(22,22,22,.88), rgba(8,8,8,.92));
  opacity: .7; z-index: 10;
}}
.tape-tl {{ top: 8px; left: 24px; transform: rotate(-30deg); }}
.tape-tr {{ top: 10px; right: 28px; transform: rotate(26deg); }}
</style></head><body>
<div class="stage">
  <div class="paper paper-torn sheet">
    <div class="tape-corner tape-tl"></div>
    <div class="tape-corner tape-tr"></div>
    {head}
    {body}
    {conc}
  </div>
</div>
</body></html>""".format(
        shared=shared_styles(),
        w=width,
        h=height,
        sw=sheet_w,
        sh=sheet_h,
        title_px=title_px,
        head=_header_section(
            item.get("headline") or "",
            item.get("chips"),
            _sticky_block(item.get("sticky")),
        ),
        body=body,
        conc=conc,
    )
