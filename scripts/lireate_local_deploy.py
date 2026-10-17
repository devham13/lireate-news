"""Copy publish-bundle images into site docroot (hosting, no FTP)."""

import shutil
from pathlib import Path


def copy_bundle_images(docroot, bundle_images, remote_dir="template/images/blog"):
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
