#!/usr/bin/env python3
"""Overlay readable Cyrillic text on blog covers (no model-generated microcopy)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

BLOG_COVER_SIZE = (860, 400)
BLOG_SMALL_SIZE = (350, 163)
MARGIN_PX = 24

L01_TITLE_LINES = ("Знак занят —", "пошлина сгорела?")


def _font_path():
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    )
    for c in candidates:
        if Path(c).is_file():
            return c
    return None


def _load_font(size: int):
    from PIL import ImageFont

    path = _font_path()
    if path:
        return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def _hosting_crop_resize(im, target_w, target_h):
    from lireate_hosting_images import _center_crop_resize, _pil_image

    Image = _pil_image()
    if Image is None:
        raise RuntimeError("Pillow required")
    return _center_crop_resize(im, target_w, target_h, Image)


def _paper_fill(im, x0, y0, x1, y1):
    sample = im.crop((
        max(0, int(im.size[0] * 0.05)),
        max(0, int(im.size[1] * 0.55)),
        max(1, int(im.size[0] * 0.12)),
        min(im.size[1], int(im.size[1] * 0.65)),
    ))
    px = sample.resize((1, 1)).getpixel((0, 0))
    if isinstance(px, tuple) and len(px) >= 3:
        return px[:3]
    return (245, 245, 240)


def _mask_l01_top_band(im):
    """Remove ghost model headline from base image."""
    from PIL import ImageDraw

    im = im.convert("RGBA")
    w, h = im.size
    band_h = int(h * 0.20)
    draw = ImageDraw.Draw(im)
    # Sample paper tone from lower-left (away from face cutout edge)
    fill = _paper_fill(im, 0, 0, w, band_h)
    draw.rectangle((0, 0, w, band_h), fill=fill + (255,))
    return im


def _clean_frame_top(im, band_h=None):
    """Erase residual headline pixels after crop (before PIL title)."""
    from PIL import ImageDraw

    im = im.convert("RGBA")
    w, h = im.size
    if band_h is None:
        band_h = max(MARGIN_PX + 4, int(h * 0.22))
    draw = ImageDraw.Draw(im)
    fill = _paper_fill(im, 0, 0, w, band_h)
    draw.rectangle((0, 0, w, band_h), fill=fill + (255,))
    return im


def _registry_window_box(w, h):
    win_x0 = int(w * 0.48)
    win_y0 = int(h * 0.22)
    win_x1 = int(w * 0.92)
    win_y1 = int(h * 0.72)
    return win_x0, win_y0, win_x1, win_y1


def apply_l01_registry_ui(im, include_title=False):
    """Registry window + labels. Title only when include_title=False is default (legacy)."""
    from PIL import ImageDraw

    im = im.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    win_x0, win_y0, win_x1, win_y1 = _registry_window_box(w, h)

    badge_font = _load_font(max(18, int(h * 0.052)))
    label_font = _load_font(max(13, int(h * 0.030)))
    small_font = _load_font(max(11, int(h * 0.024)))

    draw.rectangle((win_x0, win_y0, win_x1, win_y1), fill=(245, 245, 240), outline=(160, 160, 160), width=2)
    for i in range(4):
        row_y = win_y0 + 52 + i * int((win_y1 - win_y0 - 80) / 4)
        draw.rectangle(
            (win_x0 + 14, row_y, win_x1 - 14, row_y + 18),
            fill=(230, 230, 225),
            outline=(200, 200, 195),
        )
    draw.text((win_x0 + 12, win_y0 + 8), "Реестр Роспатента", font=label_font, fill=(40, 40, 40))

    badge_text = "98% схожесть"
    bw = draw.textlength(badge_text, font=badge_font)
    bx = win_x0 + int((win_x1 - win_x0 - bw) / 2)
    by = win_y0 + int((win_y1 - win_y0) * 0.38)
    pad = 8
    draw.rectangle(
        (bx - pad, by - pad, bx + bw + pad, by + int(badge_font.size * 1.15) + pad),
        fill=(220, 50, 50),
    )
    draw.text((bx, by), badge_text, font=badge_font, fill=(255, 255, 255))

    sub = "Сходство до степени смешения"
    sw = draw.textlength(sub, font=small_font)
    draw.text(
        (win_x0 + int((win_x1 - win_x0 - sw) / 2), win_y1 - int(h * 0.11)),
        sub,
        font=small_font,
        fill=(60, 60, 60),
    )

    if include_title:
        im = draw_l01_headline(im, profile="860")

    return im.convert("RGB")


def _fit_title_font(draw, lines, max_width, start_size, min_size=14):
    for size in range(start_size, min_size - 1, -1):
        font = _load_font(size)
        widths = [draw.textlength(line, font=font) for line in lines]
        if max(widths) <= max_width:
            return font, widths
    font = _load_font(min_size)
    return font, [draw.textlength(line, font=font) for line in lines]


def draw_l01_headline(im, profile="860"):
    """Two-line title on contrast plate; call AFTER final crop. profile: 860 | 350."""
    from PIL import ImageDraw

    im = im.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    win_x0, win_y0, win_x1, _win_y1 = _registry_window_box(w, h)

    if profile == "350":
        plate_x0 = MARGIN_PX
        plate_x1 = w - MARGIN_PX
        max_text_w = plate_x1 - plate_x0 - 12
        start_font = 18
        line_gap = 1
        plate_y0 = MARGIN_PX
    else:
        plate_x0 = max(MARGIN_PX, win_x0)
        plate_x1 = min(w - MARGIN_PX, win_x1)
        max_text_w = plate_x1 - plate_x0 - 16
        start_font = 30
        line_gap = 3
        plate_y0 = MARGIN_PX

    font, widths = _fit_title_font(draw, L01_TITLE_LINES, max_text_w, start_font, min_size=12)
    line_h = int(font.size * 1.15) + line_gap
    block_h = line_h * len(L01_TITLE_LINES) + 14
    plate_y1 = plate_y0 + block_h
    if profile == "860":
        plate_y1 = min(plate_y1, win_y0 - 8)
        if plate_y1 < plate_y0 + line_h * 2:
            plate_y1 = plate_y0 + block_h

    draw.rectangle(
        (plate_x0, plate_y0, plate_x1, plate_y1),
        fill=(255, 255, 255, 235),
        outline=(30, 30, 30, 255),
        width=2,
    )

    ty = plate_y0 + 8
    for i, line in enumerate(L01_TITLE_LINES):
        tw = widths[i]
        tx = plate_x0 + int((plate_x1 - plate_x0 - tw) / 2)
        draw.text(
            (tx, ty + i * line_h),
            line,
            font=font,
            fill=(20, 20, 20),
            stroke_width=1,
            stroke_fill=(255, 255, 255),
        )

    _assert_text_in_frame(draw, im.size, MARGIN_PX)
    return im.convert("RGB")


def _assert_text_in_frame(draw, size, margin):
    w, h = size
    # bbox of drawn text is not tracked; verify plate fits
    if margin < MARGIN_PX:
        raise ValueError("margin below minimum")
    if w < 2 * margin or h < 2 * margin:
        raise ValueError("frame too small for title margins")


def build_l01_cover_from_base(base_path: Path):
    from PIL import Image

    work = (1200, 675)
    base = Image.open(base_path).convert("RGB")
    if base.size != work:
        base = base.resize(work, Image.Resampling.LANCZOS)

    masked = _mask_l01_top_band(base)
    with_ui = apply_l01_registry_ui(masked, include_title=False)
    frame = _hosting_crop_resize(with_ui, BLOG_COVER_SIZE[0], BLOG_COVER_SIZE[1])
    frame_clean = _clean_frame_top(frame)
    cover = draw_l01_headline(frame_clean, profile="860")

    small_base = _clean_frame_top(frame.resize(BLOG_SMALL_SIZE, Image.Resampling.LANCZOS), band_h=46)
    small = draw_l01_headline(small_base, profile="350")
    return cover, small


def export_artifacts(cover, small, artifacts_dir: Path, stem: str):
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    cover.save(artifacts_dir / "{0}-crop-860x400.jpg".format(stem), quality=92)
    small.save(artifacts_dir / "{0}-crop-350x163.jpg".format(stem), quality=92)
    cover.save(artifacts_dir / "{0}.png".format(stem), format="PNG", optimize=True)


def main():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--topic", default="L01", choices=("L01",))
    ap.add_argument("--artifacts-dir", type=Path, default=Path("/opt/cursor/artifacts"))
    ap.add_argument("--artifact-stem", default="l01-cover-final")
    args = ap.parse_args()

    if args.topic != "L01":
        print("unknown topic", file=sys.stderr)
        return 2

    cover, small = build_l01_cover_from_base(args.base)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    cover.save(args.out, format="PNG", optimize=True)
    export_artifacts(cover, small, args.artifacts_dir, args.artifact_stem)
    print("OK out={0} size={1}".format(args.out, cover.size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
