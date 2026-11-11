#!/usr/bin/env python3
"""Optional hero div patches — always reattaches tail after page block."""
import sys
from pathlib import Path

MIN_LINES = 5000
HERO_ATTR = 'class="row main-screen main_back" id="main_back"'


def _validate(text: str, label: str) -> None:
    n = text.count("\n") + (0 if text.endswith("\n") else 1)
    if n < MIN_LINES:
        raise SystemExit(f"{label}: line count {n} < {MIN_LINES}")
    if "page_container" not in text:
        raise SystemExit(f"{label}: page_container missing")


def patch_block(text: str, anchor: str) -> str:
    pos = text.find(anchor)
    if pos == -1:
        return text
    next_pos = text.find("<?php if($temp['page']", pos + len(anchor))
    if next_pos == -1:
        return text
    head, segment, tail = text[:pos], text[pos:next_pos], text[next_pos:]
    if "main-screen main_back" in segment:
        return text
    for hero_old in (
        '        \t<div class="row main-screen" style="margin: 0;">',
        '\t\t\t<div class="row main-screen" style="margin: 0;">',
    ):
        if hero_old in segment:
            hero_new = hero_old.replace(
                'class="row main-screen"',
                HERO_ATTR,
                1,
            )
            segment = segment.replace(hero_old, hero_new, 1)
            out = head + segment + tail
            _validate(out, "patch_block")
            return out
    return text


def main() -> None:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8", errors="replace")
    _validate(text, "input")
    for anchor in (
        "\t\t<?php if($temp['page']=='home'):?>",
        "\t\t<?php if($temp['page']=='patent'):?>",
        "\t\t<?php if($temp['page']=='patent_prom_obr'):?>",
    ):
        text = patch_block(text, anchor)
    _validate(text, "output")
    tmp = path.with_suffix(path.suffix + ".hero-tmp")
    tmp.write_text(text, encoding="utf-8")
    _validate(tmp.read_text(encoding="utf-8", errors="replace"), "tmp")
    tmp.replace(path)
    print("OK", text.count("\n"))


if __name__ == "__main__":
    main()
