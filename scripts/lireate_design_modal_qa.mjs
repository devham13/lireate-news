#!/usr/bin/env node
import { chromium } from "playwright";

const site = process.env.LIREATE_PUBLIC_SITE_URL;
if (!site) process.exit(2);

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1024, height: 800 } });
await page.goto(`${site}/?qa=${Date.now()}`, { waitUntil: "networkidle", timeout: 120000 });
await page.locator("#pat_but").click();
await page.waitForTimeout(900);
const center = await page.evaluate(() => {
  const cx = innerWidth / 2;
  const cy = innerHeight / 2;
  const el = document.elementFromPoint(cx, cy);
  const inModal = !!el?.closest("#main-modal .modal-content");
  const bg = document.querySelector("#main-modal .modal-content");
  return {
    inModal,
    tag: el?.tagName,
    cls: el?.className?.slice?.(0, 60),
    bg: bg ? getComputedStyle(bg).backgroundColor : null,
  };
});
const link = page.locator("#modal-list a").first();
const href = await link.getAttribute("href");
await link.click();
await page.waitForTimeout(800);
const afterClick = page.url();
await page.goto(`${site}/?qa=2`, { waitUntil: "networkidle" });
await page.locator("#pat_but").click();
await page.waitForTimeout(500);
await page.locator("#main-modal .close").click({ force: true });
await page.waitForTimeout(400);
const closed = await page.evaluate(() => !document.querySelector("#main-modal.in"));
await page.locator(".lireate-hero-v4__btn--primary").click();
await page.waitForTimeout(600);
const name = page.locator('.modal-mail input[name="name"], .modal.in input[type="text"]').first();
const okFill = (await name.count()) > 0;
if (okFill) await name.fill("Тест");
console.log(JSON.stringify({ center, href, afterClick, closed, okFill }, null, 2));
await browser.close();
process.exit(center.inModal && closed && okFill ? 0 : 1);
