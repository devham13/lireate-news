from pathlib import Path


def load_topic_id(article_dir):
    import json

    meta_path = Path(article_dir) / "article.meta.json"
    if not meta_path.is_file():
        return ""
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return (meta.get("topic_id") or "").strip()


def collage_allowed(article_dir):
    """Return (ok, reason). Never mutate L01-L05 or legacy KIE-only dirs."""
    from .constants import FROZEN_TOPIC_IDS

    article_dir = Path(article_dir)
    import json

    meta_path = article_dir / "article.meta.json"
    meta = {}
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    tid = (meta.get("topic_id") or "").strip()
    if tid in FROZEN_TOPIC_IDS:
        return False, "frozen topic {0}".format(tid)
    if meta.get("cover_style") == "collage-v1":
        return True, ""
    if (article_dir / "cover" / "kie-raw.png").is_file():
        return False, "existing KIE cover (set cover_style=collage-v1 only for new dirs)"
    if meta.get("cover_fallback") == "kie" and not meta.get("cover_style"):
        return False, "kie-only meta without collage-v1"
    # New article dir: allow if topic is L* and not frozen
    if tid.startswith("L") and tid not in FROZEN_TOPIC_IDS:
        return True, ""
    if tid.startswith("B"):
        return True, ""
    return False, "not a new Lireate article dir"
