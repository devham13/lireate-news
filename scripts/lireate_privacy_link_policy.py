#!/usr/bin/env python3
"""Lireate: forbid fake privacy/policy URLs; canonical legal pages only."""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse

CANONICAL_PATHS = frozenset(
    {
        "/politika_konfidencialnosti",
        "/private_data",
    }
)

FORBIDDEN_PATH_RE = re.compile(
    r"(?:^|/)(?:privacy|policy)(?:/|$|\?)",
    re.IGNORECASE,
)


class _HrefExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "a":
            return
        for key, val in attrs:
            if key.lower() == "href" and val:
                self.hrefs.append(val.strip())


def extract_hrefs(html: str) -> List[str]:
    parser = _HrefExtractor()
    parser.feed(html)
    return parser.hrefs


def normalize_path(href: str) -> str:
    href = href.strip()
    if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
        return ""
    if href.startswith("/"):
        path = href.split("?", 1)[0].split("#", 1)[0]
        return path.rstrip("/") or "/"
    parsed = urlparse(href)
    if not parsed.scheme:
        path = "/" + href.lstrip("/")
        path = path.split("?", 1)[0].split("#", 1)[0]
        return path.rstrip("/") or "/"
    return parsed.path.rstrip("/") or "/"


def is_canonical_legal_href(href: str) -> bool:
    path = normalize_path(href.strip())
    return path in CANONICAL_PATHS


def is_forbidden_privacy_href(href: str) -> bool:
    h = href.strip()
    if not h or h.startswith("#") or h.startswith("mailto:") or h.startswith("tel:"):
        return False
    if is_canonical_legal_href(h):
        return False
    low = h.lower()
    if re.search(r"/privacy(?:/|$|\?)", low) or re.search(r"/policy(?:/|$|\?)", low):
        if not is_canonical_legal_href(h):
            return True
    path = normalize_path(h)
    if not path:
        return False
    if FORBIDDEN_PATH_RE.search(path):
        return True
    return False


def audit_html(html: str, source: str = "article.html") -> List[str]:
    errors: List[str] = []
    for href in extract_hrefs(html):
        if is_forbidden_privacy_href(href):
            errors.append(
                "{0}: forbidden privacy/policy URL {1!r}; use /politika_konfidencialnosti or /private_data "
                "(see shared/lireate-legal-page-urls.md)".format(source, href)
            )
    return errors


def lireate_article_html_files(root: Path) -> List[Path]:
    base = root / "memory/blog/articles"
    if not base.is_dir():
        return []
    out: List[Path] = []
    for p in sorted(base.iterdir()):
        if p.is_dir() and re.match(r"^L\d+-", p.name):
            html = p / "article.html"
            if html.is_file():
                out.append(html)
    return out


def audit_file(html_path: Path) -> List[str]:
    html = html_path.read_text(encoding="utf-8")
    return audit_html(html, source=str(html_path).replace("\\", "/"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Lireate privacy/policy link policy")
    ap.add_argument("html", type=Path, nargs="?", help="Single article.html")
    ap.add_argument("--all-lireate", action="store_true", help="Scan all L* article.html")
    ap.add_argument("-o", "--output", type=Path, help="Write JSON report")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    files: List[Path] = []
    if args.all_lireate:
        files = lireate_article_html_files(root)
    elif args.html:
        files = [args.html]
    else:
        ap.error("pass article.html or --all-lireate")

    all_errors: List[str] = []
    per_file = {}
    for f in files:
        errs = audit_file(f)
        per_file[str(f)] = errs
        all_errors.extend(errs)

    report = {
        "files_checked": len(files),
        "violation_count": len(all_errors),
        "verdict": "pass" if not all_errors else "fail",
        "violations": all_errors,
        "by_file": per_file,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    if all_errors:
        for e in all_errors:
            print(e, file=sys.stderr)
    return 0 if not all_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
