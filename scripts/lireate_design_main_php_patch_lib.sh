#!/usr/bin/env bash
# Atomic main.php patching: work copy → guard/php -l → mv; rollback on failure.
# shellcheck source=scripts/lireate_main_php_guard.sh

lireate_design_rollback_main() {
  local main="${1:?}"
  local pre="${main}.pre-design-patch"
  local bak_suffix="${2:-bak-2026-11-11-design}"
  local bak="${main}.${bak_suffix}"
  if [[ -f "$pre" ]]; then
    cp -a "$pre" "$main"
  elif [[ -f "$bak" ]]; then
    cp -a "$bak" "$main"
  else
    echo "MAIN_ROLLBACK_SKIP: no pre/bak for $main" >&2
    return 1
  fi
  if declare -f lireate_main_php_touch >/dev/null 2>&1; then
    lireate_main_php_touch "$main"
  else
    touch "$main"
  fi
  echo "MAIN_ROLLBACK_OK" >&2
  return 0
}

# Usage: lireate_design_patch_main_php WORK_MAIN PATCH_PY [LABEL]
lireate_design_patch_main_php() {
  local main="${1:?}"
  local patch_py="${2:?}"
  local label="${3:-main}"
  local py="${LIREATE_DESIGN_PYTHON:-python3}"
  local work="${main}.patch-work"

  if [[ ! -f "$main" ]]; then
    echo "MAIN_PATCH_FAIL: missing $main" >&2
    return 1
  fi
  if ! lireate_main_php_guard "$main"; then
    echo "MAIN_GUARD_PRE_FAIL ${label}" >&2
    return 1
  fi

  local bak_suffix="${LIREATE_DESIGN_BAK_SUFFIX:-bak-2026-11-11-design}"
  if [[ -f "$main" ]]; then
    cp -a "$main" "${main}.${bak_suffix}"
  fi
  cp -a "$main" "${main}.pre-design-patch"
  cp -a "$main" "$work"

  if ! "$py" "$patch_py" "$work"; then
    echo "${label}_PATCH_PY_FAIL" >&2
    lireate_design_rollback_main "$main" "$bak_suffix" || true
    rm -f "$work"
    return 1
  fi
  local marker_guard="${LIREATE_DESIGN_MARKER_GUARD:-${REPO:-}/scripts/lireate_design_main_php_marker_guard.py}"
  if [[ -n "${REPO:-}" && -f "$marker_guard" ]]; then
    if ! "$py" "$marker_guard" "${main}.pre-design-patch" "$work"; then
      echo "MAIN_MARKER_GUARD_FAIL ${label}" >&2
      lireate_design_rollback_main "$main" "$bak_suffix" || true
      rm -f "$work"
      return 1
    fi
  fi
  if [[ -f "$REPO/scripts/lireate_design_main_php_sanitize_cli.py" ]]; then
  if ! "$py" "$REPO/scripts/lireate_design_main_php_sanitize_cli.py" "$work"; then
    echo "MAIN_PHP_SANITIZE_FAIL ${label}" >&2
    lireate_design_rollback_main "$main" "$bak_suffix" || true
    rm -f "$work"
    return 1
  fi
  fi
  if ! php -l "$work" >/dev/null 2>&1; then
    echo "MAIN_PHP_LINT_FAIL ${label}" >&2
    lireate_design_rollback_main "$main" "$bak_suffix" || true
    rm -f "$work"
    return 1
  fi
  if ! lireate_main_php_guard "$work"; then
    echo "MAIN_GUARD_POST_FAIL ${label}" >&2
    lireate_design_rollback_main "$main" "$bak_suffix" || true
    rm -f "$work"
    return 1
  fi

  mv -f "$work" "$main"
  lireate_main_php_touch "$main"
  echo "MAIN_PATCH_OK ${label}" >&2
  return 0
}
