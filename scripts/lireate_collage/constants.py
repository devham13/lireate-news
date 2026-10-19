from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = REPO_ROOT / "memory" / "cover" / "collage-v1" / "assets"

NAVY = "#0b1020"
INK = "#111111"
PINK = "#ff2d78"
PINK_ALT = "#ff1f6b"
STICKY_PINK = "#ff8fc8"
STICKY_YELLOW = "#f7e58c"
GREEN = "#22c55e"
RED = "#ef4444"
PAPER = "#fafaf8"

COVER_OUT = (860, 400)
COVER_RENDER = (860, 400)
COVER_SMALL = (350, 163)
COVER_PREVIEW = (396, 300)

INLINE_OUT = (1200, 675)
INLINE_RENDER = (1200, 675)

FROZEN_TOPIC_IDS = frozenset({"L01", "L02", "L03", "L04", "L05"})

SLOT_FILES = {
    "inline_1": "inline-01.png",
    "inline_2": "inline-02.png",
    "inline_3": "inline-03.png",
}

GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Caveat:wght@500;600&family=Inter:wght@400;600;700;800&display=swap"
)
