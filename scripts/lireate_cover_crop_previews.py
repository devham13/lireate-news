#!/usr/bin/env python3
"""Generate /news-style center-crop previews from cover PNGs (before/after QA)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_collage.thumbnail_safe import crop_simulation_sizes  # noqa: E402
from lireate_hosting_images import _center_crop_resize, _load_rgb  # noqa: E402


def make_previews(src: Path, out_dir: Path, prefix: str = "") -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    im = _load_rgb(src)
    if im is None:
        raise RuntimeError("PIL required for crop previews")
    from PIL import Image

    written = []
    for w, h in crop_simulation_sizes():
        cropped = _center_crop_resize(im, w, h, Image)
        name = "{0}crop-{1}x{2}.png".format(prefix, w, h)
        dest = out_dir / name
        cropped.save(dest, format="PNG", optimize=True)
        written.append(dest)
    return written


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover-png", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--prefix", default="")
    args = ap.parse_args()
    paths = make_previews(args.cover_png.resolve(), args.out_dir.resolve(), args.prefix)
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
