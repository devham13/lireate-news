#!/usr/bin/env node
/**
 * Mobile service dock QA: bottom + footer at 375/390, desktop 1366 (no bar).
 * Usage: node scripts/lireate_design_service_dock_screenshots.mjs [baseUrl] [outDir]
 */
import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const baseArg = process.argv[2] || process.env.LIREATE_PUBLIC_SITE_URL || "";
if (!baseArg) {
  console.error("Usage: node lireate_design_service_dock_screenshots.mjs <baseUrl> [outDir]");
  process.exit(2);
}
const base = baseArg.replace(/\/$/, "");
const outDir = process.argv[3] || "/opt/cursor/artifacts/service-mobile-dock";

const paths = [
  "/findtz/",
  "/registraciya_tovarnogo_znaka/",
  "/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/",
  "/prodlenie_tovarnogo_znaka/",
  "/vozrazhenie_protiv_registracii_tovarnogo_znaka/",
  "/registraciya_tovarnogo_znaka_v_kitae/",
  "/zashchita_avtorskih_prav/",
  "/dogovory/",
  "/registraciya_programm_evm/",
  "/poisk_tovarnyh_znakov/",
  "/ekspertiza_tovarnogo_znaka/",
  "/mezhdunarodnaja_registracija_tovarnogo_znaka/",
  "/registracija_torgovyh_marok_i_logotipov/",
  "/patent",
  "/patent_prom_obr",
  "/mktu",
  "/uslugi/",
];

await mkdir(outDir, { recursive: true });
const manifest = { base, shots: [], barVisible: {} };
const browser = await chromium.launch({ headless: true });

for (const p of paths) {
  const slug = p.replace(/^\/|\/$/g, "").replace(/\//g, "_") || "home";
  const url = `${base}${p.startsWith("/") ? p : `/${p}`}`;
  for (const [tag, w, h] of [
    ["375", 375, 812],
    ["390", 390, 844],
    ["1366", 1366, 900],
  ]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(url, { waitUntil: "networkidle", timeout: 120000 });
    await page.waitForTimeout(1500);
    const barCount = await page.locator(".lx-mobile-bar").count();
    const barVis =
      barCount > 0
        ? await page
            .locator(".lx-mobile-bar")
            .first()
            .evaluate((el) => {
              const s = window.getComputedStyle(el);
              return s.display !== "none" && s.visibility !== "hidden";
            })
        : false;
    const file = `${slug}-${tag}.png`;
    if (tag === "375") {
      manifest.barVisible[slug] = { mobile: barVis, barCount };
    }
    if (tag === "1366") {
      manifest.barVisible[slug] = { ...(manifest.barVisible[slug] || {}), desktop: barVis };
    }
    const fullPath = path.join(outDir, file);
    if (tag === "1366") {
      await page.screenshot({ path: fullPath, fullPage: false });
    } else {
      await page.screenshot({ path: fullPath, fullPage: true });
      const footerPath = path.join(outDir, `${slug}-${tag}-footer.png`);
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(400);
      await page.screenshot({ path: footerPath, fullPage: false });
      manifest.shots.push(footerPath);
    }
    manifest.shots.push(fullPath);
    await page.close();
  }
}

await browser.close();
await writeFile(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2));
console.log("SERVICE_DOCK_SCREENSHOTS_OK", outDir);
