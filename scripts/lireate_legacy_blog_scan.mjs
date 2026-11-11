#!/usr/bin/env node
/**
 * Статьи CMS: есть ли .lireate-blog-page внутри #articleBox (не строка из CSS в <head>).
 */
const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const sm = await fetch(`${site}/sitemap.xml`).then((r) => r.text());
const urls = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const legacy = [];
const modern = [];

for (const url of urls) {
  const p = new URL(url).pathname;
  if (!/\/[a-z0-9_-]+/i.test(p) || /^(news|patent|mktu|uslugi|team|docs)(\/|$)/.test(p.replace(/^\//, ""))) {
    continue;
  }
  const html = await fetch(url, { headers: { "Cache-Control": "no-cache" } })
    .then((r) => r.text())
    .catch(() => "");
  if (!html.includes("articleBox") && !html.includes("id=\"textBox\"")) continue;
  const inArticle = /id=["']articleBox["'][^>]*>[\s\S]{0,80000}class=["']lireate-blog-page/.test(html);
  if (inArticle) modern.push(p);
  else legacy.push({ path: p, dark: html.includes("lireate-legacy-article-lu") });
}

console.log(
  JSON.stringify({ legacyCount: legacy.length, modernCount: modern.length, legacy: legacy.slice(0, 80) }, null, 2),
);
