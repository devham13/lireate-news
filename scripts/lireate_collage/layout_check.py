"""Playwright layout QA: overlaps, density, font/icon sizes."""

FORBIDDEN_OVERLAPS = (
    ("slot-headline", "slot-sticky"),
    ("slot-headline", "slot-badge"),
    ("slot-badge", "slot-sticky"),
)

MIN_GAP = 4
MIN_FONT_LOGICAL = 18
MIN_FONT_COVER_UI = 17
MAX_ICON_LOGICAL = 64
MIN_QUADRANT_INK = 0.12
MIN_CONTENT_COVERAGE = 0.85


def _rect_intersects(a, b, margin=MIN_GAP):
    return not (
        a["x"] + a["width"] + margin <= b["x"]
        or b["x"] + b["width"] + margin <= a["x"]
        or a["y"] + a["height"] + margin <= b["y"]
        or b["y"] + b["height"] + margin <= a["y"]
    )


def collect_slot_boxes(page):
    boxes = {}
    for el in page.query_selector_all("[data-layout-slot]"):
        slot = el.get_attribute("data-layout-slot")
        if not slot:
            continue
        box = el.bounding_box()
        if not box or box["width"] < 2 or box["height"] < 2:
            boxes[slot] = None
            continue
        boxes[slot] = box
    return boxes


def check_overlaps(boxes):
    errors = []
    for slot, box in boxes.items():
        if box is None:
            errors.append("missing or zero-size slot: {0}".format(slot))
    for a, b in FORBIDDEN_OVERLAPS:
        ba, bb = boxes.get(a), boxes.get(b)
        if ba and bb and _rect_intersects(ba, bb):
            errors.append("overlap {0} x {1}".format(a, b))
    return errors


def check_fonts_and_icons(page):
    data = page.evaluate(
        """() => {
      const errors = [];
      const walk = (el) => {
        if (!el || el.nodeType !== 1) return;
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden') return;
        const fs = parseFloat(style.fontSize);
        const tag = el.tagName;
        const text = (el.innerText || '').trim();
        if (text.length <= 2 && /^[✕✓✔]$/.test(text)) return;
        const minFs = el.closest('.slot-ui') ? 17 : 18;
        if (text && el.children.length === 0 && fs > 0 && fs < minFs) {
          if (!el.closest('.muted') && !el.closest('.brand-mark') && !el.closest('.ui-foot')) {
            errors.push('font-small:' + fs.toFixed(1) + 'px:' + text.slice(0,24));
          }
        }
        if (tag === 'SVG' || tag === 'svg') {
          if (el.closest('.cover-arrow, .conc-arrow, .slot-arrow')) return;
          const r = el.getBoundingClientRect();
          if (r.width > 64 || r.height > 64) {
            errors.push('icon-large:' + r.width.toFixed(0) + 'x' + r.height.toFixed(0));
          }
        }
        for (const c of el.children) walk(c);
      };
      walk(document.body);
      return errors;
    }"""
    )
    return data or []


def check_content_coverage(page):
    return page.evaluate(
        """() => {
      const paper = document.querySelector('[data-layout-paper]');
      if (!paper) return { error: 'no paper' };
      const pr = paper.getBoundingClientRect();
      const comp = document.getElementById('composition');
      const slots = comp ? [comp] : Array.from(document.querySelectorAll('[data-layout-slot]'));
      if (!slots.length) return { error: 'no slots' };
      let minX = 1e9, minY = 1e9, maxX = 0, maxY = 0;
      for (const el of slots) {
        const b = el.getBoundingClientRect();
        minX = Math.min(minX, b.left);
        minY = Math.min(minY, b.top);
        maxX = Math.max(maxX, b.right);
        maxY = Math.max(maxY, b.bottom);
      }
      const cw = maxX - minX, ch = maxY - minY;
      const wr = cw / pr.width, hr = ch / pr.height;
      return { wr, hr, minX, minY, maxX, maxY, pr };
    }"""
    )


def check_quadrant_slots(page):
    return page.evaluate(
        """() => {
      const paper = document.querySelector('[data-layout-paper]');
      if (!paper) return [];
      const pr = paper.getBoundingClientRect();
      const quads = [
        { x: pr.left, y: pr.top, w: pr.width / 2, h: pr.height / 2 },
        { x: pr.left + pr.width / 2, y: pr.top, w: pr.width / 2, h: pr.height / 2 },
        { x: pr.left, y: pr.top + pr.height / 2, w: pr.width / 2, h: pr.height / 2 },
        { x: pr.left + pr.width / 2, y: pr.top + pr.height / 2, w: pr.width / 2, h: pr.height / 2 },
      ];
      const slots = Array.from(document.querySelectorAll('[data-layout-slot]'));
      const errors = [];
      quads.forEach((q, i) => {
        let area = 0;
        slots.forEach((el) => {
          const b = el.getBoundingClientRect();
          const ix = Math.max(0, Math.min(b.right, q.x + q.w) - Math.max(b.left, q.x));
          const iy = Math.max(0, Math.min(b.bottom, q.y + q.h) - Math.max(b.top, q.y));
          area = Math.max(area, ix * iy);
        });
        if (area < 900) errors.push('quadrant ' + (i + 1) + ' no content slot');
      });
      return errors;
    }"""
    )


def check_quadrant_ink(png_path, paper_rect, dpr=2):
    """PIL: fraction of non-paper-white pixels per paper quadrant."""
    from PIL import Image

    im = Image.open(png_path).convert("RGB")
    w, h = im.size
    px = int(paper_rect["x"] * dpr)
    py = int(paper_rect["y"] * dpr)
    pw = int(paper_rect["width"] * dpr)
    ph = int(paper_rect["height"] * dpr)
    px = max(0, min(px, w - 1))
    py = max(0, min(py, h - 1))
    pw = max(1, min(pw, w - px))
    ph = max(1, min(ph, h - py))
    crop = im.crop((px, py, px + pw, py + ph))
    cw, ch = crop.size
    mids = (cw // 2, ch // 2)

    def ink_ratio(region):
        ink = 0
        total = region.size[0] * region.size[1]
        for r, g, b in region.getdata():
            if r < 235 or g < 235 or b < 235:
                ink += 1
        return ink / float(total) if total else 0

    quads = [
        crop.crop((0, 0, mids[0], mids[1])),
        crop.crop((mids[0], 0, cw, mids[1])),
        crop.crop((0, mids[1], mids[0], ch)),
        crop.crop((mids[0], mids[1], cw, ch)),
    ]
    return [ink_ratio(q) for q in quads]


def check_layout_slots(page):
    return check_overlaps(collect_slot_boxes(page))


def assert_layout_ok(page, png_path=None, dpr=2, check_density=True):
    errors = list(check_layout_slots(page))
    errors.extend(check_fonts_and_icons(page))

    cov = check_content_coverage(page)
    if cov.get("error"):
        errors.append(cov["error"])
    else:
        if cov["wr"] < MIN_CONTENT_COVERAGE or cov["hr"] < MIN_CONTENT_COVERAGE:
            errors.append(
                "content coverage low: {0:.0%} x {1:.0%}".format(cov["wr"], cov["hr"])
            )

    if check_density:
        if page.query_selector("#composition"):
            errors.extend(check_quadrant_slots(page))
        elif png_path:
            paper = page.query_selector("[data-layout-paper]")
            if paper:
                rect = paper.bounding_box()
                if rect:
                    ratios = check_quadrant_ink(png_path, rect, dpr=dpr)
                    for i, r in enumerate(ratios):
                        if r < MIN_QUADRANT_INK:
                            errors.append(
                                "quadrant {0} ink {1:.0%} < {2:.0%}".format(
                                    i + 1, r, MIN_QUADRANT_INK
                                )
                            )

    badge = page.query_selector('[data-layout-slot="slot-badge"]')
    if badge:
        text = (badge.inner_text() or "").strip()
        box = badge.bounding_box()
        if text and box and box["width"] < len(text) * 7:
            errors.append("badge clipped")

    if errors:
        raise RuntimeError("LAYOUT_BLOCKER: " + "; ".join(errors[:12]))
