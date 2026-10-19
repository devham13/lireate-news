from .constants import GOOGLE_FONTS, INK, NAVY, PAPER, PINK, PINK_ALT, STICKY_PINK, STICKY_YELLOW


def shared_styles():
    return """
@import url('{fonts}');
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; background: {navy}; font-family: 'Inter', system-ui, sans-serif; color: {ink}; }}
.hand {{ font-family: 'Caveat', cursive; }}
.pink {{ color: {pink}; }}
.pink-bg {{ background: {pink}; color: #fff; }}
.paper {{
  position: relative;
  background: {paper};
  box-shadow: 0 12px 40px rgba(0,0,0,.35);
}}
.paper-torn {{
  clip-path: polygon(
    0% 2%, 3% 0%, 8% 1%, 14% 0%, 22% 2%, 30% 0%, 38% 1%, 46% 0%, 54% 2%, 62% 0%, 70% 1%, 78% 0%, 86% 2%, 94% 0%, 100% 1%,
    100% 98%, 97% 100%, 90% 99%, 82% 100%, 74% 98%, 66% 100%, 58% 99%, 50% 100%, 42% 98%, 34% 100%, 26% 99%, 18% 100%, 10% 98%, 2% 100%, 0% 99%
  );
}}
.tape {{
  position: absolute;
  width: 72px; height: 28px;
  background: linear-gradient(135deg, rgba(30,30,30,.92), rgba(10,10,10,.88));
  opacity: .85;
  transform: rotate(-35deg);
  border-radius: 2px;
}}
.tape-tr {{ top: -6px; right: 48px; transform: rotate(25deg); }}
.tape-tl {{ top: -4px; left: 40px; }}
.tape-br {{ bottom: 12px; right: 24px; transform: rotate(-15deg); width: 64px; }}
.tape-bl {{ bottom: 8px; left: 20px; transform: rotate(12deg); width: 58px; }}
.chip {{
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px; border-radius: 999px;
  border: 1px solid #e5e7eb; background: #fff;
  font-size: 13px; font-weight: 600; white-space: nowrap;
}}
.chip svg {{ width: 14px; height: 14px; flex-shrink: 0; }}
.sticky {{
  position: absolute;
  padding: 14px 16px;
  box-shadow: 2px 4px 12px rgba(0,0,0,.2);
  font-size: 22px; line-height: 1.15;
  transform: rotate(4deg);
  max-width: 200px;
}}
.sticky-tape {{
  position: absolute; top: -10px; left: 50%; margin-left: -28px;
  width: 56px; height: 18px;
  background: rgba(245,230,200,.75);
  transform: rotate(-2deg);
}}
.torn-chip {{
  display: inline-block;
  padding: 6px 14px;
  font-size: 12px; font-weight: 700;
  transform: rotate(-3deg);
  clip-path: polygon(2% 15%, 0% 45%, 3% 85%, 8% 100%, 92% 98%, 100% 70%, 97% 25%, 90% 0%, 12% 2%);
}}
.torn-chip.black {{ background: #111; color: #fff; }}
.torn-chip.white {{ background: #fff; color: #111; border: 1px solid #ddd; }}
.torn-chip.pink {{ background: {pink}; color: #fff; }}
.conclusion-wrap {{ display: flex; align-items: center; gap: 12px; margin-top: 16px; }}
.conclusion-label {{
  font-family: 'Caveat', cursive;
  font-size: 26px; padding: 4px 10px;
  background: #fff;
  clip-path: polygon(0 20%, 5% 0, 95% 5%, 100% 30%, 98% 100%, 10% 95%, 0 70%);
}}
.conclusion-arrow {{
  width: 48px; height: 24px;
  border: none; background: transparent;
}}
.conclusion-box {{
  border: 3px solid #111;
  padding: 10px 18px;
  font-weight: 800;
  font-size: 22px;
  line-height: 1.1;
  background: #fff;
}}
.marker-under {{
  background: linear-gradient(transparent 60%, rgba(239,68,68,.45) 60%);
}}
.brand {{
  position: absolute; bottom: 10px; left: 16px;
  font-size: 10px; letter-spacing: .12em; color: #94a3b8; font-weight: 600;
}}
""".format(
        fonts=GOOGLE_FONTS,
        navy=NAVY,
        ink=INK,
        paper=PAPER,
        pink=PINK,
    )


def icon_svg(name):
    paths = {
        "tag": '<path d="M4 4h6l10 10-6 6L4 10V4z" stroke="currentColor" fill="none" stroke-width="1.5"/>',
        "calendar": '<rect x="3" y="5" width="14" height="12" rx="1" stroke="currentColor" fill="none" stroke-width="1.5"/><path d="M3 9h14M7 3v4M11 3v4" stroke="currentColor" stroke-width="1.5"/>',
        "clock": '<circle cx="10" cy="10" r="7" stroke="currentColor" fill="none" stroke-width="1.5"/><path d="M10 6v5l3 2" stroke="currentColor" stroke-width="1.5"/>',
        "globe": '<circle cx="10" cy="10" r="7" stroke="currentColor" fill="none" stroke-width="1.5"/><path d="M3 10h14M10 3c2 2.5 2 11.5 0 14M10 3c-2 2.5-2 11.5 0 14" stroke="currentColor" stroke-width="1.2"/>',
        "layers": '<path d="M2 8l8-4 8 4-8 4-8-4zm0 5l8 4 8-4" stroke="currentColor" fill="none" stroke-width="1.5"/>',
        "warning": '<path d="M10 3l8 14H2L10 3zm0 4v4m0 3h.01" stroke="currentColor" fill="none" stroke-width="1.5"/>',
        "shield": '<path d="M10 2l7 3v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V5l7-3z" stroke="currentColor" fill="none" stroke-width="1.5"/>',
        "doc": '<path d="M6 2h8l4 4v12H6V2z" stroke="currentColor" fill="none" stroke-width="1.5"/><path d="M14 2v4h4" stroke="currentColor" stroke-width="1.5"/>',
        "check": '<path d="M4 10l4 4 8-8" stroke="currentColor" fill="none" stroke-width="2"/>',
        "person": '<circle cx="10" cy="7" r="3" stroke="currentColor" fill="none" stroke-width="1.5"/><path d="M4 18c0-3 2.5-5 6-5s6 2 6 5" stroke="currentColor" fill="none" stroke-width="1.5"/>',
    }
    inner = paths.get(name, paths["doc"])
    return '<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">{0}</svg>'.format(inner)


def chip_html(chip):
    icon = chip.get("icon") or "tag"
    text = chip.get("text") or ""
    return '<span class="chip">{svg}<span>{text}</span></span>'.format(
        svg=icon_svg(icon), text=_esc(text)
    )


def _esc(s):
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def conclusion_html(conc):
    label = conc.get("label") or "итог"
    lines = conc.get("box_lines") or []
    highlight = conc.get("highlight_word") or ""
    chip = conc.get("chip") or ""
    marker = conc.get("marker_underline", False)
    parts = []
    for line in lines:
        if highlight and highlight in line:
            before, after = line.split(highlight, 1)
            span = '<span class="pink">{0}</span>'.format(_esc(highlight))
            if marker:
                span = '<span class="marker-under">{0}</span>'.format(span)
            parts.append(_esc(before) + span + _esc(after))
        else:
            parts.append(_esc(line))
    box_inner = "<br/>".join(parts)
    chip_html_s = ""
    if chip:
        chip_html_s = (
            '<div style="margin-top:8px"><span class="torn-chip black" '
            'style="transform:rotate(-4deg)">{0}</span></div>'.format(_esc(chip))
        )
    arrow_svg = (
        '<svg class="conclusion-arrow" viewBox="0 0 48 24">'
        '<path d="M2 12 C18 4, 28 20, 46 12" stroke="#111" fill="none" stroke-width="2"/>'
        '<path d="M40 8l6 4-6 4" stroke="#111" fill="none" stroke-width="2"/>'
        "</svg>"
    )
    return (
        '<div class="conclusion-wrap">'
        '<span class="conclusion-label">{label}</span>{arrow}'
        '<div><div class="conclusion-box">{box}</div>{chip}</div></div>'
    ).format(label=_esc(label), arrow=arrow_svg, box=box_inner, chip=chip_html_s)
