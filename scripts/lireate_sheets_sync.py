#!/usr/bin/env python3
"""Reliable Google Sheets publication outbox for REG.RU; stdlib only (Python >=3.6)."""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def _short(text, limit=600):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit].rstrip()

def queue_dir():
    home = Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))
    return home / "state" / "sheets-outbox"

def enqueue(title, url, summary):
    from hashlib import sha256
    url = str(url or "").strip()
    if not (url.startswith("https://lireate.ru/") or url.startswith("http://lireate.ru/")):
        raise ValueError("only public lireate.ru article URLs allowed")
    if not title or not _short(summary):
        raise ValueError("title and summary required")
    folder = queue_dir()
    folder.mkdir(parents=True, exist_ok=True)
    key = sha256(url.rstrip("/").encode("utf-8")).hexdigest()
    path = folder / (key + ".json")
    data = {"title": _short(title, 240), "url": url, "summary": _short(summary)}
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)
    return path

def flush():
    folder = queue_dir()
    files = sorted(folder.glob("*.json")) if folder.is_dir() else []
    endpoint = os.environ.get("LIREATE_SHEETS_WEBHOOK_URL", "").strip()
    secret = os.environ.get("LIREATE_SHEETS_WEBHOOK_SECRET", "").strip()
    if not files:
        return {"status": "empty", "sent": 0, "pending": 0}
    if not endpoint.startswith("https://script.google.com/macros/s/") or not endpoint.endswith("/exec") or not secret:
        return {"status": "not_configured", "sent": 0, "pending": len(files)}
    sent = 0
    errors = []
    for file in files:
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            payload = json.dumps(dict(data, secret=secret), ensure_ascii=False).encode("utf-8")
            req = Request(endpoint, data=payload, headers={"Content-Type":"application/json; charset=utf-8"}, method="POST")
            with urlopen(req, timeout=20) as response:
                body = response.read(32768).decode("utf-8")
            result = json.loads(body)
            if result.get("ok") is not True:
                raise ValueError("endpoint returned unsuccessful status")
            file.unlink()
            sent += 1
        except (OSError, ValueError, HTTPError, URLError) as exc:
            errors.append(type(exc).__name__)
    remaining = len(list(folder.glob("*.json")))
    return {"status": "ok" if not remaining else "pending", "sent": sent, "pending": remaining, "errors": errors[:3]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title")
    p.add_argument("--url")
    p.add_argument("--summary")
    a = p.parse_args()
    if any((a.title, a.url, a.summary)):
        if not all((a.title, a.url, a.summary)):
            p.error("title, url and summary must all be provided")
        enqueue(a.title, a.url, a.summary)
    result = flush()
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] in ("ok", "empty") else 1

if __name__ == "__main__":
    sys.exit(main())
