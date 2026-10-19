from .base_css import _esc, icon_svg, shared_styles
from .inline_tokens import (
    CARD_BODY_PX,
    CARD_HEAD_H,
    CARD_HEAD_PX,
    CHECK_BOX_PX,
    CHECK_ROW_H,
    CHECK_ROW_PX,
    CHIP_H,
    CHIP_ICON_PX,
    CHIP_TEXT_PX,
    COMP_W,
    CONC_BOX_H,
    CONC_BOX_W,
    CONC_CHIP_PX,
    CONC_LABEL_PX,
    CONC_TEXT_PX,
    HEADLINE_PX,
    ICON_MAX_PX,
    INLINE_H,
    INLINE_W,
    PAPER_MARGIN,
    STEP_NUM_PX,
    STEP_SUB_PX,
    STEP_TITLE_PX,
    STICKY_H,
    STICKY_TEXT_PX,
    STICKY_W,
)


def _chip(chip):
    icon = chip.get("icon") or "tag"
    text = chip.get("text") or ""
    return (
        '<span class="meta-chip">{svg}<span>{text}</span></span>'.format(
            svg=icon_svg(icon), text=_esc(text)
        )
    )


def _sticky(sticky):
    if not sticky:
        return '<div class="sticky-spacer"></div>'
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
        '<div class="sticky-note hand" data-layout-slot="slot-sticky" style="background:{bg}">'
        '<div class="sticky-tape"></div>{inner}</div>'
    ).format(bg=bg, inner=inner)


def _conclusion(conc):
    label = conc.get("label") or "итог"
    lines = conc.get("box_lines") or []
    highlight = conc.get("highlight_word") or ""
    chip = conc.get("chip") or ""
    marker = conc.get("marker_underline", False)
    parts = []
    for line in lines:
        if highlight and highlight in line:
            before, after = line.split(highlight, 1)
            span = '<span class="hl-pink">{0}</span>'.format(_esc(highlight))
            if marker:
                span = '<span class="hl-ul">{0}</span>'.format(span)
            parts.append(_esc(before) + span + _esc(after))
        else:
            parts.append(_esc(line))
    box_inner = "<br/>".join(parts)
    chip_s = (
        '<div class="conc-chip torn-chip black">{0}</div>'.format(_esc(chip)) if chip else ""
    )
    return (
        '<div class="conc-block" data-layout-slot="slot-conclusion">'
        '<span class="conc-label hand">{lab}</span>'
        '<svg class="conc-arrow" viewBox="0 0 40 24"><path d="M2 14 C14 4, 24 18, 36 10" '
        'stroke="#111" fill="none" stroke-width="2"/><path d="M30 6l8 6-10 2" stroke="#111" fill="none" stroke-width="2"/></svg>'
        '<div class="conc-box">{box}</div>{chip}</div>'
    ).format(lab=_esc(label), box=box_inner, chip=chip_s)


def _lines_html(lines, use_text=True):
    out = ""
    for line in (lines or [])[:4]:
        if use_text and line:
            out += '<p class="card-text">{0}</p>'.format(_esc(line))
        else:
            out += '<div class="bar"></div>'
    if not out:
        out = '<div class="bar"></div><div class="bar short"></div>'
    return out


def _side_checklist(item):
    check = ""
    for row in (item.get("side_checklist") or [])[:4]:
        check += '<div class="sc-row"><span class="ok-dot">✓</span><span>{0}</span></div>'.format(
            _esc(row)
        )
    if not check:
        return ""
    return '<div class="side-list" data-layout-slot="slot-side">{0}</div>'.format(check)


def _template_bad_good(item):
    bad, good = item.get("bad") or {}, item.get("good") or {}
    return (
        '<div class="main-row bad-good" data-layout-slot="slot-body">'
        '<div class="compare-pair">'
        '<div class="cmp-col"><div class="cmp-head bad-h"><span class="bx">✕</span>{bh}</div>'
        '<div class="cmp-body">{bb}</div></div>'
        '<div class="cmp-col"><div class="cmp-head good-h"><span class="gx">✓</span>{gh}</div>'
        '<div class="cmp-body">{gb}</div></div></div></div>'
    ).format(
        bh=_esc(bad.get("header") or "BAD"),
        bb=_lines_html(bad.get("lines")),
        gh=_esc(good.get("header") or "GOOD"),
        gb=_lines_html(good.get("lines")),
    )


def _template_process(item):
    steps = item.get("steps") or []
    cards = ""
    for i, step in enumerate(steps[:4]):
        variant = step.get("variant") or "lines"
        body = '<div class="bar"></div><div class="bar short"></div>'
        if variant == "toggles":
            body = (
                '<div class="tog-row"><span>A</span><span class="toggle on"></span></div>'
                '<div class="tog-row"><span>B</span><span class="toggle on"></span></div>'
            )
        elif variant == "icon":
            body = '<div class="icon-wrap">{0}</div>'.format(icon_svg("shield"))
        chip = step.get("chip") or ""
        chip_s = '<div class="step-label torn-chip white">{0}</div>'.format(_esc(chip)) if chip else ""
        cards += (
            '<div class="step">'
            '<div class="step-top"><span class="step-num">{n}</span>'
            '<div><div class="step-title">{t}</div><div class="step-sub">{s}</div></div></div>'
            '<div class="step-inner">{body}</div>{chip}</div>'
        ).format(
            n=i + 1,
            t=_esc(step.get("title") or ""),
            s=_esc(step.get("subtitle") or ""),
            body=body,
            chip=chip_s,
        )
        if i < len(steps) - 1:
            cards += '<div class="arr">→</div>'
    return '<div class="main-row process" data-layout-slot="slot-body"><div class="steps">{0}</div></div>'.format(
        cards
    )


def _template_checklist(item):
    title = item.get("checklist_title") or "Чеклист"
    rows = ""
    for row in (item.get("checklist_rows") or [])[:6]:
        icon = row.get("icon") or "doc"
        rows += (
            '<div class="ck-row"><span class="ck-box">✓</span>{ic}<span class="ck-txt">{tx}</span>'
            '<span class="ck-bars"><i></i><i></i><i></i></span></div>'
        ).format(ic=icon_svg(icon), tx=_esc(row.get("text") or ""))
    return (
        '<div class="main-row checklist" data-layout-slot="slot-body">'
        '<div class="ck-card"><div class="ck-title">{title}</div><div class="ck-line"></div>{rows}</div>'
        "</div>"
    ).format(title=_esc(title), rows=rows)


def build_inline_html(item, width, height):
    tmpl = item.get("template")
    bottom_left = ""
    if tmpl == "bad_good":
        main = _template_bad_good(item)
        bottom_left = _side_checklist(item)
    elif tmpl == "process":
        main = _template_process(item)
    elif tmpl == "checklist":
        main = _template_checklist(item)
    else:
        main = ""

    conc = _conclusion(item.get("conclusion") or {})
    chips = " ".join(_chip(c) for c in (item.get("chips") or [])[:3])
    headline = _esc(item.get("headline") or "")

    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{shared}
html, body {{ margin:0; width:{w}px; height:{h}px; overflow:hidden; }}
.stage {{ width:{w}px; height:{h}px; background:{navy}; display:flex; align-items:center; justify-content:center; }}
.sheet {{
  width:{w}px; height:{h}px; position:relative; box-sizing:border-box;
  background:{paper}; padding:0;
}}
#composition {{
  position:absolute; left:0; top:0; width:{w}px; height:{h}px;
  padding:{m}px; box-sizing:border-box;
  display:flex; flex-direction:column; justify-content:space-between;
}}
.inline-header {{
  display:grid; grid-template-columns: 1fr {sticky_w}px; gap:12px; align-items:start; margin-bottom:14px;
}}
h1.title {{
  font-size:{headline_px}px; font-weight:800; line-height:1.08; margin:0 0 10px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
}}
.meta-chip {{
  display:inline-flex; align-items:center; gap:8px; height:{chip_h}px; padding:0 14px;
  border:1px solid #e5e7eb; border-radius:999px; background:#fff;
  font-size:{chip_text}px; font-weight:600;
}}
.meta-chip svg {{ width:{chip_icon}px; height:{chip_icon}px; }}
.sticky-note {{
  width:{sticky_w}px; min-height:{sticky_h}px; padding:16px 14px; box-sizing:border-box;
  font-size:{sticky_text}px; line-height:1.2; transform:rotate(5deg);
  box-shadow:2px 5px 14px rgba(0,0,0,.15); position:relative;
}}
.sticky-tape {{
  position:absolute; top:-10px; left:50%; margin-left:-32px; width:64px; height:18px;
  background:rgba(235,220,185,.88);
}}
.sticky-ul {{ background:linear-gradient(transparent 58%, rgba(239,68,68,.55) 58%); }}
.sticky-spacer {{ width:{sticky_w}px; height:1px; }}
.main-row {{ margin-bottom:12px; }}
.bad-good {{ margin-bottom:6px; }}
.side-list {{ font-size:{card_body}px; padding:8px 0; }}
.compare-pair {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.cmp-head {{
  height:{card_head_h}px; display:flex; align-items:center; gap:10px; padding:0 12px;
  font-size:{card_head}px; font-weight:800; color:#fff; background:#111;
}}
.bx, .gx {{
  width:28px; height:28px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center;
  font-size:14px; font-weight:800;
}}
.bx {{ background:#ef4444; }}
.gx {{ background:#22c55e; }}
.cmp-body {{ border:1px solid #e5e7eb; padding:14px; background:#fff; min-height:132px; }}
.card-text {{ font-size:{card_body}px; line-height:1.35; margin:0 0 10px; }}
.bar {{ height:12px; background:#e5e7eb; border-radius:4px; margin:10px 0; }}
.bar.short {{ width:58%; }}
.sc-row {{ display:flex; gap:8px; margin:12px 0; align-items:flex-start; }}
.ok-dot {{
  width:22px; height:22px; border-radius:50%; background:#22c55e; color:#fff;
  display:inline-flex; align-items:center; justify-content:center; font-size:12px; flex-shrink:0;
}}
.process .steps {{ display:flex; align-items:flex-start; gap:8px; }}
.step {{
  width:268px; border:1px solid #e5e7eb; padding:12px; background:#fff; box-sizing:border-box;
}}
.step-top {{ display:flex; gap:10px; margin-bottom:10px; }}
.step-num {{
  width:{step_num}px; height:{step_num}px; border-radius:50%; background:#111; color:#fff;
  display:flex; align-items:center; justify-content:center; font-weight:800; font-size:18px; flex-shrink:0;
}}
.step-title {{ font-size:{step_title}px; font-weight:800; line-height:1.1; }}
.step-sub {{ font-size:{step_sub}px; color:#64748b; margin-top:4px; }}
.icon-wrap svg {{ width:{icon_max}px; height:{icon_max}px; display:block; margin:8px 0; }}
.step-label {{ font-size:18px; padding:6px 12px; margin-top:8px; display:inline-block; }}
.arr {{ font-size:28px; padding-top:48px; font-weight:700; }}
.tog-row {{ display:flex; justify-content:space-between; font-size:{card_body}px; margin:8px 0; }}
.toggle {{ width:40px; height:24px; border-radius:999px; background:#e5e7eb; position:relative; display:inline-block; }}
.toggle.on {{ background:#ff2d78; }}
.toggle.on::after {{
  content:''; position:absolute; right:3px; top:3px; width:18px; height:18px; background:#fff; border-radius:50%;
}}
.checklist .ck-card {{
  width:620px; border:1px solid #e5e7eb; padding:16px 18px; background:#fff; box-sizing:border-box;
}}
.ck-title {{ font-size:{card_head}px; font-weight:800; margin-bottom:10px; }}
.ck-line {{ height:1px; background:#e5e7eb; margin-bottom:8px; }}
.ck-row {{
  height:{check_row_h}px; display:flex; align-items:center; gap:12px; font-size:{check_row}px;
}}
.ck-box {{
  width:{check_box}px; height:{check_box}px; background:#ff2d78; color:#fff; border-radius:5px;
  display:flex; align-items:center; justify-content:center; font-weight:800; flex-shrink:0;
}}
.ck-row svg {{ width:22px; height:22px; flex-shrink:0; }}
.ck-bars {{ margin-left:auto; display:flex; gap:5px; }}
.ck-bars i {{ display:block; width:32px; height:8px; background:#e5e7eb; border-radius:3px; }}
.ck-bars i:nth-child(2) {{ width:20px; }}
.layout-bottom {{
  display:grid; grid-template-columns: 1fr auto; gap:16px; align-items:end; margin-top:6px;
}}
.conc-block {{ display:flex; flex-wrap:wrap; align-items:center; gap:8px; justify-content:flex-end; }}
.conc-label {{ font-size:{conc_label}px; }}
.conc-arrow {{ width:44px; height:28px; }}
.conc-box {{
  width:{conc_box_w}px; min-height:{conc_box_h}px; border:3px solid #111; padding:12px 16px;
  font-size:{conc_text}px; font-weight:800; line-height:1.05; background:#fff; box-sizing:border-box;
}}
.hl-pink {{ color:#ff2d78; }}
.hl-ul {{ background:linear-gradient(transparent 62%, rgba(239,68,68,.5) 62%); }}
.conc-chip {{ font-size:{conc_chip}px; padding:8px 14px; margin-top:6px; display:inline-block; transform:rotate(-3deg); }}
.tape-corner {{
  position:absolute; width:46px; height:16px; background:linear-gradient(135deg,rgba(22,22,22,.9),rgba(8,8,8,.92));
  opacity:.75; z-index:20;
}}
.tl {{ top:10px; left:20px; transform:rotate(-28deg); }}
.tr {{ top:12px; right:24px; transform:rotate(24deg); }}
</style></head><body>
<div class="stage">
  <div class="paper paper-torn sheet" data-layout-paper="1">
    <div class="tape-corner tl"></div><div class="tape-corner tr"></div>
    <div id="composition">
      <header class="inline-header">
        <div>
          <h1 class="title" data-layout-slot="slot-headline">{headline_text}</h1>
          <div data-layout-slot="slot-chips">{chips}</div>
        </div>
        {sticky}
      </header>
      {main}
      <div class="layout-bottom">
        <div class="bottom-left">{bottom_left}</div>
        {conc}
      </div>
    </div>
  </div>
</div>
</body></html>""".format(
        shared=shared_styles(),
        w=width,
        h=height,
        m=PAPER_MARGIN,
        navy="#0b1020",
        paper="#fafaf8",
        sticky_w=STICKY_W,
        headline_px=HEADLINE_PX,
        chip_h=CHIP_H,
        chip_text=CHIP_TEXT_PX,
        chip_icon=CHIP_ICON_PX,
        sticky_h=STICKY_H,
        sticky_text=STICKY_TEXT_PX,
        card_head_h=CARD_HEAD_H,
        card_head=CARD_HEAD_PX,
        card_body=CARD_BODY_PX,
        step_num=STEP_NUM_PX,
        step_title=STEP_TITLE_PX,
        step_sub=STEP_SUB_PX,
        icon_max=ICON_MAX_PX,
        check_row_h=CHECK_ROW_H,
        check_row=CHECK_ROW_PX,
        check_box=CHECK_BOX_PX,
        conc_label=CONC_LABEL_PX,
        conc_box_w=CONC_BOX_W,
        conc_box_h=CONC_BOX_H,
        conc_text=CONC_TEXT_PX,
        conc_chip=CONC_CHIP_PX,
        headline_text=headline,
        chips=chips,
        sticky=_sticky(item.get("sticky")),
        main=main,
        conc=conc,
        bottom_left=bottom_left,
    )
