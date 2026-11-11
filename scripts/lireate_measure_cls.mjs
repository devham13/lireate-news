#!/usr/bin/env node
/**
 * Playwright CLS + screenshots (375 / 1366).
 * Usage: node scripts/lireate_measure_cls.mjs <url> <outDir> [--label before|after]
 */
import { chromium, devices } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const url = process.argv[2];
const outDir = process.argv[3];
const label = process.argv.includes("--after") ? "after" : "before";

if (!url || !outDir) {
  console.error(
    "Usage: node lireate_measure_cls.mjs <url> <outDir> [--before|--after]",
  );
  process.exit(2);
}

await mkdir(outDir, { recursive: true });

async function runViewport(name, viewport, slug) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    ...devices["Desktop Chrome"],
    viewport,
    locale: "ru-RU",
  });
  const page = await context.newPage();
  let cls = 0;
  await page.addInitScript(() => {
    window.__cls = 0;
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) window.__cls += entry.value;
      }
    }).observe({ type: "layout-shift", buffered: true });
  });
  await page.goto(url, { waitUntil: "networkidle", timeout: 120000 });
  await page.waitForTimeout(2500);
  cls = await page.evaluate(() => window.__cls || 0);
  const shot = path.join(outDir, `${slug}-${label}-${name}.png`);
  await page.screenshot({ path: shot, fullPage: true });
  await browser.close();
  return { viewport: name, cls, shot };
}

const v375 = { width: 375, height: 812 };
const v1366 = { width: 1366, height: 900 };
const slug = new URL(url).pathname.replace(/\//g, "_") || "home";

const results = [
  await runViewport("375", v375, slug),
  await runViewport("1366", v1366, slug),
];

const report = { url, label, at: new Date().toISOString(), results };
await writeFile(
  path.join(outDir, `${slug}-cls-${label}.json`),
  JSON.stringify(report, null, 2),
);
console.log(JSON.stringify(report, null, 2));
