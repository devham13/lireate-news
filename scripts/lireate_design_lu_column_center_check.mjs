#!/usr/bin/env node
/** Wide LU column: .lu-wrap / .conteinerX должны быть по центру правой панели (1920). */
import { chromium } from "playwright";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}
const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const viewportCss = await readFile(join(root, "hosting-design/template/css/lireate-lu-viewport.css"), "utf8");
const cmsLuCss = await readFile(join(root, "hosting-design/template/css/lireate-cms-lu.css"), "utf8");
const mktuCss = await readFile(join(root, "hosting-design/template/css/lireate-mktu-lu.css"), "utf8");
const homeLuCss = await readFile(join(root, "hosting-design/template/page/home/lireate-home-lu.css"), "utf8");
const fixCss = [viewportCss, cmsLuCss, mktuCss, homeLuCss].join("\n");

const pages = [
  { path: "/", slug: "home", sel: "#lireate-home .lu-wrap, #lireate-home .lh-wrap" },
  { path: "/mktu/", slug: "mktu", sel: ".mktu_head, .conteinerX" },
  { path: "/uslugi/", slug: "uslugi", sel: ".page_container.lu-page, #lireate-uslugi.page_container, body.lireate-uslugi-body .page_container" },
  { path: "/patent/", slug: "patent", sel: "body.lireate-cms-page-dark .container.content > .row.col-xs-12" },
];
const widths = [375, 768, 1024, 1366, 1600, 1920];

function centeredEnough(box, vw, sidebarRight) {
  if (vw < 1500) return { ok: true, reason: "below-1500" };
  const paneLeft = sidebarRight > 50 ? sidebarRight : 20;
  const paneRight = vw - 32;
  const paneMid = (paneLeft + paneRight) / 2;
  const elMid = box.left + box.width / 2;
  const tol = 28;
  const gapR = paneRight - (box.left + box.width);
  const gapL = box.left - paneLeft;
  const balanced = Math.abs(gapL - gapR) <= tol;
  const nearMid = Math.abs(elMid - paneMid) <= tol;
  return { ok: balanced && nearMid, gapL, gapR, elMid, paneMid };
}

let fail = 0;
const browser = await chromium.launch({ headless: true });
for (const { path, slug, sel } of pages) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(`${site}${path}?qa=${Date.now()}`, { waitUntil: "networkidle", timeout: 120000 });
    await page.waitForTimeout(400);
    if (w >= 1500) {
      await page.addStyleTag({ content: fixCss, id: "lireate-lu-column-center-fix" });
      await page.waitForTimeout(250);
    }
    const rep = await page.evaluate((selector) => {
      const menu = document.getElementById("leftSideBar");
      const sidebarRight = menu ? menu.getBoundingClientRect().right : 0;
      const el = document.querySelector(selector);
      if (!el) return { missing: selector };
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        missing: null,
        sidebarRight,
        left: Math.round(r.left),
        width: Math.round(r.width),
        maxWidth: cs.maxWidth,
        marginLeft: cs.marginLeft,
        marginRight: cs.marginRight,
      };
    }, sel);
    const box = rep.missing ? null : { left: rep.left, width: rep.width };
    const cen = box ? centeredEnough(box, w, rep.sidebarRight) : { ok: false, reason: rep.missing };
    const row = { slug, w, sel, ...rep, ...cen };
    console.log(JSON.stringify(row));
    if (rep.missing) fail = 1;
    else if (rep.width < 40 && w >= 1400) {
      /* skip hidden shell */
    } else if (!cen.ok) fail = 1;
    await page.close();
  }
}
await browser.close();
process.exit(fail);
