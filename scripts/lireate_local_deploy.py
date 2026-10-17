"""Copy article assets into site docroot (hosting, no FTP)."""

import shutil
from pathlib import Path


def copy_cover_image(docroot, seo_url, cover_source):
    docroot = Path(docroot)
    cover_source = Path(cover_source)
    dest_dir = docroot / "images"
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return False, "", "mkdir {0}: {1}".format(dest_dir, e)
    if not cover_source.is_file():
        return False, "", "missing cover: {0}".format(cover_source)
    dest = dest_dir / "{0}.jpg".format(seo_url)
    shutil.copy2(cover_source, dest)
    return True, str(dest), "ok"


def copy_bundle_images(docroot, bundle_images, remote_dir="template/images/blog"):
    """Legacy path for inline blog images (optional)."""
    docroot = Path(docroot)
    bundle_images = Path(bundle_images)
    dest_root = docroot / remote_dir.strip("/")
    try:
        dest_root.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return False, [], "mkdir {0}: {1}".format(dest_root, e)

    copied = []
    if not bundle_images.is_dir():
        return False, [], "missing bundle images dir: {0}".format(bundle_images)

    for path in sorted(bundle_images.glob("*")):
        if not path.is_file():
            continue
        target = dest_root / path.name
        shutil.copy2(path, target)
        copied.append(path.name)
    return True, copied, "ok"
