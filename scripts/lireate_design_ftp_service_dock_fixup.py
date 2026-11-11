#!/usr/bin/env python3
"""FTP: upload dock assets, patch main.php + LU landings (backup *.bak-2026-11-11-design)."""
import ftplib
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BAK = "bak-2026-11-11-design"
PY = sys.executable

LANDINGS = [
    "findtz/index.php",
    "registraciya_tovarnogo_znaka/index.php",
    "registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/index.php",
    "prodlenie_tovarnogo_znaka/index.php",
    "vozrazhenie_protiv_registracii_tovarnogo_znaka/index.php",
    "registraciya_tovarnogo_znaka_v_kitae/index.php",
    "zashchita_avtorskih_prav/index.php",
]


def env(name: str) -> str:
    v = (os.environ.get(name) or "").strip()
    if not v:
        raise SystemExit(f"missing {name}")
    return v


def ftp_connect() -> ftplib.FTP:
    host = env("LIREATE_SFTP_HOST")
    port = int(os.environ.get("LIREATE_SFTP_PORT") or "21")
    user = env("LIREATE_SFTP_USER")
    password = env("LIREATE_SFTP_PASSWORD")
    ftp = ftplib.FTP()
    ftp.connect(host, port, timeout=300)
    ftp.login(user, password)
    ftp.cwd(env("LIREATE_REMOTE_SITE_ROOT").rstrip("/"))
    return ftp


def ftp_cwd_root(ftp: ftplib.FTP) -> None:
    ftp.cwd("/")
    ftp.cwd(env("LIREATE_REMOTE_SITE_ROOT").rstrip("/"))


def ensure_dir(ftp: ftplib.FTP, parts: list[str]) -> None:
    ftp_cwd_root(ftp)
    for p in parts:
        try:
            ftp.cwd(p)
        except ftplib.error_perm:
            ftp.mkd(p)
            ftp.cwd(p)


def upload_file(ftp: ftplib.FTP, local: Path, remote_rel: str) -> None:
    remote_rel = remote_rel.replace("\\", "/")
    parts = remote_rel.split("/")
    fname = parts[-1]
    ensure_dir(ftp, parts[:-1])
    try:
        ftp.rename(fname, f"{fname}.{BAK}")
    except ftplib.error_perm:
        pass
    with local.open("rb") as f:
        ftp.storbinary(f"STOR {fname}", f)


def download_file(ftp: ftplib.FTP, remote_rel: str, local: Path) -> bool:
    remote_rel = remote_rel.replace("\\", "/")
    parts = remote_rel.split("/")
    ensure_dir(ftp, parts[:-1])
    local.parent.mkdir(parents=True, exist_ok=True)
    try:
        with local.open("wb") as f:
            ftp.retrbinary(f"RETR {parts[-1]}", f.write)
        return True
    except ftplib.error_perm:
        return False


def main() -> None:
    ftp = ftp_connect()
    tmp = Path("/tmp/lireate-dock-fix")
    tmp.mkdir(parents=True, exist_ok=True)

    assets = [
        ("hosting-design/template/css/lireate-service-mobile-bar.css", "template/css/lireate-service-mobile-bar.css"),
        ("hosting-design/template/js/lireate-service-mobile-bar.js", "template/js/lireate-service-mobile-bar.js"),
        ("hosting-design/template/js/lireate-service-metrika-goals.js", "template/js/lireate-service-metrika-goals.js"),
        ("hosting-design/template/lireate/lireate-service-mobile-bar.inc.php", "template/lireate/lireate-service-mobile-bar.inc.php"),
    ]
    def with_ftp(fn):
        nonlocal ftp
        try:
            fn(ftp)
        except (TimeoutError, ftplib.error_temp, OSError) as e:
            print("FTP_RETRY", e, file=sys.stderr)
            try:
                ftp.quit()
            except Exception:
                pass
            ftp = ftp_connect()
            fn(ftp)

    for rel_src, rel_dst in assets:
        with_ftp(lambda f: upload_file(f, REPO / rel_src, rel_dst))
        print("UPLOAD", rel_dst)

    main_local = tmp / "template/main.php"
    with_ftp(lambda f: download_file(f, "template/main.php", main_local))
    if main_local.is_file():
        subprocess.check_call([PY, str(REPO / "scripts/lireate_design_patch_service_mobile_dock.py"), str(main_local)])
        with_ftp(lambda f: upload_file(f, main_local, "template/main.php"))
        print("PATCH main.php OK")

    for rel in LANDINGS:
        with_ftp(lambda f, r=rel: download_file(f, r, tmp / r))
    subprocess.check_call([PY, str(REPO / "scripts/lireate_design_patch_service_landings.py"), str(tmp)])
    for rel in LANDINGS:
        local = tmp / rel
        if local.is_file():
            with_ftp(lambda f, loc=local, r=rel: upload_file(f, loc, r))
            print("UPLOAD", rel)

    try:
        ftp.quit()
    except Exception:
        pass
    time.sleep(3)
    print("FTP_DOCK_FIXUP_OK")


if __name__ == "__main__":
    main()
