#!/usr/bin/env python3
"""Render demo covers (PIL) for style preview — not committed as article covers."""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SIZE = (860, 400)
HERO_REF = REPO_ROOT / "memory/cover/assets/blog-hero-reference.png"

L03_LINES = ("Бренд на Ozon", "и Wildberries?")
L03_SUB = "Нужен ли товарный знак"


def _ensure_import_overlay():
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import lireate_cover_text_overlay as ov

    return ov


def _hero_crop(im, box_frac):
    from PIL import Image

    w, h = im.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])
    return im.crop((x0, y0, x1, y1))


def render_bold_color_typography(ov):
    from PIL import Image, ImageDraw

    im = Image.new("RGB", SIZE, (88, 28, 135))
    draw = ImageDraw.Draw(im)
    draw.ellipse((620, -40, 920, 260), fill=(124, 58, 237))
    draw.rectangle((0, 320, 860, 400), fill=(30, 27, 75))
    font = ov._load_font(34)
    font_s = ov._load_font(18)
    y = 130
    for line in L03_LINES:
        tw = draw.textlength(line, font=font)
        draw.text(((SIZE[0] - tw) / 2, y), line, font=font, fill=(255, 255, 255))
        y += 40
    sw = draw.textlength(L03_SUB, font=font_s)
    draw.text(((SIZE[0] - sw) / 2, y + 8), L03_SUB, font=font_s, fill=(233, 213, 255))
    return im


def render_isometric_scene(ov):
    from PIL import Image, ImageDraw

    im = Image.new("RGB", SIZE, (224, 242, 254))
    draw = ImageDraw.Draw(im)
    # simple isometric blocks
    for i, color in enumerate([(14, 165, 233), (45, 212, 191), (56, 189, 248)]):
        ox = 80 + i * 140
        draw.polygon(
            [(ox, 280), (ox + 80, 240), (ox + 160, 280), (ox + 80, 320)],
            fill=color,
        )
        draw.rectangle((ox + 40, 180, ox + 120, 240), fill=(248, 250, 252), outline=(100, 116, 139))
    # sidebar caption
    sx0, sy0, sx1, sy1 = 560, 40, 840, 360
    draw.rectangle((sx0, sy0, sx1, sy1), fill=(255, 255, 255), outline=(12, 74, 110), width=2)
    font = ov._load_font(22)
    y = sy0 + 24
    for line in L03_LINES + (L03_SUB,):
        draw.text((sx0 + 16, y), line, font=font, fill=(12, 74, 110))
        y += 32
    return im


def render_dark_cinematic(ov):
    from PIL import Image, ImageDraw

    im = Image.new("RGB", SIZE, (15, 23, 42))
    if HERO_REF.is_file():
        hero = Image.open(HERO_REF).convert("RGB")
        hero = _hero_crop(hero, (0.0, 0.05, 0.55, 0.95))
        hero = hero.resize((480, 400), Image.Resampling.LANCZOS)
        im.paste(hero, (380, 0))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 260, 860, 400), fill=(15, 23, 42, 200))
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((24, 270, 820, 385), fill=(15, 23, 42, 210))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(im)
    font = ov._load_font(28)
    y = 285
    for line in L03_LINES:
        draw.text((40, y), line, font=font, fill=(254, 243, 199))
        y += 34
    draw.text((40, y + 4), L03_SUB, font=ov._load_font(16), fill=(251, 191, 36))
    return im


RENDERERS = {
    "bold_color_typography": render_bold_color_typography,
    "isometric_scene": render_isometric_scene,
    "dark_cinematic_closeup": render_dark_cinematic,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--styles",
        default="bold_color_typography,isometric_scene,dark_cinematic_closeup",
    )
    ap.add_argument("--artifacts-dir", type=Path, default=Path("/opt/cursor/artifacts"))
    ap.add_argument("--stem", default="l03-cover-sample")
    args = ap.parse_args()
    ov = _ensure_import_overlay()
    args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    registry = json.loads(
        (REPO_ROOT / "memory/blog/cover-style-registry.json").read_text(encoding="utf-8")
    )
    by_id = {s["style_id"]: s for s in registry.get("styles") or []}
    for sid in args.styles.split(","):
        sid = sid.strip()
        fn = RENDERERS.get(sid)
        if not fn:
            print("skip unknown sample style", sid)
            continue
        img = fn(ov)
        out = args.artifacts_dir / "{0}-{1}.png".format(args.stem, sid)
        img.save(out, format="PNG", optimize=True)
        name = by_id.get(sid, {}).get("name", sid)
        print("OK", out, name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
