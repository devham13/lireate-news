"""Copy publish-bundle images into site docroot (hosting, no FTP)."""

from __future__ import annotations

import shutil
from pathlib import Path


def copy_bundle_images(
    docroot: Path,
    bundle_images: Path,
    remote_dir: str = "template/images/blog",
) -> tuple[bool, list[str], str]:
    dest_root = docroot / remote_dir.strip("/")
    try:
        dest_root.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return False, [], f"mkdir {dest_root}: {e}"

    copied: list[str] = []
    if not bundle_images.is_dir():
        return False, [], f"missing bundle images dir: {bundle_images}"

    for path in sorted(bundle_images.glob("*")):
        if not path.is_file():
            continue
        target = dest_root / path.name
        shutil.copy2(path, target)
        copied.append(path.name)
    return True, copied, "ok"
