"""JS to scale #composition to fill paper without stretching children."""

FIT_COMPOSITION_JS = """
() => {
  const paper = document.querySelector('[data-layout-paper]');
  const comp = document.getElementById('composition');
  if (!paper || !comp) return { ok: false, reason: 'missing paper or composition' };
  comp.style.transform = 'none';
  comp.style.width = 'max-content';
  comp.style.maxWidth = '100%';
  const margin = 24;
  const pr = paper.getBoundingClientRect();
  const cr = comp.getBoundingClientRect();
  const availW = pr.width - margin * 2;
  const availH = pr.height - margin * 2;
  if (cr.width < 1 || cr.height < 1) return { ok: false, reason: 'zero composition' };
  let scale = Math.min(availW / cr.width, availH / cr.height);
  const minFill = 0.92;
  if (cr.height * scale < availH * minFill) {
    scale = (availH * minFill) / cr.height;
  }
  scale = Math.min(scale, 1.35);
  const scaledW = cr.width * scale;
  const scaledH = cr.height * scale;
  const tx = margin + Math.max(0, (availW - scaledW) / 2);
  const ty = margin;
  comp.style.transformOrigin = 'top left';
  comp.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + scale + ')';
  return { ok: true, scale, scaledW, scaledH, availW, availH };
}
"""
