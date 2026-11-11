#!/usr/bin/env node
/** Unique img/src on sitemap pages with HTTP >= 400 (concurrent, py3.6-safe fetch). */
const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) process.exit(2);

const pageLimit = Number(process.env.LIREATE_IMG_SCAN_PAGES || "80");
const concurrency = Number(process.env.LIREATE_IMG_SCAN_CONCURRENCY || "8");

const sm = await fetch(`${site}/sitemap.xml`).then((r) => r.text());
const pageUrls = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]).slice(0, pageLimit);

const broken = new Map();

async function checkPage(pageUrl) {
  const html = await fetch(pageUrl, { headers: { "Cache-Control": "no-cache" } })
    .then((r) => r.text())
    .catch(() => "");
  const srcs = [
    ...html.matchAll(/(?:src|href)=["']([^"']+\.(?:png|jpg|jpeg|gif|webp|svg))[^"']*["']/gi),
  ].map((m) => m[1]);
  for (let src of srcs) {
    if (src.startsWith("data:")) continue;
    const abs = src.startsWith("http") ? src : new URL(src, pageUrl).href;
    if (!abs.startsWith(site)) continue;
    if (broken.has(abs)) continue;
    const st = await fetch(abs, { method: "HEAD" })
      .then((r) => r.status)
      .catch(() => 0);
    if (st >= 400 || st === 0) {
      broken.set(abs, { status: st, from: new URL(pageUrl).pathname });
    }
  }
}

let i = 0;
async function worker() {
  while (i < pageUrls.length) {
    const idx = i++;
    await checkPage(pageUrls[idx]);
  }
}
await Promise.all(Array.from({ length: concurrency }, () => worker()));

const list = [...broken.entries()].map(([img, meta]) => ({ img, ...meta }));
const out = { scannedPages: pageUrls.length, brokenCount: list.length, broken: list };
console.log(JSON.stringify(out, null, 2));
if (process.env.LIREATE_IMG_REPORT_PATH) {
  await import("node:fs").then((fs) =>
    fs.promises.writeFile(process.env.LIREATE_IMG_REPORT_PATH, JSON.stringify(out, null, 2)),
  );
}
