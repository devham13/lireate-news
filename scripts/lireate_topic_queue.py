"""Lireate topic queue helpers (Python 3.6+ compatible, used on REG.RU hosting too).

Rules:
- Topic cards live in memory/topics/blog-topics.md as `## Lxx — title` with `- **status:** new|written|published`.
- Next topic = first card with status `new` whose id has no folder in memory/blog/articles/.
- Never rewrite an existing article. No topic -> NO_NEW_TOPIC.
- Publish candidates = L* article folders not yet published (state file / result json / ALWAYS_PUBLISHED).
"""
import json
import re
from pathlib import Path

ALWAYS_PUBLISHED = {"L01"}
CARD_RE = re.compile(r"^##\s+(L\d+)\s+—[^\n]*\n(.*?)(?=^---|^##\s|\Z)", re.DOTALL | re.MULTILINE)
STATUS_RE = re.compile(r"\*\*status:\*\*\s*([a-z_]+)", re.I)


def _num(topic_id):
    m = re.match(r"L(\d+)", topic_id or "")
    return int(m.group(1)) if m else -1


def article_dirs(root):
    base = Path(root) / "memory/blog/articles"
    if not base.is_dir():
        return {}
    out = {}
    for p in base.iterdir():
        m = re.match(r"^(L\d+)-", p.name)
        if p.is_dir() and m:
            out[m.group(1)] = p
    return out


def topic_cards(root):
    path = Path(root) / "memory/topics/blog-topics.md"
    if not path.is_file():
        return []
    cards = []
    for m in CARD_RE.finditer(path.read_text(encoding="utf-8")):
        st = STATUS_RE.search(m.group(2))
        cards.append({"id": m.group(1), "status": (st.group(1).lower() if st else "unknown")})
    return cards


def next_new_topic(root):
    dirs = article_dirs(root)
    for c in topic_cards(root):
        if c["status"] == "new" and c["id"] not in dirs and c["id"] not in ALWAYS_PUBLISHED:
            return c["id"]
    return None


def published_ids(state_file, dirs):
    done = set(ALWAYS_PUBLISHED)
    try:
        data = json.loads(Path(state_file).read_text(encoding="utf-8"))
        items = data.values() if isinstance(data, dict) else data
        for it in items:
            if isinstance(it, dict) and it.get("topic_id"):
                done.add(str(it["topic_id"]).upper())
        if isinstance(data, dict):
            for k in data.keys():
                m = re.match(r"^(L\d+)", str(k).upper())
                if m:
                    done.add(m.group(1))
    except (OSError, ValueError):
        pass
    for tid, d in dirs.items():
        res = d / "lireate-publish-result.json"
        try:
            if json.loads(res.read_text(encoding="utf-8")).get("verdict") == "published":
                done.add(tid)
        except (OSError, ValueError):
            pass
    return done


def next_unpublished_article(root, state_file):
    """Newest (highest Lxx) article folder with article.html+meta that is not published."""
    dirs = article_dirs(root)
    done = published_ids(state_file, dirs)
    ready = [
        (tid, d) for tid, d in dirs.items()
        if tid not in done and (d / "article.html").is_file() and (d / "article.meta.json").is_file()
    ]
    if not ready:
        return None
    ready.sort(key=lambda x: _num(x[0]))
    return ready[-1][1]


if __name__ == "__main__":
    import sys
    root = Path(__file__).resolve().parents[1]
    t = next_new_topic(root)
    print("LIREATE_NEXT_TOPIC_ID=" + t if t else "NO_NEW_TOPIC")
    sys.exit(0)
