#!/usr/bin/env node
import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";

const url = process.argv[2];
const outDir = process.argv[3];
let slug = process.argv[4] || "page";
try {
  const u = new URL(url);
  const parts = u.pathname.replace(/\/$/, "").split("/").filter(Boolean);
  const base = parts.length ? parts[parts.length - 1] : "home";
  if (slug === "page") slug = base;
} catch {
  /* keep slug */
}
if (!url || !outDir) process.exit(2);
await mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
for (const [name, w, h] of [
  ["375", 375, 812],
  ["1366", 1366, 900],
]) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  await page.goto(url, { waitUntil: "networkidle", timeout: 120000 });
  await page.waitForTimeout(2000);
  await page.screenshot({
    path: path.join(outDir, `${slug}-${name}.png`),
    fullPage: true,
  });
  await page.close();
}
await browser.close();
