"""Center-crop safe rectangle for 860×400 list covers on /news."""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple

# Source cover size (must match constants.COVER_RENDER).
DEFAULT_SRC = (860, 400)

# Typical /news card crops: preview 396×300, small 350×163, plus common object-fit aspects.
DEFAULT_CROP_TARGETS: Tuple[Tuple[int, int], ...] = (
    (396, 300),
    (350, 163),
    (640, 400),  # 16:10 at full height
    (860, 484),  # 16:9 at full width reference
    (860, 645),  # 4:3 at full width reference
    (400, 400),  # square card
)

DEFAULT_CROP_ASPECTS: Tuple[float, ...] = (16 / 10, 16 / 9, 4 / 3, 1.0)


def center_crop_box(
    src_w: int, src_h: int, target_w: int, target_h: int
) -> Tuple[int, int, int, int]:
    """Return (left, top, right, bottom) visible rect after cover-style center crop."""
    target_aspect = float(target_w) / float(target_h)
    src_aspect = float(src_w) / float(src_h)
    if src_aspect > target_aspect:
        new_w = int(round(src_h * target_aspect))
        left = (src_w - new_w) // 2
        return left, 0, left + new_w, src_h
    new_h = int(round(src_w / target_aspect))
    top = (src_h - new_h) // 2
    return 0, top, src_w, top + new_h


def intersect_boxes(
    boxes: Iterable[Tuple[int, int, int, int]],
) -> Tuple[int, int, int, int]:
    left = max(b[0] for b in boxes)
    top = max(b[1] for b in boxes)
    right = min(b[2] for b in boxes)
    bottom = min(b[3] for b in boxes)
    if right <= left or bottom <= top:
        raise ValueError("empty intersection for thumbnail safe zone")
    return left, top, right, bottom


def thumbnail_safe_rect(
    src_size: Sequence[int] = DEFAULT_SRC,
    crop_targets: Sequence[Tuple[int, int]] = DEFAULT_CROP_TARGETS,
    crop_aspects: Sequence[float] = DEFAULT_CROP_ASPECTS,
    padding: int = 16,
) -> Tuple[int, int, int, int]:
    """Inset rect (left, top, width, height) where all text must stay visible."""
    sw, sh = int(src_size[0]), int(src_size[1])
    boxes = [center_crop_box(sw, sh, tw, th) for tw, th in crop_targets]
    for aspect in crop_aspects:
        tw = max(1, int(round(sh * aspect)))
        boxes.append(center_crop_box(sw, sh, tw, sh))
    left, top, right, bottom = intersect_boxes(boxes)
    left += padding
    top += padding
    right -= padding
    bottom -= padding
    w = right - left
    h = bottom - top
    if w < 120 or h < 80:
        raise ValueError("thumbnail safe zone too small after padding")
    return left, top, w, h


def crop_simulation_sizes() -> Tuple[Tuple[int, int], ...]:
    """Output sizes for before/after preview PNGs."""
    return (
        (396, 300),
        (350, 163),
        (640, 360),  # ~16:10 hero
        (480, 270),  # 16:9
        (400, 300),  # 4:3
    )
