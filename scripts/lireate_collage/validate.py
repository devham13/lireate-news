import re


def _len(s):
    return len((s or "").strip())


def truncate(s, max_len):
    s = (s or "").strip()
    if _len(s) <= max_len:
        return s
    return s[: max_len - 1].rstrip() + "…"


def validate_cover_spec(spec):
    errors = []
    lines = spec.get("headline_lines") or []
    if not lines or sum(len(x) for x in lines) < 8:
        errors.append("headline too short")
    if len(lines) > 4:
        errors.append("headline max 4 lines")
    for line in lines:
        if len(line) > 42:
            errors.append("headline line too long: {0}".format(line[:20]))
    hl = spec.get("highlight") or ""
    if hl and hl not in " ".join(lines):
        errors.append("highlight not in headline")
    sticky = spec.get("sticky_text") or ""
    if _len(sticky) > 48:
        errors.append("sticky too long")
    return errors


def validate_inline_item(item):
    errors = []
    if _len(item.get("headline")) > 120:
        errors.append("headline too long")
    tmpl = item.get("template")
    if tmpl == "bad_good":
        if not item.get("bad") or not item.get("good"):
            errors.append("bad_good needs bad and good")
    elif tmpl == "process":
        steps = item.get("steps") or []
        if len(steps) < 2:
            errors.append("process needs 2+ steps")
    elif tmpl == "checklist":
        rows = item.get("checklist_rows") or []
        if len(rows) < 4:
            errors.append("checklist needs 4+ rows")
    else:
        errors.append("unknown template")
    conc = item.get("conclusion") or {}
    if not conc.get("box_lines"):
        errors.append("conclusion.box_lines required")
    return errors


_CYR_RE = re.compile(r"[\u0400-\u04FF]")


def has_cyrillic(text):
    return bool(_CYR_RE.search(text or ""))
