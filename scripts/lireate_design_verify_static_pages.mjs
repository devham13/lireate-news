#!/usr/bin/env node
/** reviews / portfolio / spasibo: dark body classes, 1 h1, no hero overlap at 375/1024/1280 (DOM) */
import { chromium } from "playwright";

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const paths = ["/reviews/", "/portfolio/", "/spasibo/"];
const widths = [375, 1024, 1280];
const browser = await chromium.launch({ headless: true });
let fail = 0;

for (const path of paths) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(site + path, { waitUntil: "domcontentloaded", timeout: 60000 });
    const data = await page.evaluate(() => {
      const body = document.body;
      const h1 = document.querySelectorAll("h1").length;
      const dark =
        body.classList.contains("lireate-cms-page-dark") &&
        (body.classList.contains("lireate-reviews-body") ||
          body.classList.contains("lireate-portfolio-body") ||
          body.classList.contains("lireate-spasibo-body"));
      const hero = document.querySelector(".main-screen.main_back:not(.lireate-hero-v4)");
      const heroVisible = hero && hero.getBoundingClientRect().height > 8;
      const bar = document.querySelectorAll(".lx-mobile-bar").length;
      const h2 = document.querySelectorAll("h2").length;
      return { h1, h2, dark, heroVisible, bar, cls: body.className };
    });
    const headingOk = data.h1 === 1 || (path === "/spasibo/" && data.h1 === 0 && data.h2 >= 1);
    const ok = headingOk && data.dark && !data.heroVisible;
    console.log(ok ? "OK" : "FAIL", path, w, data);
    if (!ok) fail++;
    await page.close();
  }
}
await browser.close();
process.exit(fail ? 1 : 0);
