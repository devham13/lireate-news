#!/usr/bin/env bash
# Pick Python ≥3.8 for design patches (hosting python3 is often 3.6).
lireate_design_resolve_python() {
  local c ver
  for c in python3.12 python3.11 python3.10 python3.9 python3.8 python3; do
    if command -v "$c" >/dev/null 2>&1; then
      ver="$("$c" -c 'import sys; print(1 if sys.version_info >= (3, 8) else 0)' 2>/dev/null || echo 0)"
      if [[ "$ver" == "1" ]]; then
        echo "$c"
        return 0
      fi
    fi
  done
  echo "python3"
  return 0
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  lireate_design_resolve_python
fi
