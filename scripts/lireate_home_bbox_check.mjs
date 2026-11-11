#!/usr/bin/env node
import { chromium } from "playwright";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

function overlap(a, b) {
  return (
    a.left < b.right &&
    a.right > b.left &&
    a.top < b.bottom &&
    a.bottom > b.top
  );
}

const widths = [375, 768, 1366, 1920];
let fail = 0;
const browser = await chromium.launch({ headless: true });
for (const w of widths) {
  const page = await browser.newPage({ viewport: { width: w, height: 900 } });
  await page.goto(site + "/?bbox=" + w, { waitUntil: "networkidle", timeout: 120000 });
  const rep = await page.evaluate(() => {
    const overlap = (a, b) =>
      a.left < b.right &&
      a.right > b.left &&
      a.top < b.bottom &&
      a.bottom > b.top;
    const menu = document.getElementById("leftSideBar");
    const mr = menu && menu.getBoundingClientRect().width > 50 ? menu.getBoundingClientRect().right : 0;
    const sel = [
      ".lireate-hero-v4",
      "#lireate-home .lh-wrap > *",
      ".lh-why-grid .advant",
      ".product.lh-product",
      ".lireate-home-blog",
      ".lx-site-footer",
    ];
    const edges = [];
    document.querySelectorAll(sel.join(",")).forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.height < 2) return;
      edges.push({ l: r.left, t: el.className.slice(0, 40) });
      if (mr > 0 && r.left < mr - 1) {
        edges.push({ underMenu: r.left, mr });
      }
    });
    const cards = [...document.querySelectorAll(".lh-why-grid > .advant, .product.lh-product")];
    const pairs = [];
    for (let i = 0; i < cards.length; i++) {
      for (let j = i + 1; j < cards.length; j++) {
        const a = cards[i].getBoundingClientRect();
        const b = cards[j].getBoundingClientRect();
        if (overlap(a, b)) pairs.push([cards[i].className, cards[j].className]);
      }
    }
    const ff = getComputedStyle(document.querySelector("#modals p") || document.body).fontFamily;
    return {
      mr,
      underMenu: edges.filter((e) => e.underMenu),
      overlaps: pairs,
      inter: /Inter/i.test(ff),
      hs: document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1,
    };
  });
  console.log("w", w, JSON.stringify(rep));
  if (rep.underMenu.length || rep.overlaps.length || !rep.inter || !rep.hs) fail = 1;
  await page.close();
}
await browser.close();
process.exit(fail);
