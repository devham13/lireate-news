"""Image paths and deploy for Lireate hosting (docroot /images/ + template/blog)."""

import shutil
from pathlib import Path

# local path under article_dir -> filename suffix under /images/{seo_url}...
_HOSTING_INLINE_FILES = (
    ("cover/inline-01.png", "_inline_01.jpg"),
    ("cover/inline-02.png", "_inline_02.jpg"),
    ("cover/inline-03.png", "_inline_03.jpg"),
)

COVER_SOURCE = "cover/cover.png"
BLOG_COVER_SIZE = (860, 400)
BLOG_SMALL_SIZE = (350, 163)


def _cover_basename(seo_url):
    return "{0}.jpg".format(seo_url)


def _assert_owned_dest(dest, seo_url):
    """Only write files whose basename matches this news seo_url."""
    expected = _cover_basename(seo_url)
    if dest.name != expected:
        raise ValueError("refuse to write {0} (expected basename {1})".format(dest, expected))


def template_blog_paths(docroot, seo_url):
    docroot = Path(docroot)
    base = docroot / "template" / "images" / "blog"
    return base / _cover_basename(seo_url), base / "small" / _cover_basename(seo_url)


def docroot_images_cover_path(docroot, seo_url):
    return Path(docroot) / "images" / _cover_basename(seo_url)


def build_hosting_image_map(seo_url, article_dir):
    article_dir = Path(article_dir)
    mapping = {}
    if (article_dir / COVER_SOURCE).is_file():
        mapping[COVER_SOURCE] = "/template/images/blog/{0}".format(_cover_basename(seo_url))
    for local_rel, suffix in _HOSTING_INLINE_FILES:
        if (article_dir / local_rel).is_file():
            fname = "{0}{1}".format(seo_url, suffix)
            mapping[local_rel] = "/images/{0}".format(fname)
    return mapping


def transform_html_paths(html, image_map):
    out = html or ""
    for local, web_path in image_map.items():
        out = out.replace('src="{0}"'.format(local), 'src="{0}"'.format(web_path))
        out = out.replace("src='{0}'".format(local), "src='{0}'".format(web_path))
    return out


def list_planned_image_destinations(docroot, seo_url, article_dir):
    docroot = Path(docroot)
    article_dir = Path(article_dir)
    paths = []
    if (article_dir / COVER_SOURCE).is_file():
        paths.append(str(docroot_images_cover_path(docroot, seo_url)))
        large, small = template_blog_paths(docroot, seo_url)
        paths.append(str(large))
        paths.append(str(small))
    for local_rel, suffix in _HOSTING_INLINE_FILES:
        if (article_dir / local_rel).is_file():
            paths.append(str(docroot / "images" / "{0}{1}".format(seo_url, suffix)))
    return paths


def _pil_image():
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        return None
    return Image


def _center_crop_resize(im, target_w, target_h, resample):
    w, h = im.size
    if w <= 0 or h <= 0:
        raise ValueError("invalid image size")
    target_aspect = float(target_w) / float(target_h)
    src_aspect = float(w) / float(h)
    if src_aspect > target_aspect:
        new_w = int(round(h * target_aspect))
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        new_h = int(round(w / target_aspect))
        top = (h - new_h) // 2
        box = (0, top, w, top + new_h)
    cropped = im.crop(box)
    try:
        resample_lanczos = resample.LANCZOS
    except AttributeError:
        resample_lanczos = resample.ANTIALIAS  # Pillow < 10
    return cropped.resize((target_w, target_h), resample_lanczos)


def _save_jpeg_variants(src_path, destinations, sizes):
    Image = _pil_image()
    if Image is None:
        for dest in destinations:
            _assert_owned_dest(dest, dest.stem)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest)
        return "copy_fallback_no_pillow"

    im = Image.open(src_path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif im.mode != "RGB":
        im = im.convert("RGB")

    resample = Image
    for dest, size in zip(destinations, sizes):
        _assert_owned_dest(dest, dest.stem)
        dest.parent.mkdir(parents=True, exist_ok=True)
        variant = _center_crop_resize(im, size[0], size[1], resample)
        variant.save(str(dest), format="JPEG", quality=88, optimize=True)
    return "jpeg_pillow"


def deploy_hosting_images(docroot, seo_url, article_dir):
    docroot = Path(docroot)
    article_dir = Path(article_dir)
    cover_src = article_dir / COVER_SOURCE
    if not cover_src.is_file():
        return False, [], "missing {0}".format(COVER_SOURCE)

    copied = []
    detail_parts = []

    images_cover = docroot_images_cover_path(docroot, seo_url)
    large, small = template_blog_paths(docroot, seo_url)
    try:
        mode = _save_jpeg_variants(
            cover_src,
            [images_cover, large, small],
            [BLOG_COVER_SIZE, BLOG_COVER_SIZE, BLOG_SMALL_SIZE],
        )
        detail_parts.append("cover:{0}".format(mode))
        copied.extend([str(images_cover), str(large), str(small)])
    except OSError as e:
        return False, copied, "cover deploy failed: {0}".format(e)
    except ValueError as e:
        return False, copied, str(e)

    dest_dir = docroot / "images"
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return False, copied, "mkdir {0}: {1}".format(dest_dir, e)

    for local_rel, suffix in _HOSTING_INLINE_FILES:
        src = article_dir / local_rel
        if not src.is_file():
            continue
        dest = dest_dir / "{0}{1}".format(seo_url, suffix)
        if not dest.name.startswith(seo_url):
            return False, copied, "refuse inline dest {0}".format(dest.name)
        shutil.copy2(src, dest)
        copied.append(str(dest))

    if len(copied) < 3:
        return False, copied, "cover files missing after deploy"
    return True, copied, "; ".join(detail_parts)
