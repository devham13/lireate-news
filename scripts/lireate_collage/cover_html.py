from .base_css import _esc, chip_html, icon_svg, shared_styles


def build_cover_html(spec, width, height):
    lines = spec.get("headline_lines") or []
    highlight = (spec.get("highlight") or "").strip()
    sticky = spec.get("sticky_text") or ""
    sticky_color = spec.get("sticky_color") or "yellow"
    badge = spec.get("badge_label") or "ТЗ"
    chips = spec.get("chips") or []
    label_chips = spec.get("label_chips") or []
    ui_title = spec.get("ui_card_title") or "Настройки"
    ui_rows = spec.get("ui_card_rows") or []
    brand = spec.get("show_brand", True)

    headline_parts = []
    for line in lines:
        if highlight and highlight in line:
            a, b = line.split(highlight, 1)
            headline_parts.append(
                '<div class="hl-line">{0}<span class="hl-accent">{1}</span>{2}</div>'.format(
                    _esc(a), _esc(highlight), _esc(b)
                )
            )
        else:
            headline_parts.append('<div class="hl-line">{0}</div>'.format(_esc(line)))
    headline_html = "\n".join(headline_parts)

    sticky_bg = "#f7e58c" if sticky_color == "yellow" else "#ff8fc8"
    chips_html = " ".join(chip_html(c) for c in chips[:3])
    labels_html = ""
    for i, (text, variant) in enumerate(label_chips[:3]):
        rot = (-6 + i * 5)
        labels_html += (
            '<div class="torn-chip {cls}" style="margin:6px 0;transform:rotate({rot}deg)">{txt}</div>'.format(
                cls=variant, txt=_esc(text), rot=rot
            )
        )

    ui_rows_html = ""
    for row in ui_rows[:4]:
        ui_rows_html += (
            '<div class="ui-row"><span>{label}</span>'
            '<span class="toggle on"></span></div>'.format(label=_esc(row))
        )
    if not ui_rows_html:
        ui_rows_html = (
            '<div class="ui-row"><span>Проверка реестра</span><span class="toggle on"></span></div>'
            '<div class="ui-row"><span>Классы МКТУ</span><span class="toggle on"></span></div>'
            '<div class="ui-row"><span>Отчёт PDF</span><span class="toggle"></span></div>'
        )

    arrow_svg = (
        '<svg class="arrow-sketch" viewBox="0 0 120 60">'
        '<path d="M10 40 Q60 10, 100 35" stroke="#111" fill="none" stroke-width="2.5"/>'
        '<path d="M92 28l10 8-12 2" stroke="#111" fill="none" stroke-width="2"/>'
        "</svg>"
    )

    brand_html = '<div class="brand">LIREATE</div>' if brand else ""

    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{shared}
.stage {{ width: {w}px; height: {h}px; position: relative; display: flex; align-items: center; justify-content: center; }}
.sheet {{
  width: {iw}px; height: {ih}px; position: relative; padding: 36px 40px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 24px;
}}
.hl {{ font-size: 38px; font-weight: 800; line-height: 1.08; letter-spacing: -0.02em; }}
.hl-accent {{ color: #ff1f6b; }}
.hl-line {{ margin-bottom: 4px; }}
.right-col {{ position: relative; min-height: 280px; }}
.badge-box {{
  position: absolute; top: 0; right: 0;
  border: 3px solid #111; padding: 8px 14px; font-weight: 800; font-size: 20px;
}}
.sticky-cover {{ top: 8px; right: 56px; background: {sticky_bg}; z-index: 2; }}
.labels {{ position: absolute; top: 100px; right: 0; text-align: right; }}
.ui-card {{
  position: absolute; bottom: 0; left: 0; right: 0;
  background: #fff; border-radius: 12px; padding: 14px 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,.12); border: 1px solid #e5e7eb;
  font-size: 13px;
}}
.ui-card h4 {{ font-size: 14px; margin-bottom: 10px; font-weight: 700; }}
.ui-row {{ display: flex; justify-content: space-between; align-items: center; margin: 8px 0; }}
.toggle {{
  width: 36px; height: 20px; border-radius: 999px; background: #e5e7eb; position: relative;
}}
.toggle.on {{ background: #ff2d78; }}
.toggle.on::after {{
  content: ''; position: absolute; right: 3px; top: 3px; width: 14px; height: 14px;
  background: #fff; border-radius: 50%;
}}
.arrow-sketch {{ position: absolute; left: -20px; top: 120px; width: 100px; opacity: .9; }}
.chips-row {{ margin-top: 14px; display: flex; flex-wrap: wrap; gap: 8px; }}
</style></head><body>
<div class="stage">
  <div class="paper paper-torn sheet">
    <div class="tape tape-tl"></div><div class="tape tape-tr"></div>
    <div class="tape tape-bl"></div><div class="tape tape-br"></div>
    <div>
      <div class="hl">{headline}</div>
      <div class="chips-row">{chips_row}</div>
      {arrow}
    </div>
    <div class="right-col">
      <div class="badge-box">{badge}</div>
      <div class="sticky hand sticky-cover"><div class="sticky-tape"></div>{sticky}</div>
      <div class="labels">{labels}</div>
      <div class="ui-card">
        <h4>{ui_title}</h4>
        {ui_rows}
        <div style="margin-top:10px;display:flex;gap:12px;justify-content:flex-end;font-size:12px">
          <span style="color:#64748b">Сохранить</span>
          <span style="background:#ff2d78;color:#fff;padding:4px 12px;border-radius:6px;font-weight:600">Применить</span>
        </div>
      </div>
    </div>
    {brand}
  </div>
</div>
</body></html>""".format(
        shared=shared_styles(),
        w=width,
        h=height,
        iw=int(width * 0.94),
        ih=int(height * 0.88),
        headline=headline_html,
        chips_row=chips_html,
        arrow=arrow_svg,
        badge=_esc(badge),
        sticky=_esc(sticky),
        sticky_bg=sticky_bg,
        labels=labels_html,
        ui_title=_esc(ui_title),
        ui_rows=ui_rows_html,
        brand=brand_html,
    )
