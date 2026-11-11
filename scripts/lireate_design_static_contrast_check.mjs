#!/usr/bin/env node
/** Contrast ≥ 4.5:1 with static3 CSS injected (pre-deploy QA). */
import { chromium } from "playwright";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

function lum(rgb) {
  const [r, g, b] = rgb.map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrast(fg, bg) {
  const L1 = lum(fg);
  const L2 = lum(bg);
  const hi = Math.max(L1, L2);
  const lo = Math.min(L1, L2);
  return (hi + 0.05) / (lo + 0.05);
}

function parseRgb(str) {
  const m = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return null;
  return [+m[1], +m[2], +m[3]];
}

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const css = await readFile(join(root, "hosting-design/template/css/lireate-static-pages-lu.css"), "utf8");
const js = await readFile(join(root, "hosting-design/template/js/lireate-static-hero-lu.js"), "utf8");

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
const cases = [
  { path: "/spasibo/", sel: ".lireate-spasibo-body .txt-content p" },
  { path: "/portfolio/", sel: "#face .h1" },
  { path: "/portfolio/", sel: "#face .titleDesc" },
  { path: "/reviews/", sel: "#face .h1" },
  { path: "/reviews/", sel: "#face .titleDesc" },
];

const browser = await chromium.launch({ headless: true });
let fail = 0;
for (const { path, sel } of cases) {
  const page = await browser.newPage({ viewport: { width: 1024, height: 900 } });
  await page.goto(site + path, { waitUntil: "domcontentloaded", timeout: 90000 });
  await page.addStyleTag({ content: css });
  await page.evaluate(js);
  const ratio = await page.evaluate((selector) => {
    const el = document.querySelector(selector);
    if (!el) return null;
    const fg = getComputedStyle(el).color;
    let n = el;
    let bg = "rgb(11, 16, 32)";
    while (n) {
      const b = getComputedStyle(n).backgroundColor;
      if (b && b !== "rgba(0, 0, 0, 0)" && b !== "transparent") {
        bg = b;
        break;
      }
      n = n.parentElement;
    }
    return { fg, bg, text: (el.textContent || "").slice(0, 80) };
  }, sel);
  if (!ratio) {
    console.log("SKIP", path, sel);
    await page.close();
    continue;
  }
  const fg = parseRgb(ratio.fg);
  const bg = parseRgb(ratio.bg);
  const cr = fg && bg ? contrast(fg, bg) : 0;
  const ok = cr >= 4.5;
  console.log(ok ? "OK" : "FAIL", path, cr.toFixed(2), ratio.text);
  if (!ok) fail++;
  await page.close();
}
await browser.close();
process.exit(fail ? 1 : 0);
