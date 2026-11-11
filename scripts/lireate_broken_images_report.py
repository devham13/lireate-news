#!/usr/bin/env python3
"""List unique 404 image URLs from lireate access log (hosting)."""
import re
import sys
from collections import Counter
from pathlib import Path

LOG = Path(sys.argv[1] if len(sys.argv) > 1 else "~/logs/site.access.log")
pat = re.compile(r'GET (\S+) HTTP.*" 404 ')
urls = Counter()
if not LOG.is_file():
    print("LOG_MISSING", LOG, file=sys.stderr)
    raise SystemExit(1)
for line in LOG.open(errors="replace"):
    m = pat.search(line)
    if not m:
        continue
    u = m.group(1)
    if "/images/" in u or "/template/images/" in u:
        urls[u] += 1
for u, n in urls.most_common():
    print(f"{n}\t{u}")
print(f"# unique={len(urls)} total_hits={sum(urls.values())}", file=sys.stderr)
