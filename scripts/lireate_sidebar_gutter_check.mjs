#!/usr/bin/env node
import { chromium } from "playwright";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) process.exit(2);

const pages = ["/", "/patent", "/patent_prom_obr", "/mktu"];
const widths = [992, 1024, 1100, 1199, 1200, 1280];
let fail = 0;

const browser = await chromium.launch({ headless: true });
for (const path of pages) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 800 } });
    await page.goto(`${site}${path}?qa=${Date.now()}`, {
      waitUntil: "networkidle",
      timeout: 120000,
    });
    const rep = await page.evaluate(() => {
      const sb = document.getElementById("leftSideBar");
      const h1 = document.querySelector("h1");
      if (!h1) return { err: "no h1" };
      const sr = sb?.getBoundingClientRect();
      const hr = h1.getBoundingClientRect();
      const vis = !!(sr && sr.left >= -1 && sr.width > 40 && sr.right > 0);
      const ref = vis ? sr.right : 0;
      const gap = hr.left - ref;
      const vw = window.innerWidth;
      const leftPct = (hr.left / vw) * 100;
      const pl = getComputedStyle(document.querySelector(".container.content") || document.body)
        .paddingLeft;
      return {
        vis,
        sbRight: Math.round(ref),
        h1Left: Math.round(hr.left),
        gap: Math.round(gap),
        leftPct: Math.round(leftPct * 10) / 10,
        contPl: pl,
      };
    });
    const okGap = rep.vis ? rep.gap >= 16 && rep.gap <= 72 : rep.leftPct <= 8.5;
    const slug = path === "/" ? "home" : path.slice(1);
    console.log(JSON.stringify({ slug, w, ...rep, okGap }));
    if (rep.err || !okGap) fail = 1;
    await page.close();
  }
}
await browser.close();
process.exit(fail);
