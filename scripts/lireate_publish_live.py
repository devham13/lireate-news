"""Live URL checks and publish state (stdlib, Py3.6+)."""

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def http_status(url, method="HEAD", timeout=25):
    try:
        req = urllib.request.Request(
            url,
            data=None,
            headers={"User-Agent": "lireate_publish/1.0"},
        )
        if method and method != "GET":
            req.get_method = lambda m=method: m  # type: ignore — Py3.6
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return getattr(resp, "status", None) or resp.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return "{0}: {1}".format(type(e).__name__, e)


def load_state(path):
    path = Path(path)
    if not path.is_file():
        return {"articles": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return {"articles": {}}


def save_state(path, state):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def record_published(state_path, slug, topic_id, url, category_id):
    state = load_state(state_path)
    articles = state.setdefault("articles", {})
    articles[slug] = {
        "topic_id": topic_id,
        "url": url,
        "category_id": category_id,
        "status": "published",
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    save_state(state_path, state)


def is_already_live(site, canonical_path, state_path, slug):
    url = "{0}{1}".format(site.rstrip("/"), canonical_path)
    status = http_status(url)
    if status == 200:
        return True, status
    if state_path and Path(state_path).is_file():
        state = load_state(state_path)
        entry = (state.get("articles") or {}).get(slug) or {}
        if entry.get("status") == "published" and entry.get("url"):
            status2 = http_status(entry["url"])
            if status2 == 200:
                return True, status2
    return False, status
