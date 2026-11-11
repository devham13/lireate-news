#!/usr/bin/env node
/** Скан live URL из sitemap на служебные пометки в HTML. */
const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) process.exit(2);
const markers = [
  /MCP\s+недоступен/i,
  /среде\s+подготовки/i,
  /среде\s+исследования/i,
  /research-notes/i,
  /\bTODO\b/,
  /\bFIXME\b/,
];
const sm = await fetch(`${site}/sitemap.xml`).then((r) => r.text());
const urls = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const hits = [];
for (const url of urls) {
  const html = await fetch(url).then((r) => r.text()).catch(() => "");
  if (!html) continue;
  const text = html.replace(/<script[\s\S]*?<\/script>/gi, "").replace(/<[^>]+>/g, " ");
  for (const rx of markers) {
    if (rx.test(text)) {
      hits.push({ url: new URL(url).pathname, marker: rx.source });
      break;
    }
  }
}
console.log(JSON.stringify({ scanned: urls.length, hits }, null, 2));
