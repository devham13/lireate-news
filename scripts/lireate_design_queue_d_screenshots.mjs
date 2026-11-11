#!/usr/bin/env node
/** Скриншоты очереди D: ключевые URL на 375/1024/1280/1920 */
import { chromium } from "playwright";
import path from "path";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
const outDir = process.env.LIREATE_SCREENSHOT_DIR || "/opt/cursor/artifacts/queue-d-20261111";
if (!site) process.exit(2);

const urls = [
  "/",
  "/patent/",
  "/patent_prom_obr/",
  "/mktu/",
  "/reviews/",
  "/portfolio/",
  "/spasibo/",
  "/uslugi/",
  "/patent_na_poleznuyu_model_rospatent/",
  "/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta/",
];
const widths = [375, 1024, 1280, 1920];

import fs from "fs";
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
for (const url of urls) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: w < 500 ? 812 : 900 } });
    const full = `${site}${url}?qa=${Date.now()}`;
    await page.goto(full, { waitUntil: "domcontentloaded", timeout: 90000 });
    await page.waitForTimeout(800);
    const dark = await page.evaluate(() => document.body.classList.contains("lireate-cms-page-dark"));
    const overlap = await page.evaluate(() => {
      const w = document.getElementById("floatingBlock");
      if (!w || w.classList.contains("lx-widget-hidden")) return false;
      const r = w.getBoundingClientRect();
      const el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      return !!(el && !w.contains(el) && el.id !== "manager_icon");
    });
    const slug = url.replace(/\//g, "_").replace(/^_/, "") || "home";
    const file = `${slug}-w${w}.png`;
    await page.screenshot({ path: path.join(outDir, file), fullPage: w >= 1280 });
    results.push({ url, width: w, dark, widgetOverlap: overlap, file });
    await page.close();
  }
}
await browser.close();
fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify(results, null, 2));
console.log(JSON.stringify({ outDir, count: results.length, bad: results.filter((r) => !r.dark || r.widgetOverlap) }, null, 2));
