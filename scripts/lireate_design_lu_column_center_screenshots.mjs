#!/usr/bin/env node
import { chromium } from "playwright";
import { mkdir, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}
const outDir = process.env.LIREATE_SCREENSHOT_DIR || "/opt/cursor/artifacts/lu-column-center-20261111";
const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const viewportCss = await readFile(join(root, "hosting-design/template/css/lireate-lu-viewport.css"), "utf8");
const cmsLuCss = await readFile(join(root, "hosting-design/template/css/lireate-cms-lu.css"), "utf8");
const mktuCss = await readFile(join(root, "hosting-design/template/css/lireate-mktu-lu.css"), "utf8");
const homeLuCss = await readFile(join(root, "hosting-design/template/page/home/lireate-home-lu.css"), "utf8");
const fixCss = [viewportCss, cmsLuCss, mktuCss, homeLuCss].join("\n");

const pages = [
  { path: "/", slug: "home" },
  { path: "/mktu/", slug: "mktu" },
];
const widths = [1366, 1920];

await mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

for (const { path, slug } of pages) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(`${site}${path}?qa=${Date.now()}`, { waitUntil: "domcontentloaded", timeout: 120000 });
    await page.waitForTimeout(500);
    await page.screenshot({ path: join(outDir, `${slug}-${w}-before.png`), fullPage: false });
    await page.addStyleTag({ content: fixCss });
    await page.waitForTimeout(300);
    await page.screenshot({ path: join(outDir, `${slug}-${w}-after.png`), fullPage: false });
    console.log("WROTE", slug, w, "before+after");
    await page.close();
  }
}
await browser.close();
