#!/usr/bin/env python3
"""Probe Lireate /admin/ from worker IP: RCPC, login form, news module links."""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lireate_cms_http import LireateCmsClient, _FormCollector  # noqa: E402
from lireate_compat import require_python  # noqa: E402
from lireate_dotenv import load_dotenv  # noqa: E402

require_python((3, 6))

load_dotenv(Path(os.environ.get("LIREATE_ENV_FILE") or (Path.home() / "lireate-autopub" / ".env")))

CANDIDATE_PATHS = [
    "/admin/",
    "/admin/index.php",
    "/admin/main.php",
    "/admin/news.php",
    "/admin/news/",
    "/admin/news/index.php",
    "/admin/news/edit.php",
    "/admin/news/add.php",
    "/admin/blog.php",
    "/admin/articles.php",
    "/admin/content.php",
    "/admin/pages.php",
    "/admin/?module=news",
    "/admin/?mod=news",
]


def _res_dict(res):
    return {"ok": res.ok, "stage": res.stage, "detail": res.detail, "extra": res.extra}


def main():
    site = (os.environ.get("LIREATE_PUBLIC_SITE_URL") or "").strip().rstrip("/")
    if not site:
        print("FAIL: set LIREATE_PUBLIC_SITE_URL", file=sys.stderr)
        return 2

    user = (os.environ.get("LIREATE_ADMIN_USER") or "").strip()
    password = os.environ.get("LIREATE_ADMIN_PASSWORD") or ""
    if not user or not password:
        print("FAIL: set LIREATE_ADMIN_USER and LIREATE_ADMIN_PASSWORD", file=sys.stderr)
        return 2

    out_dir = REPO_ROOT / "memory" / "lireate-cms-probe"
    out_dir.mkdir(parents=True, exist_ok=True)

    client = LireateCmsClient(site)
    report = {"site": site, "stages": []}

    warm = client.warmup_rcpc()
    report["stages"].append({"rcpc": _res_dict(warm)})
    if not warm.ok:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    login_url = warm.extra.get("url", "{0}/admin/login.php".format(site))
    status, html, _ = client._request(login_url)
    parser = _FormCollector()
    parser.feed(html)
    (out_dir / "login-page.html").write_text(html[:500000], encoding="utf-8")
    report["login_page"] = {"status": status, "forms": parser.forms, "html_len": len(html)}

    login_form = client._pick_login_form(parser.forms)
    if login_form and client._form_has_captcha(login_form):
        report["stages"].append(
            {
                "login": {
                    "ok": False,
                    "stage": "login",
                    "detail": "captcha on login form — use DB publish on hosting",
                    "extra": {},
                }
            }
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    login_res = client.login(user, password, {})
    report["stages"].append({"login": _res_dict(login_res)})
    if not login_res.ok:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    hits = []
    for path in CANDIDATE_PATHS:
        url = client._abs(path)
        st, body, _ = client._request(url)
        score = 0
        low = body.lower()
        for kw in ("новост", "news", "блог", "blog", "category", "рубрик", "alias", "чпу"):
            if kw in low:
                score += 1
        if score >= 2 or (st == 200 and len(body) > 3000):
            safe = path.strip("/").replace("/", "_") or "root"
            snippet_path = out_dir / ("hit_{0}.html".format(safe))
            snippet_path.write_text(body[:300000], encoding="utf-8")
        hits.append({"path": path, "status": st, "len": len(body), "score": score})

    hits.sort(key=lambda x: (-x["score"], -x["len"]))
    report["admin_path_hits"] = hits[:20]

    suggested = REPO_ROOT / "shared" / "lireate-cms-http-config.json.example"
    example = json.loads(suggested.read_text(encoding="utf-8")) if suggested.is_file() else {}
    if login_res.extra.get("user_field"):
        example.setdefault("login", {})
        example["login"]["username_field"] = login_res.extra["user_field"]
        example["login"]["password_field"] = login_res.extra["pass_field"]
    if hits:
        best = hits[0]
        example.setdefault("news", {})
        example["news"]["create_path"] = best["path"]
        example["news"]["_probe_note"] = "Откройте memory/lireate-cms-probe/*.html и заполните fields вручную"

    dest = REPO_ROOT / "memory" / "lireate-cms-http-config.json"
    dest.write_text(json.dumps(example, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report["wrote_config_draft"] = str(dest)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\nOK: draft config -> {0}".format(dest), file=sys.stderr)
    print("Next: edit news.fields in that JSON, then run lireate_news_publish.py", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
