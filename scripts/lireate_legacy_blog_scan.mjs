#!/usr/bin/env node
/** Статьи без .lireate-blog-page (очередь D) */
const site = process.env.LIREATE_PUBLIC_SITE_URL;
const sm = await fetch(`${site}/sitemap.xml`).then((r) => r.text());
const urls = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const legacy = [];
const modern = [];
for (const url of urls) {
  const p = new URL(url).pathname;
  if (!/\/[a-z0-9_-]+/i.test(p) || /^(news|patent|mktu|uslugi|team|docs)/.test(p.replace(/^\//, ""))) continue;
  const html = await fetch(url).then((r) => r.text()).catch(() => "");
  if (!html.includes("news") && !html.includes("articleBox")) continue;
  if (html.includes("lireate-blog-page")) modern.push(p);
  else if (html.includes("main_back") || html.includes("imgBlock")) legacy.push({ path: p, dark: html.includes("lireate-cms-page-dark") });
}
console.log(JSON.stringify({ legacyCount: legacy.length, modernCount: modern.length, legacy: legacy.slice(0, 80) }, null, 2));
