#!/usr/bin/env node
import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
const out = process.argv[2] || "/opt/cursor/artifacts/design-viewport-qa-20261111";
const pages = [
  { path: "/", slug: "home" },
  { path: "/patent", slug: "patent" },
  { path: "/patent_prom_obr", slug: "patent_prom_obr" },
  { path: "/mktu", slug: "mktu" },
];
const widths = [375, 768, 1024, 1280, 1366, 1920];
if (!site) process.exit(2);
await mkdir(out, { recursive: true });
const browser = await chromium.launch({ headless: true });
for (const { path: p, slug } of pages) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(`${site}${p}?qa=${Date.now()}`, { waitUntil: "networkidle", timeout: 120000 });
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(out, `${slug}-${w}.png`), fullPage: true });
    await page.close();
  }
}
await browser.close();
