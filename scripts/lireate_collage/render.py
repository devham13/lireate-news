from pathlib import Path

from .fit_composition import FIT_COMPOSITION_JS
from .layout_check import assert_layout_ok

DEVICE_SCALE = 2


def render_html_to_png(html, width, height, out_path, device_scale_factor=None, layout_check=True, fit=False):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("playwright not installed; pip install playwright && playwright install chromium")

    dsf = device_scale_factor if device_scale_factor is not None else DEVICE_SCALE
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=dsf,
        )
        page.set_content(html, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(300)
        if fit:
            page.evaluate(FIT_COMPOSITION_JS)
            page.wait_for_timeout(200)
        tmp = out_path.with_suffix(".layout.png")
        page.screenshot(path=str(tmp), clip={"x": 0, "y": 0, "width": width, "height": height})
        if layout_check:
            assert_layout_ok(page, png_path=str(tmp), dpr=dsf, check_density=True)
        tmp.replace(out_path)
        browser.close()
    return out_path


def resize_png(src, dest, size):
    from PIL import Image

    im = Image.open(src).convert("RGB")
    if im.size != size:
        im = im.resize(size, Image.Resampling.LANCZOS)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, format="PNG", optimize=True)
