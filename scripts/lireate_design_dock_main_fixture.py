#!/usr/bin/env python3
"""Build tests/fixtures/main-php-v117-service-dock-v1.php (padded, php -l safe)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_V1 = ROOT / "tests" / "fixtures" / "main-php-v117-service-dock-v1.php"
OUT_V2_DRIFT = ROOT / "tests" / "fixtures" / "main-php-v120-dock-v2-body-drift.php"

spec = importlib.util.spec_from_file_location(
    "lireate_dock_patch",
    ROOT / "scripts" / "lireate_design_patch_service_mobile_dock.py",
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)
V1_BODY = mod.V1_BODY_SNIP.replace("\n", " ")

MIN_LINES = 6100


def _pad(text: str, path: Path) -> None:
    lines = text.splitlines(keepends=True)
    pad = MIN_LINES - len(lines)
    if pad > 0:
        lines.extend(f"<!-- fixture-pad-{i} -->\n" for i in range(pad))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")
    print("FIXTURE_OK", path, len(lines))


def main() -> None:
    v1_body = (
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
    _pad(v1_body, OUT_V1)

    # Production failure mode: dock v2 marker before static/news/home snippets on one line.
    v2_compact = mod.BODY_SNIP.replace("\n", " ").replace(
        mod.STANDALONE_REGEX_NEW_TAIL, mod.STANDALONE_REGEX_OLD_TAIL, 1
    )
    v2_body = (
        "<?php\n"
        "// page_container\n"
        "$temp = array('page' => 'home');\n"
        "?>\n"
        "<html><head></head><body class=\"cms-default<?php "
        "/* lireate_cms_dark_body_v1 */ "
        "if (in_array($temp['page'], array('home','patent','patent_prom_obr','mktu','mktu1'), true)) "
        "echo ' lireate-cms-page-dark'; "
        f"{v2_compact} "
        "/* lireate_design_static_lu_v1 */ if($temp['page']=='uslugi') echo ' lireate-uslugi-body'; "
        "/* lireate_design_news_lu_v1 */ if($temp['page']=='news') echo ' lireate-news-lu-body'; "
        "/* lireate_design_legacy_cms_services_v1 body */ "
        "echo ' lireate-legacy-cms-lu-marker'; "
        " if ($temp['page']==='home') echo ' lireate-home-dark';"
        '?>\">\n'
        "<main>Fixture v2 drift</main>\n"
        "</body></html>\n"
    )
    _pad(v2_body, OUT_V2_DRIFT)


if __name__ == "__main__":
    main()
