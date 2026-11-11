#!/usr/bin/env python3
"""Assert dock v2 emits URI_LEGACY with mktu1? in head, footer, and body blocks."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "dock",
    ROOT / "scripts" / "lireate_design_patch_service_mobile_dock.py",
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

blob = mod.HEAD_BLOCK + mod.FOOTER_BLOCK + mod.BODY_SNIP.replace("\n", " ")
if blob.count("mktu1?") < 3:
    print("FAIL: expected mktu1? in 3 dock blocks, got", blob.count("mktu1?"), file=sys.stderr)
    raise SystemExit(1)
if mod.URI_LEGACY_REGEX_OLD in blob:
    print("FAIL: old URI regex still in v2 blocks", file=sys.stderr)
    raise SystemExit(1)
print("URI_REGEX_CHECK_OK")


if __name__ == "__main__":
    main = sys.modules[__name__]
    # no-op
