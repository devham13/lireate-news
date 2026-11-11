#!/usr/bin/env node
import { chromium } from "playwright";

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
const paths = ["/", "/news/", "/findtz/", "/avtor/", "/mktu"];
const browser = await chromium.launch({ headless: true });
let fail = 0;

for (const path of paths) {
  const page = await browser.newPage({ viewport: { width: 375, height: 800 } });
  await page.goto(site + path, { waitUntil: "domcontentloaded", timeout: 60000 });
  const data = await page.evaluate(() => {
    const block = document.getElementById("floatingBlock");
    const msg = document.getElementById("managerMessage");
    const msgVisible =
      msg && msg.getBoundingClientRect().width > 2 && getComputedStyle(msg).display !== "none";
    const iconsOnly = block && block.classList.contains("lx-widget-icons-only");
    const w = block ? block.getBoundingClientRect().width : 0;
    const hiddenSvc = block && getComputedStyle(block).display === "none";
    return { msgVisible, iconsOnly, w, hiddenSvc, hasBlock: !!block };
  });
  const ok =
    !data.hasBlock ||
    data.hiddenSvc ||
    (data.w > 40 && data.w < 90 && !data.msgVisible && data.iconsOnly);
  console.log(ok ? "OK" : "FAIL", path, data);
  if (!ok) fail++;
  await page.close();
}
await browser.close();
process.exit(fail ? 1 : 0);
