#!/usr/bin/env python3
"""Build tests/fixtures/main-php-v117-service-dock-v1.php (padded, php -l safe)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "fixtures" / "main-php-v117-service-dock-v1.php"

spec = importlib.util.spec_from_file_location(
    "lireate_dock_patch",
    ROOT / "scripts" / "lireate_design_patch_service_mobile_dock.py",
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)
V1_BODY = mod.V1_BODY_SNIP.replace("\n", " ")

MIN_LINES = 6100


def main() -> None:
    body = (
        "<?php\n"
        "// page_container\n"
        "$temp = array('page' => 'patent');\n"
        "?>\n"
        "<html><head></head><body class=\"cms-default<?php "
        "/* lireate_cms_dark_body_v1 */ "
        "if (in_array($temp['page'], array('home','patent','patent_prom_obr','mktu','mktu1'), true)) "
        "echo ' lireate-cms-page-dark'; "
        "if ($temp['page']==='home') echo ' lireate-home-dark';"
        f"{V1_BODY}"
        '?>\">\n'
        "<main>Fixture</main>\n"
        "\t<?php /* lireate_site_footer_v1 */ ?>\n"
        "</body></html>\n"
    )
    lines = body.splitlines(keepends=True)
    pad = MIN_LINES - len(lines)
    if pad > 0:
        lines.extend(f"<!-- fixture-pad-{i} -->\n" for i in range(pad))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print("FIXTURE_OK", OUT, len(lines))


if __name__ == "__main__":
    main()
