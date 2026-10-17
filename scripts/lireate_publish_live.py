"""Live URL checks and publish state (stdlib, Py3.8)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def http_status(url: str, method: str = "HEAD", timeout: int = 25) -> Any:
    try:
        req = urllib.request.Request(
            url,
            method=method,
            headers={"User-Agent": "lireate_publish/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"{type(e).__name__}: {e}"


def load_state(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"articles": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"articles": {}}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def record_published(state_path: Path, slug: str, topic_id: Optional[str], url: str, category_id: int) -> None:
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


def is_already_live(site: str, canonical_path: str, state_path: Optional[Path], slug: str) -> tuple[bool, Any]:
    url = f"{site.rstrip('/')}{canonical_path}"
    status = http_status(url)
    if status == 200:
        return True, status
    if state_path and state_path.is_file():
        state = load_state(state_path)
        entry = (state.get("articles") or {}).get(slug) or {}
        if entry.get("status") == "published" and entry.get("url"):
            status2 = http_status(entry["url"])
            if status2 == 200:
                return True, status2
    return False, status
