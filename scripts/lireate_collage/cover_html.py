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
        '<div class="sticky hand slot-sticky" data-layout-slot="slot-sticky" style="background:{bg}">'
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

    # Arrow lives in right column left edge, curves toward sticky (does not enter left col)
    arrow_svg = (
        '<svg class="slot-arrow" data-layout-slot="slot-arrow" viewBox="0 0 90 44" aria-hidden="true">'
        '<path d="M6 32 C30 6, 52 36, 78 14" stroke="#111" fill="none" stroke-width="2.2"/>'
        '<path d="M70 8l12 8-14 3" stroke="#111" fill="none" stroke-width="2"/>'
        "</svg>"
    )

    hl_px = max(48, int(height * 0.125))
    sheet_w = int(width * 0.97)
    sheet_h = int(height * 0.94)

    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{shared}
.stage {{ width: {w}px; height: {h}px; display: flex; align-items: center; justify-content: center; }}
.sheet {{
  width: {sw}px; height: {sh}px; position: relative;
  display: grid;
  grid-template-columns: 55% 45%;
  grid-template-rows: 1fr;
  padding: 28px 32px 24px 36px;
  gap: 0;
}}
.col-left {{
  display: flex; align-items: center;
  padding-right: 12px;
  z-index: 1;
}}
.col-right {{
  position: relative;
  height: 100%;
  min-height: 0;
}}
.hl {{
  font-size: {hl_px}px;
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.03em;
  width: 100%;
}}
.hl-accent {{ color: #ff1f6b; }}
.hl-line {{ margin-bottom: 0.06em; }}
.slot-badge {{
  position: absolute; top: 0; right: 0;
  border: 3px solid #111; padding: 10px 16px;
  font-weight: 800; font-size: 22px;
  white-space: nowrap; z-index: 5;
  background: #fff;
}}
.slot-sticky {{
  position: absolute; top: 6%; left: 0; width: 78%;
  padding: 16px 14px 14px;
  font-size: 22px; line-height: 1.2;
  transform: rotate(3deg);
  z-index: 4;
  box-shadow: 2px 6px 14px rgba(0,0,0,.18);
}}
.sticky-text {{ font-size: 20px; }}
.sticky-ul {{
  text-decoration: none;
  background: linear-gradient(transparent 55%, rgba(239,68,68,.55) 55%);
}}
.sticky-tape-beige {{
  position: absolute; top: -9px; left: 50%; margin-left: -30px;
  width: 60px; height: 16px;
  background: rgba(235,220,185,.82);
  transform: rotate(-3deg);
  border-radius: 1px;
}}
.slot-chips {{
  position: absolute; top: 34%; right: 0; width: 92%;
  display: flex; flex-direction: column;
  align-items: flex-end; gap: 10px;
  z-index: 3;
}}
.chip-tilt {{ font-size: 18px; padding: 8px 16px; transform: rotate(var(--rot)); }}
.slot-ui {{
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 42%;
  background: #fff; border-radius: 14px; padding: 14px 16px 12px;
  box-shadow: 0 10px 28px rgba(0,0,0,.14); border: 1px solid #e5e7eb;
  font-size: 14px; z-index: 2;
}}
.slot-ui h4 {{ font-size: 15px; margin-bottom: 8px; font-weight: 700; }}
.ui-foot {{ margin-top: auto; padding-top: 8px; display: flex; gap: 12px; justify-content: flex-end; font-size: 12px; align-items: center; }}
.muted {{ color: #64748b; }}
.apply {{ background: #ff2d78; color: #fff; padding: 5px 14px; border-radius: 6px; font-weight: 600; }}
.slot-ui {{ display: flex; flex-direction: column; }}
.ui-row {{ display: flex; justify-content: space-between; align-items: center; margin: 7px 0; }}
.toggle {{
  width: 38px; height: 22px; border-radius: 999px; background: #e5e7eb; position: relative; flex-shrink: 0;
}}
.toggle.on {{ background: #ff2d78; }}
.toggle.on::after {{
  content: ''; position: absolute; right: 3px; top: 3px; width: 16px; height: 16px;
  background: #fff; border-radius: 50%;
}}
.slot-arrow {{
  position: absolute; top: 20%; left: 4%; width: 38%; height: auto;
  z-index: 2; pointer-events: none;
}}
.tape-corner {{
  position: absolute; width: 48px; height: 18px;
  background: linear-gradient(135deg, rgba(22,22,22,.88), rgba(8,8,8,.92));
  opacity: .75; border-radius: 2px; z-index: 10;
}}
.tape-tl {{ top: 6px; left: 28px; transform: rotate(-32deg); }}
.tape-tr {{ top: 8px; right: 32px; transform: rotate(28deg); }}
.brand-mark {{
  position: absolute; bottom: 8px; right: 12px;
  font-size: 11px; font-weight: 700; letter-spacing: 0.14em;
  color: #64748b; z-index: 6;
}}
</style></head><body>
<div class="stage">
  <div class="paper paper-torn sheet">
    <div class="tape-corner tape-tl"></div>
    <div class="tape-corner tape-tr"></div>
    <div class="col-left">
      <div class="hl slot-headline" data-layout-slot="slot-headline">{headline}</div>
    </div>
    <div class="col-right">
      {arrow}
      <div class="slot-badge" data-layout-slot="slot-badge">{badge}</div>
      {sticky}
      <div class="slot-chips" data-layout-slot="slot-chips">{labels}</div>
      <div class="slot-ui" data-layout-slot="slot-ui-card">
        <h4>{ui_title}</h4>
        {ui_rows}
        <div class="ui-foot">
          <span class="muted">Сохранить</span>
          <span class="apply">Применить</span>
        </div>
      </div>
    </div>
    <div class="brand-mark">LIREATE</div>
  </div>
</div>
</body></html>""".format(
        shared=shared_styles(),
        w=width,
        h=height,
        sw=sheet_w,
        sh=sheet_h,
        hl_px=hl_px,
        headline=_headline_html(lines, highlight),
        arrow=arrow_svg,
        badge=_esc(badge),
        sticky=_sticky_html(
            spec.get("sticky_text") or "",
            spec.get("sticky_underline") or "",
            sticky_bg,
        ),
        labels=labels_html,
        ui_title=_esc(ui_title),
        ui_rows=ui_rows_html,
    )
