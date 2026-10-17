"""Image paths and deploy for Lireate hosting (/images/ in docroot)."""

import shutil
from pathlib import Path

# local path under article_dir -> filename suffix under /images/{seo_url}...
_HOSTING_FILES = (
    ("cover/cover.png", ".jpg"),
    ("cover/inline-01.png", "_inline_01.jpg"),
    ("cover/inline-02.png", "_inline_02.jpg"),
    ("cover/inline-03.png", "_inline_03.jpg"),
)


def build_hosting_image_map(seo_url, article_dir):
    article_dir = Path(article_dir)
    mapping = {}
    for local_rel, suffix in _HOSTING_FILES:
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


def deploy_hosting_images(docroot, seo_url, article_dir):
    docroot = Path(docroot)
    article_dir = Path(article_dir)
    dest_dir = docroot / "images"
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return False, [], "mkdir {0}: {1}".format(dest_dir, e)

    copied = []
    for local_rel, suffix in _HOSTING_FILES:
        src = article_dir / local_rel
        if not src.is_file():
            continue
        dest = dest_dir / "{0}{1}".format(seo_url, suffix)
        shutil.copy2(src, dest)
        copied.append(str(dest))
    if not copied:
        return False, [], "no image files in article cover/"
    return True, copied, "ok"
