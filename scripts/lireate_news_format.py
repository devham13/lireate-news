"""Build news row payload for lireate DB (Py3.6+)."""

from lireate_translit import translit_seo_url, truncate_utf8


def build_cover_paragraph(name, seo_url, lead_style="template"):
    """Lead image prepended to full_story (CMS also shows template/blog cover in imgBlock)."""
    if lead_style in ("none", "off", False):
        return ""
    alt = (name or "").replace('"', "&quot;")
    if lead_style == "float_images":
        return (
            '<p style="text-align: justify;">'
            '<img alt="{0}" src="/images/{1}.jpg" '
            'style="float: right; width: 500px; height: 281px;" />'
            '</p> \r\n'
        ).format(alt, seo_url)
    # Как у существующих новостей на lireate.ru (см. diagnostic full_story_head).
    return (
        '<p style="text-align: justify; background: transparent;">'
        '<img class=\'img-responsive\' alt="{0}" class="img-responsive" '
        'src="/template/images/blog/{1}.jpg" style="width: 838px; height: 400px;" />'
        '</p>\r\n'
    ).format(alt, seo_url)


def build_full_story(name, seo_url, body_html, lead_style="template"):
    body = (body_html or "").strip()
    lead = build_cover_paragraph(name, seo_url, lead_style=lead_style)
    if not lead:
        if body.startswith("<p"):
            return body
        return "<p>" + body + "</p>" if body else ""
    if body.startswith("<p"):
        return lead + body
    return lead + "<p>" + body + "</p>"


def build_news_row(meta, body_html, lead_style="template"):
    name = (meta.get("title") or meta.get("h1") or meta.get("slug") or "").strip()
    seo_url = translit_seo_url(name)
    explicit = (meta.get("lireate_seo_url") or "").strip()
    if explicit:
        seo_url = explicit.strip("/").replace("/", "_")

    keywords = meta.get("keywords") or []
    if isinstance(keywords, list):
        seo_keywords = ", ".join(keywords)
    else:
        seo_keywords = str(keywords)

    description = meta.get("description") or ""
    return {
        "name": name,
        "title": 1,
        "seo_title": meta.get("title") or name,
        "seo_keywords": seo_keywords,
        "seo_description": truncate_utf8(description, 200),
        "seo_url": seo_url,
        "category": int(meta.get("lireate_category_id", 9)),
        "short_story": "",
        "full_story": build_full_story(name, seo_url, body_html, lead_style=lead_style),
        "active": 1,
        "cover_image_basename": "{0}.jpg".format(seo_url),
        "cover_web_path": "/template/images/blog/{0}.jpg".format(seo_url),
        "cover_web_path_small": "/template/images/blog/small/{0}.jpg".format(seo_url),
    }
