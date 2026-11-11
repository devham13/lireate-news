"""Sanitize common main.php patch accidents (stray quote after script tags)."""
import re

STRAY_SCRIPT_TAIL = re.compile(
    r'(<script defer src="/template/js/lireate-static-hero-lu\.js[^"]*"></script>)\s*"\s*/>\s*',
    re.I,
)

STRAY_ANY_SCRIPT_TAIL = re.compile(
    r"(</script>)\s*\"\s*/>\s*",
    re.I,
)


def sanitize_main_php_head(text: str) -> str:
    """Remove `\"></script>" />` tails from botched in-tag upgrades."""
    text = STRAY_SCRIPT_TAIL.sub(r"\1\n", text)
    text = STRAY_ANY_SCRIPT_TAIL.sub(r"\1\n", text)
    text = text.replace('</script>" />', "</script>\n")
    text = text.replace("</script>\" />", "</script>\n")
    return text
