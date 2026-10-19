from .base_css import _esc, shared_styles


def _headline_html(lines, highlight):
    parts = []
    for line in lines:
        if highlight and highlight in line:
            a, b = line.split(highlight, 1)
            parts.append(
                '<div class="hl-line">{0}<span class="hl-accent">{1}</span>{2}</div>'.format(
                    _esc(a), _esc(highlight), _esc(b)
                )
            )
        else:
            parts.append('<div class="hl-line">{0}</div>'.format(_esc(line)))
    return "\n".join(parts)


def _sticky_html(text, underline, bg):
    if not text:
        return ""
    if underline and underline in text:
        a, b = text.split(underline, 1)
        inner = '{0}<span class="sticky-ul">{1}</span>{2}'.format(_esc(a), _esc(underline), _esc(b))
    else:
        inner = _esc(text)
    return (
        '<div class="cover-sticky hand" data-layout-slot="slot-sticky" style="background:{bg}">'
        '<div class="sticky-tape-beige"></div><div class="sticky-text">{inner}</div></div>'
    ).format(bg=bg, inner=inner)


def build_cover_html(spec, width, height):
    lines = spec.get("headline_lines") or []
    highlight = (spec.get("highlight") or "").strip()
    sticky_bg = "#f7e58c" if (spec.get("sticky_color") or "yellow") == "yellow" else "#ff8fc8"
    badge = spec.get("badge_label") or "ТЗ"
    label_chips = spec.get("label_chips") or []
    ui_title = spec.get("ui_card_title") or "Настройки"
    ui_rows = spec.get("ui_card_rows") or []

    labels_html = ""
    rots = (-4, 2, -3)
    for i, chip in enumerate(label_chips[:3]):
        if isinstance(chip, (list, tuple)):
            text, variant = chip[0], chip[1]
        else:
            text, variant = chip.get("text", ""), chip.get("variant", "black")
        labels_html += (
            '<div class="torn-chip {cls} chip-tilt" style="--rot:{rot}deg">{txt}</div>'.format(
                cls=variant, txt=_esc(text), rot=rots[i % 3]
            )
        )

    ui_rows_html = ""
    for i, row in enumerate(ui_rows[:4]):
        on = "on" if i < 2 else ""
        ui_rows_html += (
            '<div class="ui-row"><span>{label}</span><span class="toggle {on}"></span></div>'
        ).format(label=_esc(row), on=on)

    hl_px = max(44, int(height * 0.13))
    sw, sh = width, height

    arrow_svg = (
        '<svg class="cover-arrow" data-layout-slot="slot-arrow" viewBox="0 0 100 36" aria-hidden="true">'
        '<path d="M8 28 C42 8, 58 30, 88 12" stroke="#111" fill="none" stroke-width="2.2"/>'
        '<path d="M80 6l12 8-14 3" stroke="#111" fill="none" stroke-width="2"/>'
        "</svg>"
    )

    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{shared}
html, body {{ margin:0; width:{w}px; height:{h}px; overflow:hidden; }}
.stage {{ width:{w}px; height:{h}px; background:#0b1020; display:flex; align-items:center; justify-content:center; }}
.sheet {{
  width:{sw}px; height:{sh}px; position:relative; box-sizing:border-box;
  display:grid; grid-template-columns: 54% 46%; padding:20px 22px 16px 26px;
}}
.col-left {{ display:flex; align-items:center; position:relative; padding-right:8px; }}
.col-right {{ position:relative; }}
.hl {{
  font-size:{hl_px}px; font-weight:800; line-height:1.05; letter-spacing:-0.03em;
}}
.hl-accent {{ color:#ff1f6b; }}
.hl-line {{ margin-bottom:0.05em; }}
.cover-arrow {{
  position:absolute; right:-4px; top:38%; width:90px; height:auto; pointer-events:none;
}}
.cover-sticky {{
  position:absolute; top:44px; left:6px; width:230px; min-height:150px;
  padding:18px 16px; box-sizing:border-box; font-size:22px; line-height:1.15;
  transform:rotate(4deg); z-index:4; box-shadow:2px 6px 14px rgba(0,0,0,.18);
}}
.sticky-ul {{ background:linear-gradient(transparent 58%, rgba(239,68,68,.55) 58%); }}
.sticky-tape-beige {{
  position:absolute; top:-10px; left:50%; margin-left:-34px; width:68px; height:18px;
  background:rgba(235,220,185,.88); transform:rotate(-2deg);
}}
.slot-badge {{
  position:absolute; top:0; right:0; border:3px solid #111; padding:8px 14px;
  font-weight:800; font-size:20px; white-space:nowrap; z-index:6; background:#fff;
}}
.slot-chips {{
  position:absolute; top:200px; right:0; width:100%;
  display:flex; flex-direction:column; align-items:flex-end; gap:8px; z-index:3;
}}
.chip-tilt {{ font-size:18px; padding:8px 16px; transform:rotate(var(--rot)); }}
.slot-ui {{
  position:absolute; bottom:8px; right:0; width:94%; z-index:5;
  background:#fff; border-radius:12px; padding:12px 14px 10px;
  box-shadow:0 10px 26px rgba(0,0,0,.14); border:1px solid #e5e7eb;
  font-size:17px;
}}
.slot-ui h4 {{ font-size:17px; margin:0 0 8px; font-weight:700; }}
.ui-row {{ display:flex; justify-content:space-between; align-items:center; margin:6px 0; }}
.toggle {{ width:36px; height:20px; border-radius:999px; background:#e5e7eb; position:relative; flex-shrink:0; }}
.toggle.on {{ background:#ff2d78; }}
.toggle.on::after {{
  content:''; position:absolute; right:3px; top:3px; width:14px; height:14px; background:#fff; border-radius:50%;
}}
.ui-foot {{ margin-top:8px; display:flex; gap:10px; justify-content:flex-end; font-size:12px; align-items:center; }}
.muted {{ color:#64748b; }}
.apply {{ background:#ff2d78; color:#fff; padding:4px 12px; border-radius:6px; font-weight:600; }}
.tape-corner {{
  position:absolute; width:42px; height:14px;
  background:linear-gradient(135deg,rgba(22,22,22,.88),rgba(8,8,8,.92));
  opacity:.75; z-index:10;
}}
.tape-tl {{ top:6px; left:22px; transform:rotate(-30deg); }}
.tape-tr {{ top:8px; right:26px; transform:rotate(26deg); }}
.brand-mark {{
  position:absolute; bottom:6px; right:10px; font-size:11px; font-weight:700;
  letter-spacing:0.14em; color:#64748b; z-index:6;
}}
</style></head><body>
<div class="stage">
  <div class="paper paper-torn sheet" data-layout-paper="1">
    <div class="tape-corner tape-tl"></div><div class="tape-corner tape-tr"></div>
    <div class="col-left">
      <div class="hl" data-layout-slot="slot-headline">{headline}</div>
      {arrow}
    </div>
    <div class="col-right" data-layout-slot="slot-body">
      <div class="slot-badge" data-layout-slot="slot-badge">{badge}</div>
      {sticky}
      <div class="slot-chips" data-layout-slot="slot-chips">{labels}</div>
      <div class="slot-ui" data-layout-slot="slot-ui-card">
        <h4>{ui_title}</h4>{ui_rows}
        <div class="ui-foot"><span class="muted">Сохранить</span><span class="apply">Применить</span></div>
      </div>
    </div>
    <div class="brand-mark">LIREATE</div>
  </div>
</div>
</body></html>""".format(
        shared=shared_styles(),
        w=width,
        h=height,
        sw=sw,
        sh=sh,
        hl_px=hl_px,
        headline=_headline_html(lines, highlight),
        arrow=arrow_svg,
        badge=_esc(badge),
        sticky=_sticky_html(spec.get("sticky_text") or "", spec.get("sticky_underline") or "", sticky_bg),
        labels=labels_html,
        ui_title=_esc(ui_title),
        ui_rows=ui_rows_html,
    )
