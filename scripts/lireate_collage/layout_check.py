"""Playwright bounding-box overlap checks for collage layouts."""

# Pairs that must not intersect (with margin px)
FORBIDDEN_OVERLAPS = (
    ("slot-headline", "slot-sticky"),
    ("slot-headline", "slot-badge"),
    ("slot-headline", "slot-chips"),
    ("slot-headline", "slot-ui-card"),
    ("slot-badge", "slot-sticky"),
)

# Sticky may overlap chips slightly; badge must clear sticky
MIN_GAP = 6


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


def check_layout_slots(page):
    """Return list of error strings; empty if OK."""
    boxes = collect_slot_boxes(page)
    errors = []
    for slot, box in boxes.items():
        if box is None:
            errors.append("missing or zero-size slot: {0}".format(slot))

    for a, b in FORBIDDEN_OVERLAPS:
        ba, bb = boxes.get(a), boxes.get(b)
        if ba and bb and _rect_intersects(ba, bb):
            errors.append("overlap {0} x {1}".format(a, b))

    # Badge must show full label (min width)
    badge = page.query_selector('[data-layout-slot="slot-badge"]')
    if badge:
        text = (badge.inner_text() or "").strip()
        box = badge.bounding_box()
        if text and box and box["width"] < len(text) * 8:
            errors.append("badge clipped: {0!r} width={1}".format(text, box["width"]))

    sticky = page.query_selector('[data-layout-slot="slot-sticky"]')
    if sticky:
        box = sticky.bounding_box()
        if box and box["height"] < 40:
            errors.append("sticky too small to read")

    return errors


def assert_layout_ok(page):
    errors = check_layout_slots(page)
    if errors:
        raise RuntimeError("LAYOUT_BLOCKER: " + "; ".join(errors))
