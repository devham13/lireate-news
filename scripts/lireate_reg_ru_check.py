#!/usr/bin/env python3
"""Preflight: REG.RU FTP for lireate.ru (LIREATE_* env only)."""

from __future__ import annotations

import ftplib
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request


def _truthy(name: str) -> bool:
    v = (os.environ.get(name) or "").strip().lower()
    return v in ("1", "yes", "true", "on")


def main() -> int:
    host = (os.environ.get("LIREATE_SFTP_HOST") or "").strip()
    port = int((os.environ.get("LIREATE_SFTP_PORT") or "21").strip())
    user = (os.environ.get("LIREATE_SFTP_USER") or "").strip()
    password = os.environ.get("LIREATE_SFTP_PASSWORD") or ""
    root = (os.environ.get("LIREATE_REMOTE_SITE_ROOT") or "/").strip() or "/"
    site = (os.environ.get("LIREATE_PUBLIC_SITE_URL") or "").strip()

    legacy = [k for k in ("FTP_HOST", "SFTP_HOST", "FTP_USER", "SFTP_USER") if os.environ.get(k)]
    report: dict[str, object] = {
        "host": host,
        "port": port,
        "user": user,
        "root": root,
        "allow_publish": os.environ.get("LIREATE_ALLOW_PUBLISH"),
        "pass_len": len(password),
        "pass_sha8": hashlib.sha256(password.encode()).hexdigest()[:8] if password else None,
        "legacy_beget_vars_set": legacy,
        "ftp_login": False,
        "cwd_root": False,
        "site_http": None,
    }

    if legacy:
        print(
            "INFO: в окружении есть FTP_*/SFTP_* — этот репозиторий их не использует, "
            f"проверяется только LIREATE_*: {', '.join(legacy)}",
            file=sys.stderr,
        )

    if not all([host, user, password]):
        print("FAIL: задайте LIREATE_SFTP_HOST, LIREATE_SFTP_USER, LIREATE_SFTP_PASSWORD", file=sys.stderr)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    if port != 21:
        print(
            f"WARN: LIREATE_SFTP_PORT={port}; для REG.RU FTP из панели обычно 21 (не SSH 22)",
            file=sys.stderr,
        )

    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=30)
        ftp.login(user, password)
        ftp.set_pasv(True)
        report["ftp_login"] = True
        report["ftp_pwd"] = ftp.pwd()
        if root not in (".", "/"):
            ftp.cwd(root.lstrip("/"))
        report["cwd_root"] = True
        report["cwd_after"] = ftp.pwd()
        ftp.quit()
    except Exception as e:
        report["ftp_error"] = f"{type(e).__name__}: {e}"
        print("FAIL: FTP", report["ftp_error"], file=sys.stderr)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    if site:
        try:
            req = urllib.request.Request(site, headers={"User-Agent": "lireate_reg_ru_check/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                report["site_http"] = resp.status
        except urllib.error.HTTPError as e:
            report["site_http"] = e.code
        except Exception as e:
            report["site_http"] = f"{type(e).__name__}: {e}"
    else:
        report["site_http"] = "skipped (LIREATE_PUBLIC_SITE_URL unset)"

    ok = report["ftp_login"] and report["cwd_root"]
    print("PASS" if ok else "FAIL")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
