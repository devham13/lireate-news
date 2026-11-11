#!/usr/bin/env node
import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
const outDir = process.argv[2] || "/opt/cursor/artifacts/design-modals-20261111";
if (!site) process.exit(2);
await mkdir(outDir, { recursive: true });

const triggers = [
  { id: "tz_but", name: "home-modal-tz" },
  { id: "pat_but", name: "home-modal-patent" },
  { id: "dog_but", name: "home-modal-dogovory" },
  { id: "pro_but", name: "home-modal-po" },
];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto(`${site}/?qa=${Date.now()}`, { waitUntil: "networkidle", timeout: 120000 });

for (const t of triggers) {
  const btn = page.locator(`#${t.id}`);
  if ((await btn.count()) === 0) continue;
  await btn.click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, `${t.name}-1280.png`), fullPage: false });
  await page.evaluate(() => {
    window.jQuery?.(".modal.in").modal("hide");
    document.querySelectorAll(".modal-backdrop").forEach((el) => el.remove());
  });
  await page.waitForTimeout(300);
}

const consult = page.locator(".lireate-hero-v4__btn--primary").first();
if (await consult.count()) {
  await consult.click();
  await page.waitForTimeout(600);
  await page.screenshot({
    path: path.join(outDir, "home-modal-callback-1280.png"),
    fullPage: false,
  });
}
await browser.close();
