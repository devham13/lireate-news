#!/usr/bin/env node
/** 4 legacy CMS URIs: body.lireate-legacy-cms-lu + dark page bg, no bare pagekey digit. */
import { chromium } from "playwright";

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const paths = [
  "/poisk_tovarnyh_znakov/",
  "/ekspertiza_tovarnogo_znaka/",
  "/mezhdunarodnaja_registracija_tovarnogo_znaka/",
  "/registracija_torgovyh_marok_i_logotipov/",
];

function luminance(rgb) {
  const [r, g, b] = rgb;
  return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
}

function parseRgb(color) {
  const m = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return null;
  return [Number(m[1]), Number(m[2]), Number(m[3])];
}

const browser = await chromium.launch({ headless: true });
let fail = 0;

for (const path of paths) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const res = await page.goto(site + path, { waitUntil: "domcontentloaded", timeout: 60000 });
  const data = await page.evaluate(() => {
    const body = document.body;
    const cls = body ? body.className : "";
    const bg = body ? getComputedStyle(body).backgroundColor : "";
    const legacyCss = !!document.querySelector('link[href*="lireate-legacy-cms-lu.css"]');
    let strayPagekey = false;
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = tw.nextNode())) {
      const t = (node.textContent || "").trim();
      if (/^\d{1,3}$/.test(t) && node.parentElement === document.body) {
        strayPagekey = true;
        break;
      }
    }
    const h1 = document.querySelectorAll("h1").length;
    return { cls, bg, legacyCss, strayPagekey, h1 };
  }, path);
  const rgb = parseRgb(data.bg);
  const darkOk = rgb ? luminance(rgb) < 0.35 : false;
  const legacyBody = data.cls.includes("lireate-legacy-cms-lu");
  const darkClass = data.cls.includes("lireate-cms-page-dark");
  const ok =
    res?.status() === 200 &&
    data.h1 === 1 &&
    data.legacyCss &&
    legacyBody &&
    darkClass &&
    darkOk &&
    !data.strayPagekey;
  console.log(ok ? "OK" : "FAIL", path, { ...data, darkOk, legacyBody, darkClass });
  if (!ok) fail++;
  await page.close();
}

await browser.close();
process.exit(fail ? 1 : 0);
