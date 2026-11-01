"""Shrink cover headline until it fits its column (Playwright evaluate)."""

HEADLINE_FIT_JS = """
() => {
  const hl = document.querySelector('[data-layout-slot="slot-headline"]');
  const safe = document.querySelector('[data-thumbnail-safe="1"]');
  if (!hl) return { ok: false, reason: 'no headline' };
  const col = hl.closest('.col-headline') || hl.parentElement;
  const colRect = col ? col.getBoundingClientRect() : hl.getBoundingClientRect();
  const safeRect = safe ? safe.getBoundingClientRect() : colRect;
  const pad = 4;
  const maxW = Math.min(colRect.width, safeRect.width) - pad;
  const maxH = Math.min(colRect.height, safeRect.height) - pad;
  let size = parseFloat(window.getComputedStyle(hl).fontSize) || 48;
  hl.style.fontSize = size + 'px';
  hl.style.maxWidth = maxW + 'px';
  for (let i = 0; i < 48 && size > 20; i++) {
    const r = hl.getBoundingClientRect();
    if (r.width <= maxW + 1 && r.height <= maxH + 1
        && r.bottom <= safeRect.bottom - pad + 0.5
        && r.top >= safeRect.top + pad - 0.5) break;
    size -= 1.25;
    hl.style.fontSize = size + 'px';
  }
  return { ok: true, fontSize: size, w: hl.getBoundingClientRect().width, h: hl.getBoundingClientRect().height };
}
"""
