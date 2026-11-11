#!/usr/bin/env node
import { chromium } from "playwright";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const pages = [
  { path: "/", slug: "home", expect: 302, tol: 12 },
  { path: "/patent", slug: "patent", expect: 302, tol: 16 },
  { path: "/patent_prom_obr", slug: "patent_prom_obr", expect: 302, tol: 16 },
  { path: "/mktu", slug: "mktu", expect: 302, tol: 16 },
];

function failMsg(slug, detail) {
  console.error(`${slug}: ${detail}`);
  return 1;
}

let fail = 0;
const browser = await chromium.launch({ headless: true });
for (const { path, slug, expect, tol } of pages) {
  for (const w of [375, 1366]) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(`${site}${path}?qa=${Date.now()}`, {
      waitUntil: "networkidle",
      timeout: 120000,
    });
    const rep = await page.evaluate(({ expect, tol, w }) => {
      const menu = document.getElementById("leftSideBar");
      const mr = menu && menu.getBoundingClientRect().width > 50 ? menu.getBoundingClientRect().right : 0;
      const ref = w >= 1150 ? expect : 20;
      const pick = [
        ...document.querySelectorAll("h1, h2, h3.title, .advant, .block_contact, .lireate-hero-v4__head"),
      ].filter((el) => {
        const r = el.getBoundingClientRect();
        return r.width > 40 && r.height > 8;
      });
      const xs = pick.map((el) => Math.round(el.getBoundingClientRect().left));
      const unique = [...new Set(xs)].sort((a, b) => a - b);
      const spread = unique.length ? unique[unique.length - 1] - unique[0] : 0;
      const overflow = [];
      document.querySelectorAll(".advant, .block_contact").forEach((el) => {
        const sw = el.scrollWidth;
        const cw = el.clientWidth;
        if (sw > cw + 1) overflow.push({ cls: el.className.slice(0, 40), sw, cw });
      });
      const hero = document.querySelector(".lireate-hero-v4__facts");
      const facts = hero
        ? getComputedStyle(hero).display
        : "n/a";
      return { w, mr, ref, xs: unique.slice(0, 8), spread, overflow, facts, inter: /Inter/i.test(getComputedStyle(document.body).fontFamily) };
    }, { expect, tol, w });
    const okX =
      w < 1150
        ? true
        : rep.xs.length === 0 || rep.xs.every((x) => Math.abs(x - ref) <= tol);
    console.log(JSON.stringify({ slug, ...rep, okX }));
    if (!okX || rep.overflow.length) fail = 1;
    await page.close();
  }
}
await browser.close();
process.exit(fail);
