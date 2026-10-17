#!/usr/bin/env python3
"""Overlay readable Cyrillic text on blog covers (no model-generated microcopy)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Hosting template sizes (must match lireate_hosting_images.py)
BLOG_COVER_SIZE = (860, 400)
BLOG_SMALL_SIZE = (350, 163)


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


def _draw_text_stroke(draw, xy, text, font, fill, stroke=3, stroke_fill=(0, 0, 0)):
    draw.text(xy, text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def _hosting_crop_resize(im, target_w, target_h):
    """Same center crop as lireate_hosting_images._center_crop_resize."""
    from lireate_hosting_images import _center_crop_resize, _pil_image

    Image = _pil_image()
    if Image is None:
        raise RuntimeError("Pillow required")
    return _center_crop_resize(im, target_w, target_h, Image)


def apply_l01_overlays(im):
    from PIL import ImageDraw

    im = im.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size

    title_font = _load_font(max(28, int(h * 0.075)))
    badge_font = _load_font(max(22, int(h * 0.055)))
    label_font = _load_font(max(14, int(h * 0.032)))
    small_font = _load_font(max(12, int(h * 0.026)))

    title = "Знак занят — пошлина сгорела?"
    tw = draw.textlength(title, font=title_font)
    tx = int((w - tw) / 2)
    ty = int(h * 0.04)
    _draw_text_stroke(draw, (tx, ty), title, title_font, fill=(26, 26, 26), stroke=2)

    # Mask any model-generated UI text; draw clean window in code only
    win_x0 = int(w * 0.48)
    win_y0 = int(h * 0.22)
    win_x1 = int(w * 0.92)
    win_y1 = int(h * 0.72)

    draw.rectangle((win_x0, win_y0, win_x1, win_y1), fill=(245, 245, 240), outline=(160, 160, 160), width=2)
    for i in range(4):
        row_y = win_y0 + 52 + i * int((win_y1 - win_y0 - 80) / 4)
        draw.rectangle(
            (win_x0 + 14, row_y, win_x1 - 14, row_y + 18),
            fill=(230, 230, 225),
            outline=(200, 200, 195),
        )
    _draw_text_stroke(
        draw,
        (win_x0 + 12, win_y0 + 8),
        "Реестр Роспатента",
        label_font,
        fill=(40, 40, 40),
        stroke=1,
    )

    badge_text = "98% схожесть"
    bw = draw.textlength(badge_text, font=badge_font)
    bx = win_x0 + int((win_x1 - win_x0 - bw) / 2)
    by = win_y0 + int((win_y1 - win_y0) * 0.38)
    pad = 8
    draw.rectangle(
        (bx - pad, by - pad, bx + bw + pad, by + int(badge_font.size * 1.2) + pad),
        fill=(220, 50, 50),
    )
    draw.text((bx, by), badge_text, font=badge_font, fill=(255, 255, 255))

    sub = "Сходство до степени смешения"
    sw = draw.textlength(sub, font=small_font)
    draw.text(
        (win_x0 + int((win_x1 - win_x0 - sw) / 2), win_y1 - int(h * 0.12)),
        sub,
        font=small_font,
        fill=(60, 60, 60),
    )

    return im.convert("RGB")


def export_hosting_previews(cover_im, artifacts_dir: Path, stem: str):
    from PIL import Image

    im = cover_im if hasattr(cover_im, "size") else Image.open(cover_im).convert("RGB")
    large = im.resize(BLOG_COVER_SIZE, Image.Resampling.LANCZOS)
    small = im.resize(BLOG_SMALL_SIZE, Image.Resampling.LANCZOS)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    large.save(artifacts_dir / "{0}-crop-860x400.jpg".format(stem), quality=90)
    small.save(artifacts_dir / "{0}-crop-350x163.jpg".format(stem), quality=90)


def main():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True, help="Base image without readable text")
    ap.add_argument("--out", type=Path, required=True, help="Final cover.png")
    ap.add_argument("--topic", default="L01", choices=("L01",))
    ap.add_argument("--artifacts-dir", type=Path, default=Path("/opt/cursor/artifacts"))
    ap.add_argument("--artifact-stem", default="l01-cover-final")
    args = ap.parse_args()

    from PIL import Image

    base = Image.open(args.base).convert("RGB")
    # Compose on 16:9, then export cover.png at hosting aspect (860×400) — no vertical crop on deploy
    work = (1200, 675)
    if base.size != work:
        base = base.resize(work, Image.Resampling.LANCZOS)

    if args.topic == "L01":
        composed = apply_l01_overlays(base)
    else:
        print("unknown topic", file=sys.stderr)
        return 2

    final = _hosting_crop_resize(composed, BLOG_COVER_SIZE[0], BLOG_COVER_SIZE[1])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    final.save(args.out, format="PNG", optimize=True)
    export_hosting_previews(final, args.artifacts_dir, args.artifact_stem)
    print("OK out={0}".format(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
