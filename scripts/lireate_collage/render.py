from pathlib import Path


def render_html_to_png(html, width, height, out_path, device_scale_factor=1):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("playwright not installed; pip install playwright && playwright install chromium")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=device_scale_factor,
        )
        page.set_content(html, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(400)
        page.screenshot(path=str(out_path), clip={"x": 0, "y": 0, "width": width, "height": height})
        browser.close()
    return out_path


def resize_png(src, dest, size):
    from PIL import Image

    im = Image.open(src).convert("RGB")
    im = im.resize(size, Image.Resampling.LANCZOS)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, format="PNG", optimize=True)
