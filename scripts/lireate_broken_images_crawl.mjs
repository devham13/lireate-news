#!/usr/bin/env node
/** Уникальные img src на sitemap с HTTP >= 400 */
const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) process.exit(2);
const sm = await fetch(`${site}/sitemap.xml`).then((r) => r.text());
const pageUrls = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]).slice(0, 120);
const broken = new Map();
for (const pageUrl of pageUrls) {
  const html = await fetch(pageUrl).then((r) => r.text()).catch(() => "");
  const srcs = [...html.matchAll(/(?:src|href)=["']([^"']+\.(?:png|jpg|jpeg|gif|webp|svg))[^"']*["']/gi)].map((m) => m[1]);
  for (let src of srcs) {
    if (src.startsWith("data:")) continue;
    const abs = src.startsWith("http") ? src : new URL(src, pageUrl).href;
    if (!abs.includes(site.replace(/\/$/, ""))) continue;
    const key = abs;
    if (broken.has(key)) continue;
    const st = await fetch(abs, { method: "HEAD" }).then((r) => r.status).catch(() => 0);
    if (st >= 400 || st === 0) broken.set(key, { status: st, from: new URL(pageUrl).pathname });
  }
}
const list = [...broken.entries()].map(([img, meta]) => ({ img, ...meta }));
console.log(JSON.stringify({ scannedPages: pageUrls.length, brokenCount: list.length, broken: list.slice(0, 120) }, null, 2));
