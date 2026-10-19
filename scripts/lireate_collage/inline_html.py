from .base_css import _esc, chip_html, conclusion_html, icon_svg, shared_styles


def _headline_block(headline, chips):
    chips_html = " ".join(chip_html(c) for c in (chips or [])[:4])
    return (
        '<div class="head-block">'
        '<h1 class="title">{hl}</h1>'
        '<div class="chips">{chips}</div></div>'.format(hl=_esc(headline), chips=chips_html)
    )


def _sticky_block(sticky):
    if not sticky:
        return ""
    color = sticky.get("color") or "pink"
    bg = "#ff8fc8" if color == "pink" else "#f7e58c"
    return (
        '<div class="sticky hand" style="background:{bg};top:24px;right:32px">'
        '<div class="sticky-tape"></div>{txt}</div>'.format(bg=bg, txt=_esc(sticky.get("text") or ""))
    )


def _template_bad_good(item):
    bad = item.get("bad") or {}
    good = item.get("good") or {}
    checklist = item.get("side_checklist") or []

    def card(side, data, badge):
        lines = data.get("lines") or []
        body = "".join('<div class="mock-line">{0}</div>'.format(_esc(x)) for x in lines[:3])
        if not body:
            body = '<div class="mock-line dim">Текст публикации…</div><div class="mock-line dim">…</div>'
        return (
            '<div class="compare-col">'
            '<div class="compare-head">{badge}<span>{hdr}</span></div>'
            '<div class="compare-card">{inner}</div></div>'
        ).format(badge=badge, hdr=_esc(data.get("header") or side), inner=body)

    bad_badge = '<span class="badge-x">✕</span>'
    good_badge = '<span class="badge-ok">✓</span>'
    cols = card("BAD", bad, bad_badge) + card("GOOD", good, good_badge)
    check_html = ""
    for row in checklist[:4]:
        check_html += (
            '<div class="check-row"><span class="badge-ok small">✓</span><span>{0}</span></div>'.format(
                _esc(row)
            )
        )
    return (
        '<div class="body-grid bad-good">'
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
                '<div class="ui-row" style="margin:4px 0"><span>Слой A</span><span class="toggle on" style="display:inline-block"></span></div>'
                '<div class="ui-row" style="margin:4px 0"><span>Слой B</span><span class="toggle on" style="display:inline-block"></span></div>'
            )
        elif variant == "icon":
            inner = '<div style="margin:8px 0">{0}</div>'.format(icon_svg("shield"))
        chip = step.get("chip") or ""
        chip_s = (
            '<div class="torn-chip white" style="margin-top:8px;font-size:11px">{0}</div>'.format(_esc(chip))
            if chip
            else ""
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
    return '<div class="body-grid process"><div class="steps-row">{0}</div></div>'.format(
        "".join(inner_cards)
    )


def _template_checklist(item):
    title = item.get("checklist_title") or "Чеклист перед публикацией"
    rows = item.get("checklist_rows") or []
    rows_html = ""
    for row in rows[:6]:
        icon = row.get("icon") or "check"
        rows_html += (
            '<div class="cl-row">'
            '<span class="cl-check">✓</span>{icon}<span class="cl-text">{txt}</span>'
            '<span class="cl-bars"><i></i><i></i><i></i></span></div>'
        ).format(icon=icon_svg(icon), txt=_esc(row.get("text") or ""))
    return (
        '<div class="body-grid checklist">'
        '<div class="cl-card"><h3>{title}</h3><div class="cl-sep"></div>{rows}</div></div>'
    ).format(title=_esc(title), rows=rows_html)


def build_inline_html(item, width, height):
    tmpl = item.get("template")
    if tmpl == "bad_good":
        body = _template_bad_good(item)
    elif tmpl == "process":
        body = _template_process(item)
    elif tmpl == "checklist":
        body = _template_checklist(item)
    else:
        body = ""

    conc = conclusion_html(item.get("conclusion") or {})

    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{shared}
.stage {{ width: {w}px; height: {h}px; position: relative; display: flex; align-items: center; justify-content: center; }}
.sheet {{
  width: {iw}px; min-height: {ih}px; position: relative; padding: 32px 36px 28px;
}}
.head-block .title {{ font-size: 28px; font-weight: 800; line-height: 1.12; max-width: 72%; margin-bottom: 12px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }}
.body-grid {{ margin-top: 8px; }}
.bad-good {{ display: grid; grid-template-columns: 1fr 180px; gap: 16px; }}
.compare-wrap {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
.compare-head {{ background: #111; color: #fff; padding: 8px 10px; font-weight: 700; font-size: 13px; display: flex; align-items: center; gap: 8px; }}
.compare-card {{ border: 1px solid #e5e7eb; padding: 12px; min-height: 100px; background: #fff; }}
.mock-line {{ height: 10px; background: #e5e7eb; border-radius: 4px; margin: 8px 0; }}
.mock-line.short {{ width: 60%; }}
.mock-line.dim {{ opacity: .5; }}
.badge-x, .badge-ok {{
  display: inline-flex; width: 22px; height: 22px; border-radius: 50%;
  align-items: center; justify-content: center; font-size: 12px; font-weight: 800;
}}
.badge-x {{ background: #ef4444; color: #fff; }}
.badge-ok {{ background: #22c55e; color: #fff; }}
.badge-ok.small {{ width: 18px; height: 18px; font-size: 10px; }}
.check-row {{ display: flex; gap: 8px; align-items: flex-start; font-size: 12px; margin: 8px 0; }}
.process .steps-row {{ display: flex; align-items: flex-start; gap: 8px; flex-wrap: wrap; }}
.step-card {{
  flex: 1; min-width: 140px; border: 1px solid #e5e7eb; padding: 12px; background: #fff;
}}
.step-num {{
  width: 28px; height: 28px; border-radius: 50%; background: #111; color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 800; margin-bottom: 8px;
}}
.step-title {{ font-weight: 700; font-size: 14px; }}
.step-sub {{ font-size: 11px; color: #64748b; margin-bottom: 8px; }}
.step-arrow {{ font-size: 24px; align-self: center; padding-top: 40px; }}
.checklist .cl-card {{ border: 1px solid #e5e7eb; padding: 16px; max-width: 55%; background: #fff; }}
.cl-card h3 {{ font-size: 15px; font-weight: 700; margin-bottom: 8px; }}
.cl-sep {{ height: 1px; background: #e5e7eb; margin-bottom: 12px; }}
.cl-row {{ display: flex; align-items: center; gap: 10px; margin: 10px 0; font-size: 13px; }}
.cl-check {{
  width: 18px; height: 18px; background: #ff2d78; color: #fff; border-radius: 4px;
  display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800;
}}
.cl-bars {{ margin-left: auto; display: flex; gap: 4px; }}
.cl-bars i {{ display: block; width: 24px; height: 6px; background: #e5e7eb; border-radius: 2px; }}
.cl-bars i:nth-child(2) {{ width: 16px; }}
.cl-bars i:nth-child(3) {{ width: 32px; }}
.toggle {{ width: 36px; height: 20px; border-radius: 999px; background: #e5e7eb; position: relative; }}
.toggle.on {{ background: #ff2d78; }}
.toggle.on::after {{
  content: ''; position: absolute; right: 3px; top: 3px; width: 14px; height: 14px;
  background: #fff; border-radius: 50%;
}}
</style></head><body>
<div class="stage">
  <div class="paper paper-torn sheet">
    <div class="tape tape-tl"></div><div class="tape tape-tr"></div>
    {head}
    {sticky}
    {body}
    {conc}
  </div>
</div>
</body></html>""".format(
        shared=shared_styles(),
        w=width,
        h=height,
        iw=int(width * 0.92),
        ih=int(height * 0.86),
        head=_headline_block(item.get("headline") or "", item.get("chips")),
        sticky=_sticky_block(item.get("sticky")),
        body=body,
        conc=conc,
    )
