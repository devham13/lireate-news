#!/usr/bin/env python3
"""
Export Yandex Webmaster API v4 stats from REG.RU hosting (stdlib + urllib only).

Writes atomically to $LIREATE_AUTOPUB_HOME/analytics/webmaster.json.
Never prints OAuth token or analytics key.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://api.webmaster.yandex.net/v4"
DEFAULT_HOST_HINTS = ("lireate.ru",)
OUTPUT_NAME = "webmaster.json"
HOSTING_ANALYTICS_REL = Path("hosting") / "lireate-analytics"
WEBMASTER_TEMPLATE_NAME = "webmaster.php"
# PHP 7+ markers — must not appear in deployed endpoint (hosting mod_php may be 5.x).
_LEGACY_PHP7_MARKERS = ("declare(strict_types=1)",)
TOKEN_RE = re.compile(r"(?i)(oauth|authorization|bearer|token)[^\s]*\s+[\w\-\.~+/]+=*")


def _default_autopub_home() -> Path:
    return Path(os.environ.get("LIREATE_AUTOPUB_HOME") or (Path.home() / "lireate-autopub"))


def _load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        if key not in os.environ:
            os.environ[key] = val


def _sanitize_text(text: str) -> str:
    if not text:
        return text
    return TOKEN_RE.sub("[redacted]", text)


def _utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


class WebmasterClient:
    def __init__(self, token: str, timeout: float = 60.0):
        self._token = token
        self._timeout = timeout

    def request_json(self, path: str, query: Optional[List[Tuple[str, str]]] = None) -> Tuple[Optional[Any], Optional[str]]:
        url = API_BASE + path
        if query:
            url = url + "?" + urlencode(query, doseq=True)
        req = Request(url, method="GET")
        req.add_header("Authorization", "OAuth {0}".format(self._token))
        req.add_header("Accept", "application/json")
        try:
            with urlopen(req, timeout=self._timeout) as resp:
                body = resp.read().decode("utf-8")
        except HTTPError as e:
            try:
                body = e.read().decode("utf-8")
            except Exception:
                body = ""
            msg = _sanitize_text(body or str(e))
            if e.code == 403 and "INVALID_USER_ID" in body:
                try:
                    data = json.loads(body)
                    avail = data.get("available_user_id")
                    if avail is not None:
                        return None, "INVALID_USER_ID: use user_id={0}".format(avail)
                except json.JSONDecodeError:
                    pass
            return None, "HTTP {0}: {1}".format(e.code, msg[:500])
        except URLError as e:
            return None, _sanitize_text(str(e.reason if hasattr(e, "reason") else e))
        except Exception as e:
            return None, _sanitize_text(str(e))
        try:
            return json.loads(body), None
        except json.JSONDecodeError:
            return None, "invalid JSON response"


def _pick_host(hosts: List[Dict[str, Any]], hints: Tuple[str, ...]) -> Optional[Dict[str, Any]]:
    candidates = []
    for h in hosts or []:
        hid = (h.get("host_id") or "").lower()
        urls = " ".join(
            [
                str(h.get("ascii_host_url") or ""),
                str(h.get("unicode_host_url") or ""),
                hid,
            ]
        ).lower()
        if any(hint in urls for hint in hints):
            candidates.append(h)
    if not candidates:
        return None

    def score(h: Dict[str, Any]) -> Tuple[int, int]:
        hid = (h.get("host_id") or "").lower()
        s = 0
        if hid.startswith("https:"):
            s += 10
        if ":443" in hid:
            s += 5
        if h.get("verified"):
            s += 3
        return (s, 0)

    candidates.sort(key=score, reverse=True)
    return candidates[0]


def _date_range(days: int) -> Tuple[str, str]:
    end = date.today()
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def _enrich_queries(queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for row in queries or []:
        ind = row.get("indicators") or {}
        shows = ind.get("TOTAL_SHOWS")
        clicks = ind.get("TOTAL_CLICKS")
        ctr = None
        try:
            if shows and float(shows) > 0 and clicks is not None:
                ctr = round(float(clicks) / float(shows) * 100.0, 4)
        except (TypeError, ValueError):
            ctr = None
        out.append(
            {
                "query_id": row.get("query_id"),
                "query_text": row.get("query_text"),
                "shows": shows,
                "clicks": clicks,
                "ctr_percent": ctr,
                "avg_show_position": ind.get("AVG_SHOW_POSITION"),
                "avg_click_position": ind.get("AVG_CLICK_POSITION"),
            }
        )
    return out


def _fetch_popular(
    client: WebmasterClient,
    user_id: int,
    host_id: str,
    days: int,
    limit: int = 50,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    date_from, date_to = _date_range(days)
    query: List[Tuple[str, str]] = [
        ("order_by", "TOTAL_SHOWS"),
        ("limit", str(limit)),
        ("date_from", date_from),
        ("date_to", date_to),
    ]
    for qi in ("TOTAL_SHOWS", "TOTAL_CLICKS", "AVG_SHOW_POSITION", "AVG_CLICK_POSITION"):
        query.append(("query_indicator", qi))
    path = "/user/{0}/hosts/{1}/search-queries/popular".format(user_id, host_id)
    data, err = client.request_json(path, query)
    if err:
        return None, err
    return {
        "days": days,
        "date_from": data.get("date_from") or date_from,
        "date_to": data.get("date_to") or date_to,
        "count": data.get("count"),
        "queries": _enrich_queries(data.get("queries") or []),
    }, None


def _fetch_section(
    errors: Dict[str, str],
    key: str,
    fn: Callable[[], Tuple[Optional[Any], Optional[str]]],
) -> Any:
    try:
        data, err = fn()
    except Exception as e:
        errors[key] = _sanitize_text(str(e))
        return None
    if err:
        errors[key] = err
        return None
    return data


def _atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".webmaster-", suffix=".json", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(str(tmp_path), str(path))
    finally:
        if tmp_path.is_file():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def _webmaster_template_in(repo_root: Path) -> Path:
    return repo_root / HOSTING_ANALYTICS_REL / WEBMASTER_TEMPLATE_NAME


def _resolve_repo_root(autopub_home: Path) -> Path:
    """
    Canonical git checkout on hosting: $LIREATE_AUTOPUB_HOME/repo.
    Do not use a stale copy under $LIREATE_AUTOPUB_HOME/hosting/ (outside repo).
    """
    env_root = (os.environ.get("LIREATE_REPO_ROOT") or "").strip()
    candidates: List[Path] = []
    if env_root:
        candidates.append(Path(env_root).expanduser())
    candidates.append(autopub_home / "repo")
    candidates.append(Path(__file__).resolve().parents[1])

    seen = set()
    for root in candidates:
        try:
            resolved = root.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if _webmaster_template_in(resolved).is_file():
            return resolved

    tried = ", ".join(str(c) for c in candidates)
    raise FileNotFoundError(
        "webmaster.php template not found (expected {0} under repo root). Tried: {1}".format(
            HOSTING_ANALYTICS_REL, tried
        )
    )


def _assert_php54_compatible_template(text: str, src: Path) -> None:
    for marker in _LEGACY_PHP7_MARKERS:
        if marker in text:
            raise ValueError(
                "Template {0} still contains PHP 7+ syntax ({1}). "
                "Run git pull in $LIREATE_AUTOPUB_HOME/repo.".format(src, marker)
            )
    if "define('LIREATE_AUTOPUB_HOME'" not in text and 'define("LIREATE_AUTOPUB_HOME"' not in text:
        raise ValueError(
            "Template {0} does not look like the PHP 5.4+ endpoint (missing define LIREATE_AUTOPUB_HOME).".format(
                src
            )
        )


def _deploy_php_endpoint(docroot: Path, autopub_home: Path) -> List[str]:
    repo = _resolve_repo_root(autopub_home)
    src_dir = repo / HOSTING_ANALYTICS_REL
    stale = autopub_home / HOSTING_ANALYTICS_REL / WEBMASTER_TEMPLATE_NAME
    if stale.is_file() and stale.resolve() != _webmaster_template_in(repo).resolve():
        print(
            "STATUS: WARN stale template outside repo (ignored): {0} — remove or update repo/ only".format(
                stale
            )
        )

    dest_dir = docroot / "lireate-analytics"
    dest_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(dest_dir, 0o755)
    except OSError:
        pass

    written: List[str] = []
    home_str = str(autopub_home.resolve())
    print("deploy source repo: {0}".format(repo))
    print("deploy template dir: {0}".format(src_dir))

    for name in (WEBMASTER_TEMPLATE_NAME, ".htaccess"):
        src = src_dir / name
        if not src.is_file():
            print("STATUS: WARN deploy skip missing: {0}".format(src))
            continue
        text = src.read_text(encoding="utf-8")
        if name == WEBMASTER_TEMPLATE_NAME:
            _assert_php54_compatible_template(text, src)
        text = text.replace("{{LIREATE_AUTOPUB_HOME}}", home_str)
        if name == WEBMASTER_TEMPLATE_NAME:
            for marker in _LEGACY_PHP7_MARKERS:
                if marker in text:
                    raise ValueError("Rendered webmaster.php still contains {0}".format(marker))
        dest = dest_dir / name
        dest.write_text(text, encoding="utf-8")
        try:
            os.chmod(dest, 0o644)
        except OSError:
            pass
        written.append(str(dest))
        print("deployed: {0} ({1} bytes, mode 644)".format(dest, dest.stat().st_size))
    return written


def build_export(
    client: WebmasterClient,
    host_hints: Tuple[str, ...],
    popular_limit: int = 50,
) -> Dict[str, Any]:
    errors: Dict[str, str] = {}
    out: Dict[str, Any] = {
        "generated_at": _utc_now_iso(),
        "api_base": API_BASE,
        "errors": errors,
    }

    user_data, user_err = client.request_json("/user")
    if user_err or not user_data:
        errors["user"] = user_err or "empty user response"
        return out
    user_id = user_data.get("user_id")
    if user_id is None and isinstance(user_data.get("available_user_id"), int):
        user_id = user_data.get("available_user_id")
    if user_id is None:
        errors["user"] = "missing user_id"
        return out
    out["user_id"] = user_id

    hosts_data, hosts_err = client.request_json("/user/{0}/hosts".format(user_id))
    if hosts_err or not hosts_data:
        errors["hosts"] = hosts_err or "empty hosts response"
        return out
    hosts = hosts_data.get("hosts") or []
    host = _pick_host(hosts, host_hints)
    if not host:
        errors["hosts"] = "host not found for hints: {0}".format(",".join(host_hints))
        out["hosts_available"] = [
            {"host_id": h.get("host_id"), "unicode_host_url": h.get("unicode_host_url")}
            for h in hosts[:20]
        ]
        return out

    host_id = host.get("host_id")
    out["host"] = {
        "host_id": host_id,
        "ascii_host_url": host.get("ascii_host_url"),
        "unicode_host_url": host.get("unicode_host_url"),
        "verified": host.get("verified"),
    }

    uid = user_id
    hid = host_id

    out["summary"] = _fetch_section(
        errors,
        "summary",
        lambda: client.request_json("/user/{0}/hosts/{1}/summary".format(uid, hid)),
    )
    out["diagnostics"] = _fetch_section(
        errors,
        "diagnostics",
        lambda: client.request_json("/user/{0}/hosts/{1}/diagnostics".format(uid, hid)),
    )

    out["search_queries"] = {
        "last_7_days": _fetch_section(
            errors,
            "search_queries.last_7_days",
            lambda: _fetch_popular(client, uid, hid, 7, popular_limit),
        ),
        "last_28_days": _fetch_section(
            errors,
            "search_queries.last_28_days",
            lambda: _fetch_popular(client, uid, hid, 28, popular_limit),
        ),
    }

    d_from, d_to = _date_range(30)
    out["indexing_history_30d"] = _fetch_section(
        errors,
        "indexing_history_30d",
        lambda: client.request_json(
            "/user/{0}/hosts/{1}/indexing/history".format(uid, hid),
            [("date_from", d_from), ("date_to", d_to)],
        ),
    )

    out["important_urls"] = _fetch_section(
        errors,
        "important_urls",
        lambda: client.request_json("/user/{0}/hosts/{1}/important-urls".format(uid, hid)),
    )

    def _excluded_sample():
        data, err = client.request_json(
            "/user/{0}/hosts/{1}/search-urls/events/samples".format(uid, hid),
            [("limit", "100")],
        )
        if err:
            return None, err
        samples = data.get("samples") or []
        removed = [s for s in samples if s.get("event") == "REMOVED_FROM_SEARCH"]
        return {"count_total": data.get("count"), "removed_sample": removed[:50]}, None

    out["excluded_pages"] = _fetch_section(errors, "excluded_pages", _excluded_sample)

    def _external_links():
        hist, err = client.request_json(
            "/user/{0}/hosts/{1}/links/external/history".format(uid, hid),
            [("indicator", "LINKS_TOTAL_COUNT")],
        )
        if err:
            return None, err
        samples, s_err = client.request_json(
            "/user/{0}/hosts/{1}/links/external/samples".format(uid, hid),
            [("limit", "20")],
        )
        if s_err:
            return {"history": hist, "samples_error": s_err}, None
        indicators = (hist or {}).get("indicators") or {}
        series = indicators.get("LINKS_TOTAL_COUNT") or []
        latest = series[-1] if series else None
        return {
            "history": hist,
            "latest_total": latest,
            "samples": samples,
        }, None

    out["external_links"] = _fetch_section(errors, "external_links", _external_links)

    if not errors:
        out["errors"] = {}
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Yandex Webmaster stats for lireate.ru hosting")
    parser.add_argument("--env-file", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--host-hint", action="append", default=None, help="Substring to match host (default: lireate.ru)")
    parser.add_argument("--popular-limit", type=int, default=50)
    parser.add_argument(
        "--deploy-php",
        action="store_true",
        help="After export, copy webmaster.php + .htaccess into $LIREATE_DOCROOT/lireate-analytics/",
    )
    parser.add_argument(
        "--deploy-php-only",
        action="store_true",
        help="Only deploy PHP from $LIREATE_AUTOPUB_HOME/repo/hosting/ (no Webmaster API export)",
    )
    args = parser.parse_args()

    home = _default_autopub_home()
    env_file = args.env_file or Path(os.environ.get("LIREATE_ENV_FILE") or (home / ".env"))
    _load_env_file(env_file)

    deploy_only = bool(args.deploy_php_only)
    if deploy_only and args.deploy_php:
        print("STATUS: BLOCKER use either --deploy-php-only or --deploy-php, not both")
        return 2

    host_id = None
    if not deploy_only:
        token = (os.environ.get("YANDEX_WEBMASTER_TOKEN") or "").strip()
        analytics_key = (os.environ.get("LIREATE_ANALYTICS_KEY") or "").strip()
        missing = []
        if not token:
            missing.append("YANDEX_WEBMASTER_TOKEN")
        if not analytics_key:
            missing.append("LIREATE_ANALYTICS_KEY")
        if missing:
            print("STATUS: BLOCKER missing env: {0} (in {1})".format(", ".join(missing), env_file))
            return 2

        hints = tuple(args.host_hint or DEFAULT_HOST_HINTS)
        client = WebmasterClient(token)
        payload = build_export(client, hints, popular_limit=max(1, min(args.popular_limit, 500)))

        out_path = args.output or (home / "analytics" / OUTPUT_NAME)
        try:
            _atomic_write_json(out_path, payload)
        except OSError as e:
            print("STATUS: BLOCKER write failed: {0}".format(e))
            return 1

        err_count = len(payload.get("errors") or {})
        host_id = (payload.get("host") or {}).get("host_id")
        print(
            "STATUS: OK written={0} host={1} section_errors={2}".format(
                out_path, host_id or "none", err_count
            )
        )

    if args.deploy_php or deploy_only:
        docroot = (os.environ.get("LIREATE_DOCROOT") or "").strip()
        if not docroot:
            print("STATUS: BLOCKER --deploy-php requires LIREATE_DOCROOT in {0}".format(env_file))
            return 2
        try:
            _deploy_php_endpoint(Path(docroot).expanduser(), home)
        except (OSError, ValueError, FileNotFoundError) as e:
            print("STATUS: BLOCKER deploy failed: {0}".format(e))
            return 1
        print("STATUS: OK deploy-php")

    if deploy_only:
        return 0
    return 0 if host_id else 1


if __name__ == "__main__":
    raise SystemExit(main())
