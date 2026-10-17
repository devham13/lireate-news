"""HTTP client for Lireate custom CMS (/admin/). Uses only LIREATE_* env."""

import json
import os
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from http.cookiejar import Cookie, CookieJar
from pathlib import Path

from lireate_compat import header_charset, http_response_code

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = REPO_ROOT / "memory" / "lireate-cms-http-config.json"
EXAMPLE_CONFIG_PATH = REPO_ROOT / "shared" / "lireate-cms-http-config.json.example"

USER_AGENT = "lireate_cms_http/1.0 (+worker)"


class CmsHttpResult(object):
    def __init__(self, ok, stage, detail, extra=None):
        self.ok = ok
        self.stage = stage
        self.detail = detail
        self.extra = extra if extra is not None else {}


class _FormCollector(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.forms = []
        self._form = None
        self._in_form = False

    def handle_starttag(self, tag, attrs):
        ad = {k: (v or "") for k, v in attrs}
        if tag == "form":
            self._in_form = True
            self._form = {
                "action": ad.get("action", ""),
                "method": (ad.get("method") or "GET").upper(),
                "inputs": [],
                "textareas": [],
            }
        elif self._in_form and self._form is not None:
            if tag == "input":
                self._form["inputs"].append(
                    {
                        "name": ad.get("name", ""),
                        "type": (ad.get("type") or "text").lower(),
                        "value": ad.get("value", ""),
                    }
                )
            elif tag == "textarea":
                self._form["textareas"].append({"name": ad.get("name", "")})

    def handle_endtag(self, tag):
        if tag == "form" and self._in_form and self._form is not None:
            self.forms.append(self._form)
            self._form = None
            self._in_form = False


class LireateCmsClient(object):
    def __init__(self, site_url, admin_base=None):
        self.site_url = site_url.rstrip("/")
        parsed = urllib.parse.urlparse(self.site_url)
        self.vhost = (parsed.hostname or "").strip()
        cms_base = (os.environ.get("LIREATE_CMS_HTTP_BASE") or "").strip().rstrip("/")
        self.http_origin = cms_base or self.site_url
        admin = (admin_base or os.environ.get("LIREATE_ADMIN_URL") or "").strip()
        if not admin:
            admin = "{0}/admin/".format(self.http_origin)
        elif admin.startswith("/"):
            admin = self.http_origin + admin
        self.admin_base = admin.rstrip("/") + "/"
        self.jar = CookieJar()
        ctx = ssl.create_default_context()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar),
            urllib.request.HTTPSHandler(context=ctx),
        )

    def _request(self, url, method="GET", data=None, headers=None):
        hdrs = {"User-Agent": USER_AGENT}
        cms_base_env = (os.environ.get("LIREATE_CMS_HTTP_BASE") or "").strip()
        if self.vhost and cms_base_env:
            hdrs.setdefault("Host", self.vhost)
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(url, data=data, headers=hdrs)
        if method and method.upper() != "GET":
            req.get_method = lambda m=method.upper(): m
        try:
            resp = self.opener.open(req, timeout=45)
            try:
                body = resp.read()
                charset = header_charset(resp.headers) or "utf-8"
                try:
                    text = body.decode(charset, errors="replace")
                except LookupError:
                    text = body.decode("utf-8", errors="replace")
                return http_response_code(resp), text, dict(resp.headers)
            finally:
                resp.close()
        except urllib.error.HTTPError as e:
            body = e.read()
            charset = header_charset(e.headers) if e.headers else None
            text = body.decode(charset or "utf-8", errors="replace")
            return e.code, text, dict(e.headers or {})

    def _abs(self, path_or_url):
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        if path_or_url.startswith("/"):
            return self.http_origin + path_or_url
        return urllib.parse.urljoin(self.admin_base, path_or_url)

    def _is_rcpc_stub(self, html):
        if len(html) < 400 and "Refresh" in html and "attempt=" in html:
            return True
        if "RCPC" in html and 'type="password"' not in html.lower():
            return len(html) < 2000
        return False

    def _meta_refresh_url(self, html):
        m = re.search(
            r'URL=([^"\'>\s]+)',
            html,
            flags=re.IGNORECASE,
        )
        if m:
            return self._abs(m.group(1).strip())
        return None

    def warmup_rcpc(self, start_path="/admin/login.php", max_hops=12):
        url = self._abs(start_path)
        for hop in range(max_hops):
            status, html, _hdr = self._request(url)
            if not self._is_rcpc_stub(html):
                return CmsHttpResult(
                    ok=True,
                    stage="rcpc_warmup",
                    detail="ready after {0} hops".format(hop),
                    extra={"url": url, "status": status, "html_len": len(html)},
                )
            nxt = self._meta_refresh_url(html)
            if not nxt:
                return CmsHttpResult(
                    ok=False,
                    stage="rcpc_warmup",
                    detail="RCPC stub without refresh URL (need worker / home IP)",
                    extra={"url": url, "status": status},
                )
            url = nxt
        return CmsHttpResult(
            ok=False,
            stage="rcpc_warmup",
            detail="RCPC loop exceeded {0} hops".format(max_hops),
            extra={"last_url": url},
        )

    def _pick_login_form(self, forms):
        for form in forms:
            has_pass = any(i.get("type") == "password" for i in form.get("inputs", []))
            if has_pass:
                return form
        return forms[0] if forms else None

    def login(self, username, password, config):
        cookie_hdr = (os.environ.get("LIREATE_ADMIN_COOKIE") or "").strip()
        if cookie_hdr:
            for part in cookie_hdr.split(";"):
                part = part.strip()
                if "=" in part:
                    name, val = part.split("=", 1)
                    self.jar.set_cookie(
                        Cookie(
                            version=0,
                            name=name.strip(),
                            value=val.strip(),
                            port=None,
                            port_specified=False,
                            domain="",
                            domain_specified=False,
                            domain_initial_dot=False,
                            path="/",
                            path_specified=True,
                            secure=False,
                            expires=None,
                            discard=True,
                            comment=None,
                            comment_url=None,
                            rest={},
                            rfc2109=False,
                        )
                    )
            return CmsHttpResult(ok=True, stage="login", detail="used LIREATE_ADMIN_COOKIE")

        login_cfg = config.get("login") or {}
        login_path = login_cfg.get("path") or "/admin/login.php"
        warm = self.warmup_rcpc(login_path)
        if not warm.ok:
            return warm

        login_url = warm.extra.get("url") or self._abs(login_path)
        status, html, _ = self._request(login_url)
        parser = _FormCollector()
        parser.feed(html)
        form = self._pick_login_form(parser.forms)
        if not form:
            return CmsHttpResult(
                ok=False,
                stage="login",
                detail="login form not found (RCPC or wrong URL)",
                extra={"status": status, "html_len": len(html), "url": login_url},
            )

        user_field = login_cfg.get("username_field")
        pass_field = login_cfg.get("password_field")
        if not user_field or not pass_field:
            for inp in form["inputs"]:
                n = inp.get("name") or ""
                low = n.lower()
                if inp.get("type") == "password":
                    pass_field = pass_field or n
                elif any(x in low for x in ("login", "user", "email", "name")) and inp.get("type") != "hidden":
                    user_field = user_field or n
            if not user_field:
                for inp in form["inputs"]:
                    if inp.get("type") not in ("hidden", "submit", "button", "password") and inp.get("name"):
                        user_field = inp["name"]
                        break
        if not user_field or not pass_field:
            return CmsHttpResult(
                ok=False,
                stage="login",
                detail="could not detect username/password field names — run lireate_cms_probe.py",
                extra={"form": form},
            )

        payload = {}
        for inp in form["inputs"]:
            name = inp.get("name")
            if not name:
                continue
            if name == user_field:
                payload[name] = username
            elif name == pass_field:
                payload[name] = password
            elif inp.get("type") in ("hidden",):
                payload[name] = inp.get("value") or ""
            elif inp.get("type") == "submit" and inp.get("value"):
                payload[name] = inp["value"]

        extra_login = login_cfg.get("extra_fields") or {}
        for k, v in extra_login.items():
            payload[k] = str(v)

        action = form.get("action") or login_path
        post_url = self._abs(action)
        data = urllib.parse.urlencode(payload).encode("utf-8")
        status2, html2, _ = self._request(
            post_url,
            method="POST",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        still_login = "password" in html2.lower() and login_path.split("/")[-1] in html2.lower()
        has_sess = any(c.name == "PHPSESSID" for c in self.jar)
        ok = status2 in (200, 302, 303) and not still_login and has_sess
        if not ok and has_sess and not self._is_rcpc_stub(html2):
            ok = True

        return CmsHttpResult(
            ok=ok,
            stage="login",
            detail="logged in" if ok else "login failed (check LIREATE_ADMIN_* or form config)",
            extra={
                "post_url": post_url,
                "status": status2,
                "php_sessid": has_sess,
                "user_field": user_field,
                "pass_field": pass_field,
            },
        )

    def _load_config(self):
        cfg_path = os.environ.get("LIREATE_CMS_HTTP_CONFIG") or str(DEFAULT_CONFIG_PATH)
        path = Path(cfg_path)
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
        if EXAMPLE_CONFIG_PATH.is_file():
            return json.loads(EXAMPLE_CONFIG_PATH.read_text(encoding="utf-8"))
        return {}

    def _format_fields(self, template, ctx):
        out = {}
        for k, v in template.items():
            s = v
            for key, val in ctx.items():
                s = s.replace("{" + key + "}", val)
            out[k] = s
        return out

    def publish_news(self, meta, body_html, skip_if_live=True):
        slug = meta.get("slug") or ""
        canonical = meta.get("canonical_path") or "/{0}".format(slug)
        if skip_if_live and self.site_url:
            live_url = "{0}{1}".format(self.site_url, canonical)
            try:
                req = urllib.request.Request(
                    live_url,
                    headers={"User-Agent": USER_AGENT},
                )
                req.get_method = lambda: "HEAD"
                resp = self.opener.open(req, timeout=25)
                try:
                    st = http_response_code(resp)
                finally:
                    resp.close()
            except urllib.error.HTTPError as e:
                st = e.code
            except Exception:
                st = None
            if st == 200:
                return CmsHttpResult(
                    ok=True,
                    stage="publish",
                    detail="already_live_skip_cms",
                    extra={"live_url": live_url, "http_status": st},
                )

        config = self._load_config()
        news_cfg = config.get("news") or {}
        if not news_cfg.get("create_path"):
            return CmsHttpResult(
                ok=False,
                stage="publish",
                detail="news.create_path missing — run probe and save memory/lireate-cms-http-config.json",
            )

        username = (os.environ.get("LIREATE_ADMIN_USER") or "").strip()
        password = os.environ.get("LIREATE_ADMIN_PASSWORD") or ""
        if not username or not password:
            return CmsHttpResult(ok=False, stage="publish", detail="missing LIREATE_ADMIN_USER/PASSWORD")

        login_res = self.login(username, password, config)
        if not login_res.ok:
            return login_res

        canonical = canonical.strip("/")
        alias = canonical.split("/")[-1] if canonical else slug.replace("-", "_")

        ctx = {
            "title": meta.get("title") or "",
            "h1": meta.get("h1") or "",
            "description": meta.get("description") or "",
            "slug": slug,
            "alias": alias,
            "canonical_path": meta.get("canonical_path") or "/{0}".format(slug),
            "category_id": str(meta.get("lireate_category_id", 9)),
            "body_html": body_html,
        }

        field_template = news_cfg.get("fields") or {}
        payload = self._format_fields(field_template, ctx)

        create_path = news_cfg["create_path"]
        url = self._abs(create_path)
        method = (news_cfg.get("method") or "POST").upper()
        if method == "GET":
            url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(payload)
            data = None
        else:
            data = urllib.parse.urlencode(payload).encode("utf-8")

        status, html, _ = self._request(
            url,
            method=method,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"} if data else None,
        )

        success_contains = news_cfg.get("success_html_contains") or []
        success_url = news_cfg.get("success_url_contains") or meta.get("canonical_path", "")
        ok = status in (200, 302, 303)
        if success_contains:
            ok = ok and all(s in html for s in success_contains)
        if success_url and success_url not in html and status not in (302, 303):
            pass

        return CmsHttpResult(
            ok=ok,
            stage="publish",
            detail="news POST sent" if ok else "news POST uncertain — verify live URL",
            extra={"url": url, "status": status, "html_len": len(html)},
        )


def load_http_config_path():
    raw = os.environ.get("LIREATE_CMS_HTTP_CONFIG") or str(DEFAULT_CONFIG_PATH)
    return Path(raw)
