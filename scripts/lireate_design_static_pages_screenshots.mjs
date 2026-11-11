#!/usr/bin/env node
import { chromium } from "playwright";
import { mkdir, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
const outDir = process.env.LIREATE_SCREENSHOT_DIR || "/opt/cursor/artifacts/static-pages-contrast-20261111";
const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const paths = ["/spasibo/", "/portfolio/", "/reviews/"];
const widths = [375, 1024, 1280];

const css = await readFile(join(root, "hosting-design/template/css/lireate-static-pages-lu.css"), "utf8");
const js = await readFile(join(root, "hosting-design/template/js/lireate-static-hero-lu.js"), "utf8");

await mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

for (const path of paths) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(site + path, { waitUntil: "domcontentloaded", timeout: 90000 });
    await page.addStyleTag({ content: css });
    await page.evaluate(js);
    await page.waitForTimeout(300);
    const name = path.replace(/\//g, "_").replace(/^_|_$/g, "") || "root";
    const file = `${outDir}/${name}-${w}.png`;
    await page.screenshot({ path: file, fullPage: false });
    console.log("WROTE", file);
    await page.close();
  }
}
await browser.close();
