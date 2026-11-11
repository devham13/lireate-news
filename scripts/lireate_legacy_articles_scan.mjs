#!/usr/bin/env node
/**
 * Скан: URL из sitemap без .lireate-blog-page (старый шаблон).
 */
import { chromium } from "playwright";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const sm = await fetch(`${site}/sitemap.xml`).then((r) => r.text());
const urls = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)]
  .map((m) => m[1])
  .filter((u) => {
    try {
      const p = new URL(u).pathname;
      return (
        p.length > 2 &&
        !/^\/(news|patent|mktu|uslugi|avtor|kontaktyi|team|partners|docs)(\/|$)/.test(p)
      );
    } catch {
      return false;
    }
  });

const browser = await chromium.launch({ headless: true });
const legacy = [];
const modern = [];
for (const url of urls.slice(0, 200)) {
  const page = await browser.newPage();
  try {
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    const kind = await page.evaluate(() => {
      if (document.querySelector("#articleBox .lireate-blog-page")) return "blog";
      if (document.querySelector(".main-screen, #main_back")) return "legacy-hero";
      if (document.querySelector(".product")) return "legacy-product";
      return "other";
    });
    const path = new URL(url).pathname;
    if (kind === "blog") modern.push(path);
    else legacy.push({ path, kind });
  } catch {
    legacy.push({ path: new URL(url).pathname, kind: "error" });
  }
  await page.close();
}
await browser.close();
console.log(JSON.stringify({ total: urls.length, scanned: Math.min(urls.length, 200), legacy: legacy.slice(0, 80), modernCount: modern.length, legacyCount: legacy.length }, null, 2));
