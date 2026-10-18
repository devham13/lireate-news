#!/usr/bin/env python3
"""Overlay readable Cyrillic text on blog covers (no model-generated microcopy)."""

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

BLOG_COVER_SIZE = (860, 400)
BLOG_SMALL_SIZE = (350, 163)
COVER_SMALL_FILENAME = "cover-small.png"
MARGIN_PX = 24
SMALL_MARGIN_PX = 8

L01_TITLE_LINES = ("Знак занят —", "пошлина сгорела?")
L01_TITLE_SHORT = ("Знак занят?",)

L02_TITLE_LINES = ("Претензия по ТЗ?", "30 дней на ответ")
L02_TITLE_SHORT = ("Претензия по ТЗ?",)


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


def _crop_resize_top_left_bias(im, target_w, target_h):
    """Crop to aspect keeping top + left (heroine head on left must stay in frame)."""
    from PIL import Image

    w, h = im.size
    target_aspect = float(target_w) / float(target_h)
    src_aspect = float(w) / float(h)
    if src_aspect > target_aspect:
        new_w = int(round(h * target_aspect))
        left = 0
        box = (left, 0, left + new_w, h)
    else:
        new_h = int(round(w / target_aspect))
        top = 0
        box = (0, top, w, top + new_h)
    cropped = im.crop(box)
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)


def _registry_window_box(w, h, profile="860"):
    """UI overlays only in the right half (PIL text zone)."""
    if profile == "350":
        win_x0 = int(w * 0.55)
        win_y0 = int(h * 0.46)
        win_x1 = w - MARGIN_PX
        win_y1 = int(h * 0.88)
        return win_x0, win_y0, win_x1, win_y1
    win_x0 = int(w * 0.45)
    win_y0 = int(h * 0.30)
    win_x1 = w - MARGIN_PX
    win_y1 = int(h * 0.80)
    return win_x0, win_y0, win_x1, win_y1


def apply_l02_claim_ui(im, profile="860"):
    from PIL import ImageDraw

    im = im.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    win_x0, win_y0, win_x1, win_y1 = _registry_window_box(w, h, profile)

    badge_font = _load_font(max(18, int(h * 0.052)))
    label_font = _load_font(max(13, int(h * 0.030)))
    small_font = _load_font(max(11, int(h * 0.024)))

    draw.rectangle((win_x0, win_y0, win_x1, win_y1), fill=(245, 245, 240), outline=(160, 160, 160), width=2)
    for i in range(4):
        row_y = win_y0 + 48 + i * int((win_y1 - win_y0 - 72) / 4)
        draw.rectangle(
            (win_x0 + 12, row_y, win_x1 - 12, row_y + 16),
            fill=(230, 230, 225),
            outline=(200, 200, 195),
        )
    draw.text((win_x0 + 10, win_y0 + 6), "Досудебная претензия", font=label_font, fill=(40, 40, 40))

    badge_text = "Срок 30 дней"
    bw = draw.textlength(badge_text, font=badge_font)
    bx = win_x0 + int((win_x1 - win_x0 - bw) / 2)
    by = win_y0 + int((win_y1 - win_y0) * 0.36)
    pad = 7
    draw.rectangle(
        (bx - pad, by - pad, bx + bw + pad, by + int(badge_font.size * 1.1) + pad),
        fill=(220, 50, 50),
    )
    draw.text((bx, by), badge_text, font=badge_font, fill=(255, 255, 255))

    sub = "п. 5.1 ст. 1252 ГК РФ"
    sw = draw.textlength(sub, font=small_font)
    draw.text(
        (win_x0 + int((win_x1 - win_x0 - sw) / 2), win_y1 - int(h * 0.10)),
        sub,
        font=small_font,
        fill=(60, 60, 60),
    )

    return im.convert("RGB")


def apply_l01_registry_ui(im, profile="860"):
    from PIL import ImageDraw

    im = im.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    win_x0, win_y0, win_x1, win_y1 = _registry_window_box(w, h, profile)

    badge_font = _load_font(max(18, int(h * 0.052)))
    label_font = _load_font(max(13, int(h * 0.030)))
    small_font = _load_font(max(11, int(h * 0.024)))

    draw.rectangle((win_x0, win_y0, win_x1, win_y1), fill=(245, 245, 240), outline=(160, 160, 160), width=2)
    for i in range(4):
        row_y = win_y0 + 48 + i * int((win_y1 - win_y0 - 72) / 4)
        draw.rectangle(
            (win_x0 + 12, row_y, win_x1 - 12, row_y + 16),
            fill=(230, 230, 225),
            outline=(200, 200, 195),
        )
    draw.text((win_x0 + 10, win_y0 + 6), "Реестр Роспатента", font=label_font, fill=(40, 40, 40))

    badge_text = "98% схожесть"
    bw = draw.textlength(badge_text, font=badge_font)
    bx = win_x0 + int((win_x1 - win_x0 - bw) / 2)
    by = win_y0 + int((win_y1 - win_y0) * 0.36)
    pad = 7
    draw.rectangle(
        (bx - pad, by - pad, bx + bw + pad, by + int(badge_font.size * 1.1) + pad),
        fill=(220, 50, 50),
    )
    draw.text((bx, by), badge_text, font=badge_font, fill=(255, 255, 255))

    sub = "Сходство до степени смешения"
    sw = draw.textlength(sub, font=small_font)
    draw.text(
        (win_x0 + int((win_x1 - win_x0 - sw) / 2), win_y1 - int(h * 0.10)),
        sub,
        font=small_font,
        fill=(60, 60, 60),
    )

    return im.convert("RGB")


def _fit_title_font(draw, lines, max_width, start_size, min_size=11):
    for size in range(start_size, min_size - 1, -1):
        font = _load_font(size)
        widths = [draw.textlength(line, font=font) for line in lines]
        if max(widths) <= max_width:
            return font, widths
    font = _load_font(min_size)
    return font, [draw.textlength(line, font=font) for line in lines]


def draw_topic_headline(im, lines, short_lines, profile="860"):
    from PIL import ImageDraw

    im = im.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    win_x0, win_y0, win_x1, _win_y1 = _registry_window_box(w, h, profile)

    if profile == "350":
        plate_x0 = int(w * 0.55)
        plate_x1 = w - MARGIN_PX
        lines_use = short_lines
        max_text_w = plate_x1 - plate_x0 - 6
        start_font = 13
        line_gap = 0
        plate_y0 = MARGIN_PX
        max_plate_bottom = int(h * 0.34)
    else:
        plate_x0 = win_x0
        plate_x1 = win_x1
        lines_use = lines
        max_text_w = plate_x1 - plate_x0 - 12
        start_font = 28
        line_gap = 2
        plate_y0 = MARGIN_PX
        max_plate_bottom = win_y0 - 10

    font, widths = _fit_title_font(draw, lines_use, max_text_w, start_font, min_size=10)
    line_h = int(font.size * 1.12) + line_gap
    block_h = line_h * len(lines_use) + 12
    plate_y1 = min(plate_y0 + block_h, max_plate_bottom)

    draw.rectangle(
        (plate_x0, plate_y0, plate_x1, plate_y1),
        fill=(255, 255, 255, 240),
        outline=(30, 30, 30, 255),
        width=2,
    )

    ty = plate_y0 + 6
    for i, line in enumerate(lines_use):
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

    if profile == "350" and plate_x0 < int(w * 0.50):
        raise ValueError("small title must stay in right half")
    return im.convert("RGB")


def draw_l01_headline(im, profile="860"):
    return draw_topic_headline(im, L01_TITLE_LINES, L01_TITLE_SHORT, profile=profile)


def draw_l02_headline(im, profile="860"):
    return draw_topic_headline(im, L02_TITLE_LINES, L02_TITLE_SHORT, profile=profile)


def build_l02_small_thumb(base_path: Path):
    from PIL import Image, ImageDraw

    base_r = Image.open(base_path).convert("RGB").resize(
        (1290, 600), Image.Resampling.LANCZOS
    )
    bg = _crop_resize_top_left_bias(base_r, BLOG_SMALL_SIZE[0], BLOG_SMALL_SIZE[1])
    im = bg.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    m = SMALL_MARGIN_PX
    col_x0 = int(w * 0.48)
    col_x1 = w - m
    max_w = col_x1 - col_x0 - 4

    title = L02_TITLE_SHORT[0]
    title_font, title_widths = _fit_title_font(draw, (title,), max_w, 15, min_size=9)
    tw = title_widths[0]
    th = int(title_font.size * 1.2) + 8
    plate_y1 = m + th
    draw.rectangle(
        (col_x0, m, col_x1, plate_y1),
        fill=(255, 255, 255, 245),
        outline=(30, 30, 30, 255),
        width=1,
    )
    tx = col_x0 + int((col_x1 - col_x0 - tw) / 2)
    draw.text((tx, m + 4), title, font=title_font, fill=(20, 20, 20))

    badge = "Срок 30 дней"
    badge_font, badge_widths = _fit_title_font(draw, (badge,), max_w - 12, 14, min_size=9)
    bw = badge_widths[0]
    pad = 5
    bh = int(badge_font.size * 1.15) + pad * 2
    by = plate_y1 + m
    if by + bh > int(h * 0.62):
        by = int(h * 0.62) - bh
    bx = col_x0 + int((col_x1 - col_x0 - bw) / 2)
    draw.rectangle(
        (col_x0, by, col_x1, by + bh),
        fill=(220, 50, 50, 255),
    )
    draw.text((bx, by + pad), badge, font=badge_font, fill=(255, 255, 255))

    if col_x1 > w - m or col_x0 < m:
        raise ValueError("small overlays exceed horizontal margins")
    return im.convert("RGB")


def build_l01_small_thumb(base_path: Path):
    """News list thumb: same photo crop, minimal PIL on the right only."""
    from PIL import Image, ImageDraw

    base_r = Image.open(base_path).convert("RGB").resize(
        (1290, 600), Image.Resampling.LANCZOS
    )
    bg = _crop_resize_top_left_bias(base_r, BLOG_SMALL_SIZE[0], BLOG_SMALL_SIZE[1])
    im = bg.convert("RGBA")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    m = SMALL_MARGIN_PX
    col_x0 = int(w * 0.48)
    col_x1 = w - m
    max_w = col_x1 - col_x0 - 4

    title = L01_TITLE_SHORT[0]
    title_font, title_widths = _fit_title_font(draw, (title,), max_w, 15, min_size=9)
    tw = title_widths[0]
    th = int(title_font.size * 1.2) + 8
    plate_y1 = m + th
    draw.rectangle(
        (col_x0, m, col_x1, plate_y1),
        fill=(255, 255, 255, 245),
        outline=(30, 30, 30, 255),
        width=1,
    )
    tx = col_x0 + int((col_x1 - col_x0 - tw) / 2)
    draw.text((tx, m + 4), title, font=title_font, fill=(20, 20, 20))

    badge = "98% схожесть"
    badge_font, badge_widths = _fit_title_font(draw, (badge,), max_w - 12, 14, min_size=9)
    bw = badge_widths[0]
    pad = 5
    bh = int(badge_font.size * 1.15) + pad * 2
    by = plate_y1 + m
    if by + bh > int(h * 0.62):
        by = int(h * 0.62) - bh
    bx = col_x0 + int((col_x1 - col_x0 - bw) / 2)
    draw.rectangle(
        (col_x0, by, col_x1, by + bh),
        fill=(220, 50, 50, 255),
    )
    draw.text((bx, by + pad), badge, font=badge_font, fill=(255, 255, 255))

    if col_x1 > w - m or col_x0 < m:
        raise ValueError("small overlays exceed horizontal margins")
    return im.convert("RGB")


def build_l01_cover_from_base(base_path: Path):
    from PIL import Image

    base = Image.open(base_path).convert("RGB")
    work = (1290, 600)
    base_r = base.resize(work, Image.Resampling.LANCZOS)
    with_ui = apply_l01_registry_ui(base_r, profile="860")
    frame = _crop_resize_top_left_bias(with_ui, BLOG_COVER_SIZE[0], BLOG_COVER_SIZE[1])
    cover = draw_l01_headline(frame, profile="860")
    small = build_l01_small_thumb(base_path)
    return cover, small


def build_l02_cover_from_base(base_path: Path):
    from PIL import Image

    base = Image.open(base_path).convert("RGB")
    work = (1290, 600)
    base_r = base.resize(work, Image.Resampling.LANCZOS)
    with_ui = apply_l02_claim_ui(base_r, profile="860")
    frame = _crop_resize_top_left_bias(with_ui, BLOG_COVER_SIZE[0], BLOG_COVER_SIZE[1])
    cover = draw_l02_headline(frame, profile="860")
    small = build_l02_small_thumb(base_path)
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
    ap.add_argument("--topic", default="L01", choices=("L01", "L02"))
    ap.add_argument("--artifacts-dir", type=Path, default=Path("/opt/cursor/artifacts"))
    ap.add_argument("--artifact-stem", default="l01-cover-final")
    ap.add_argument(
        "--small-only",
        action="store_true",
        help="Regenerate cover-small.png only; do not overwrite cover.png",
    )
    args = ap.parse_args()

    builders = {
        "L01": (build_l01_cover_from_base, build_l01_small_thumb),
        "L02": (build_l02_cover_from_base, build_l02_small_thumb),
    }
    build_cover, build_small = builders[args.topic]

    from PIL import Image

    cover_path = args.out
    small_path = cover_path.parent / COVER_SMALL_FILENAME
    skip_large = args.small_only or os.environ.get("LIREATE_COVER_ONLY_SMALL")
    if skip_large and cover_path.is_file():
        small = build_small(args.base)
        cover = Image.open(cover_path).convert("RGB")
    else:
        cover, small = build_cover(args.base)

    cover_path.parent.mkdir(parents=True, exist_ok=True)
    if not skip_large and not os.environ.get("LIREATE_COVER_SKIP_LARGE"):
        cover.save(cover_path, format="PNG", optimize=True)
    small.save(small_path, format="PNG", optimize=True)
    export_artifacts(cover, small, args.artifacts_dir, args.artifact_stem)
    print("OK out={0} size={1}".format(args.out, cover.size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
