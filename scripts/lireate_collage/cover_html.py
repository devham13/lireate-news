from .base_css import _esc, shared_styles
from .inline_tokens import COVER_STICKY_H, COVER_STICKY_TEXT_PX, COVER_STICKY_W
from .thumbnail_safe import thumbnail_safe_rect


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
    rots = (-6, 4, -5)
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

    safe_left, safe_top, safe_w, safe_h = thumbnail_safe_rect((width, height))
    hl_px = max(26, min(46, int(safe_h * 0.10)))

    sticky_w = min(COVER_STICKY_W, int(safe_w * 0.42))
    sticky_h = min(COVER_STICKY_H, int(safe_h * 0.26))
    sticky_text_px = max(18, min(COVER_STICKY_TEXT_PX, 22))

    return """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{shared}
html, body {{ margin:0; width:{w}px; height:{h}px; overflow:hidden; }}
.stage {{ width:{w}px; height:{h}px; background:#0b1020; position:relative; }}
.sheet {{
  width:{w}px; height:{h}px; position:relative; box-sizing:border-box;
  background: transparent;
}}
.board-safe {{
  position:absolute;
  left:{safe_left}px; top:{safe_top}px;
  width:{safe_w}px; height:{safe_h}px;
  box-sizing:border-box;
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap:10px 8px;
  padding:4px 6px;
}}
.col-headline {{
  grid-column:1; grid-row:1 / span 2;
  display:flex; align-items:center; justify-content:center;
  text-align:center; position:relative; min-width:0;
}}
.col-deco {{
  grid-column:2; grid-row:1 / span 2;
  position:relative; min-height:0; min-width:0;
}}
.hl {{
  font-size:{hl_px}px; font-weight:800; line-height:1.06; letter-spacing:-0.03em;
  max-width:100%; overflow:hidden;
}}
.hl-accent {{ color:#ff1f6b; }}
.hl-line {{ margin-bottom:0.06em; word-break:break-word; hyphens:auto; }}
.cover-sticky {{
  position:absolute; top:52px; right:0; width:{sticky_w}px; height:{sticky_h}px;
  padding:8px 10px; box-sizing:border-box; font-size:{sticky_text}px; line-height:1.1;
  transform:rotate(4deg); z-index:4; box-shadow:2px 6px 14px rgba(0,0,0,.18);
  display:flex; align-items:center; justify-content:center; text-align:center;
}}
.cover-sticky .sticky-text {{
  display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden;
}}
.sticky-ul {{ background:linear-gradient(transparent 58%, rgba(239,68,68,.55) 58%); }}
.sticky-tape-beige {{
  position:absolute; top:-10px; left:50%; margin-left:-34px; width:68px; height:18px;
  background:rgba(235,220,185,.88); transform:rotate(-2deg);
}}
.slot-badge {{
  position:absolute; top:0; right:0; border:3px solid #111; padding:6px 12px;
  font-weight:800; font-size:18px; white-space:nowrap; z-index:6; background:#fff;
}}
.slot-chips {{
  position:absolute; top:108px; right:0; width:100%;
  display:flex; flex-direction:column; align-items:flex-end; gap:5px; z-index:6;
  pointer-events:none; max-height:88px; overflow:hidden;
}}
.chip-tilt {{ font-size:18px; padding:5px 10px; transform:rotate(var(--rot)); max-width:100%; overflow:hidden; text-overflow:ellipsis; }}
.slot-ui {{
  position:absolute; bottom:0; right:0; left:0; z-index:5;
  max-height:148px;
  background:#fff; border-radius:10px; padding:8px 10px 8px;
  box-shadow:0 8px 22px rgba(0,0,0,.14); border:1px solid #e5e7eb;
  font-size:17px;
}}
.slot-ui h4 {{ font-size:17px; margin:0 0 6px; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.ui-row {{ display:flex; justify-content:space-between; align-items:center; margin:4px 0; gap:6px; }}
.ui-row span:first-child {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1; min-width:0; }}
.toggle {{ width:32px; height:18px; border-radius:999px; background:#e5e7eb; position:relative; flex-shrink:0; }}
.toggle.on {{ background:#ff2d78; }}
.toggle.on::after {{
  content:''; position:absolute; right:3px; top:3px; width:12px; height:12px; background:#fff; border-radius:50%;
}}
.ui-foot {{ margin-top:6px; display:flex; gap:8px; justify-content:flex-end; font-size:11px; align-items:center; }}
.muted {{ color:#64748b; }}
.apply {{ background:#ff2d78; color:#fff; padding:3px 10px; border-radius:6px; font-weight:600; }}
.paper-torn {{
  clip-path: polygon(
    0% 2%, 3% 0%, 8% 1%, 14% 0%, 22% 2%, 30% 0%, 38% 1%, 46% 0%, 54% 2%, 62% 0%, 70% 1%, 78% 0%, 86% 2%, 94% 0%, 100% 1%,
    100% 98%, 97% 100%, 90% 99%, 82% 100%, 74% 98%, 66% 100%, 58% 99%, 50% 100%, 42% 98%, 34% 100%, 26% 99%, 18% 100%, 10% 98%, 2% 100%, 0% 99%
  );
}}
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
    <div class="board-safe" id="composition" data-thumbnail-safe="1">
      <div class="col-headline">
        <div class="hl" data-layout-slot="slot-headline">{headline}</div>
      </div>
      <div class="col-deco">
        <div class="slot-badge" data-layout-slot="slot-badge">{badge}</div>
        {sticky}
        <div class="slot-chips" data-layout-slot="slot-chips">{labels}</div>
        <div class="slot-ui" data-layout-slot="slot-ui-card">
          <h4>{ui_title}</h4>{ui_rows}
          <div class="ui-foot"><span class="muted">Сохранить</span><span class="apply">Применить</span></div>
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
        safe_left=safe_left,
        safe_top=safe_top,
        safe_w=safe_w,
        safe_h=safe_h,
        hl_px=hl_px,
        sticky_w=sticky_w,
        sticky_h=sticky_h,
        sticky_text=sticky_text_px,
        headline=_headline_html(lines, highlight),
        badge=_esc(badge),
        sticky=_sticky_html(spec.get("sticky_text") or "", spec.get("sticky_underline") or "", sticky_bg),
        labels=labels_html,
        ui_title=_esc(ui_title),
        ui_rows=ui_rows_html,
    )
