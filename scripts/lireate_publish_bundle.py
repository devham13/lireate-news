"""Build publish-bundle/ from article dir (stdlib, shared by cloud + hosting)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


def build_image_map(article_dir: Path, slug: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    base = f"/template/images/blog/l01_{slug.replace('-', '_')}"
    files = [
        ("cover/cover.png", f"{base}_cover.png"),
        ("cover/inline-01.png", f"{base}_inline_01.png"),
        ("cover/inline-02.png", f"{base}_inline_02.png"),
        ("cover/inline-03.png", f"{base}_inline_03.png"),
    ]
    for rel, remote in files:
        local_path = article_dir / rel
        if local_path.is_file():
            mapping[rel] = remote
    return mapping


def transform_html(html: str, image_map: dict[str, str]) -> str:
    out = html
    for local, remote in image_map.items():
        out = out.replace(f'src="{local}"', f'src="{remote}"')
        out = out.replace(f"src='{local}'", f"src='{remote}'")
    return out


def build_publish_bundle(article_dir: Path, meta: dict[str, Any], html: str) -> tuple[Path, dict[str, str], str]:
    slug = meta.get("slug") or article_dir.name.split("-", 1)[-1]
    image_map = build_image_map(article_dir, slug)
    transformed = transform_html(html, image_map)

    bundle = article_dir / "publish-bundle"
    if bundle.exists():
        shutil.rmtree(bundle)
    bundle.mkdir(parents=True)
    (bundle / "article-body.html").write_text(transformed, encoding="utf-8")
    (bundle / "publish-meta.json").write_text(
        json.dumps(
            {
                "topic_id": meta.get("topic_id"),
                "slug": slug,
                "canonical_path": meta.get("canonical_path") or f"/{slug}",
                "lireate_category_id": meta.get("lireate_category_id", 9),
                "lireate_category_name": meta.get("lireate_category_name", "Товарный знак"),
                "title": meta.get("title"),
                "description": meta.get("description"),
                "image_map": image_map,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    img_dest = bundle / "images"
    img_dest.mkdir()
    for local_rel, remote_path in image_map.items():
        src = article_dir / local_rel
        dest_name = Path(remote_path).name
        shutil.copy2(src, img_dest / dest_name)

    schema_src = article_dir / "schema.jsonld"
    if schema_src.is_file():
        shutil.copy2(schema_src, bundle / "schema.jsonld")

    return bundle, image_map, transformed
