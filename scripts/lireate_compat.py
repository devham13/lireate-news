"""Python 3.6+ helpers for Lireate scripts (stdlib only)."""

import sys


def require_python(min_version=(3, 6)):
    if sys.version_info < min_version:
        sys.stderr.write(
            "ERROR: Python {0}.{1}+ required, got {2}\n".format(
                min_version[0], min_version[1], sys.version.split()[0]
            )
        )
        sys.exit(2)


def http_response_code(resp):
    """HTTP status from urlopen response (3.6 uses getcode())."""
    return getattr(resp, "status", None) or resp.getcode()


def header_charset(headers):
    if headers is None:
        return None
    getter = getattr(headers, "get_content_charset", None)
    if callable(getter):
        try:
            return getter()
        except Exception:
            pass
    ctype = headers.get("Content-Type") or headers.get("content-type") or ""
    if "charset=" in ctype.lower():
        return ctype.lower().split("charset=", 1)[-1].split(";")[0].strip()
    return None
