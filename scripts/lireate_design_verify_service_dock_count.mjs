#!/usr/bin/env node
import { chromium } from "playwright";

const baseArg = process.argv[2] || process.env.LIREATE_PUBLIC_SITE_URL || "";
if (!baseArg) {
  console.error("Usage: node lireate_design_verify_service_dock_count.mjs <baseUrl>");
  process.exit(2);
}
const base = baseArg.replace(/\/$/, "");

const paths = [
  "/findtz/",
  "/registraciya_tovarnogo_znaka/",
  "/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/",
  "/prodlenie_tovarnogo_znaka/",
  "/vozrazhenie_protiv_registracii_tovarnogo_znaka/",
  "/registraciya_tovarnogo_znaka_v_kitae/",
  "/zashchita_avtorskih_prav/",
  "/poisk_tovarnyh_znakov/",
  "/ekspertiza_tovarnogo_znaka/",
  "/mezhdunarodnaja_registracija_tovarnogo_znaka/",
  "/registracija_torgovyh_marok_i_logotipov/",
  "/patent",
  "/patent_prom_obr",
  "/mktu",
  "/uslugi/",
];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
const bad = [];
for (const p of paths) {
  const url = `${base}${p}`;
  await page.goto(url, { waitUntil: "networkidle", timeout: 120000 });
  const n = await page.evaluate(() => document.querySelectorAll(".lx-mobile-bar").length);
  if (n !== 1) bad.push({ path: p, count: n });
}
await browser.close();
if (bad.length) {
  console.error("SERVICE_DOCK_COUNT_FAIL", JSON.stringify(bad, null, 2));
  process.exit(1);
}
console.log("SERVICE_DOCK_COUNT_OK", paths.length);
