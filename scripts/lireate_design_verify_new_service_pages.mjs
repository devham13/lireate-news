#!/usr/bin/env node
/**
 * QA for /dogovory/ and /registraciya_programm_evm/ (local php -S or live).
 * Usage: node scripts/lireate_design_verify_new_service_pages.mjs <baseUrl> [outDir]
 */
import { chromium } from "playwright";
import { mkdir, writeFile, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");

const base = (process.argv[2] || process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!base) {
  console.error("Usage: node lireate_design_verify_new_service_pages.mjs <baseUrl> [outDir]");
  process.exit(2);
}
const outDir = process.argv[3] || "/opt/cursor/artifacts/lu-new-services-20261111";
const localPreview =
  process.env.LIREATE_LOCAL_PREVIEW === "1" || /^https?:\/\/(127\.0\.0\.1|localhost)(:|\/|$)/.test(base);
const paths = localPreview
  ? ["/dogovory/index.php", "/registraciya_programm_evm/index.php"]
  : ["/dogovory/", "/registraciya_programm_evm/"];
const widths = [375, 1024, 1280];
const siteCssHost = (process.env.LIREATE_CSS_PROXY || process.env.LIREATE_PUBLIC_SITE_URL || "").replace(
  /\/$/,
  "",
);

await mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const report = { base, ok: true, pages: {} };

for (const p of paths) {
  const slug = p.replace(/^\/|\/$/g, "").replace(/\/index\.php$/, "");
  report.pages[slug] = { checks: {}, shots: [] };
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.route("**/assets/lireate-shared/**", async (route) => {
      const u = route.request().url();
      const proxied = u.replace(/^https?:\/\/[^/]+/, siteCssHost);
      try {
        const resp = await page.request.get(proxied);
        await route.fulfill({ status: resp.status(), body: await resp.body(), headers: resp.headers() });
      } catch {
        await route.continue();
      }
    });
    await page.route("**/template/js/lireate-service-metrika-goals.js**", async (route) => {
      await route.fulfill({ status: 200, body: "/* stub */", contentType: "application/javascript" });
    });
    await page.route("**/template/css/lireate-service-mobile-bar.css**", async (route) => {
      const proxied = `${siteCssHost}/template/css/lireate-service-mobile-bar.css`;
      const resp = await page.request.get(proxied);
      await route.fulfill({ status: resp.status(), body: await resp.body(), headers: resp.headers() });
    });
    if (localPreview) {
      const rel = p.replace(/^\//, "");
      const html = await readFile(path.join(repoRoot, "hosting-design/service-landings", rel), "utf8");
      await page.setContent(html, { waitUntil: "domcontentloaded" });
    } else {
      const url = `${base}${p}`;
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 120000 });
    }
    try {
      const dark = await page.request.get(
        `${siteCssHost}/prodlenie_tovarnogo_znaka/assets/lireate-shared/lireate-service-dark.css`,
      );
      if (dark.ok()) await page.addStyleTag({ content: await dark.text() });
      const bar = await page.request.get(`${siteCssHost}/template/css/lireate-service-mobile-bar.css`);
      if (bar.ok()) await page.addStyleTag({ content: await bar.text() });
    } catch {
      /* prod CSS optional in CI */
    }
    await page.waitForTimeout(600);

    const h1 = await page.locator("h1").count();
    const overflow = await page.evaluate(() => {
      const sw = document.documentElement.scrollWidth;
      const cw = document.documentElement.clientWidth;
      return sw > cw + 2;
    });
    const bars = await page.locator(".lx-mobile-bar").count();
    const barVisible =
      bars > 0
        ? await page
            .locator(".lx-mobile-bar")
            .first()
            .evaluate((el) => {
              const s = window.getComputedStyle(el);
              return s.display !== "none" && s.visibility !== "hidden" && s.opacity !== "0";
            })
        : false;

    const contrastMin = await page.evaluate(() => {
      const pick = (sel) => {
        const el = document.querySelector(sel);
        if (!el) return null;
        const s = getComputedStyle(el);
        const fg = s.color;
        const bg = s.backgroundColor;
        return { fg, bg };
      };
      const hero = pick(".lx-hero h1");
      const body = pick("main");
      const parse = (c) => c.match(/[\d.]+/g)?.map(Number) || [0, 0, 0];
      const lum = ([r, g, b]) => {
        const a = [r, g, b].map((v) => {
          v /= 255;
          return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
      };
      const ratio = (fg, bg) => {
        const L1 = lum(parse(fg)) + 0.05;
        const L2 = lum(parse(bg)) + 0.05;
        return L1 > L2 ? L1 / L2 : L2 / L1;
      };
      if (!hero) return 21;
      return ratio(hero.fg, body?.bg || "rgb(15, 23, 42)");
    });

    let formOk = true;
    if (w === 375) {
      formOk = await page.evaluate(() => {
        const f = document.querySelector("form[data-lx-mail-action]");
        return f ? f.checkValidity() === false : false;
      });
    }

    const key = `${w}`;
    report.pages[slug].checks[key] = { h1, overflow, bars, barVisible, contrastMin, formOk };
    if (h1 !== 1 || overflow) report.ok = false;
    if (w === 375 && (!barVisible || bars !== 1)) report.ok = false;
    if (w >= 1024 && barVisible) report.ok = false;
    if (contrastMin < 4.5) report.ok = false;
    if (w === 375 && !formOk) report.ok = false;

    const file = path.join(outDir, `${slug}-${w}.png`);
    await page.screenshot({ path: file, fullPage: true });
    report.pages[slug].shots.push(file);
    await page.close();
  }
}

await browser.close();
await writeFile(path.join(outDir, "report.json"), JSON.stringify(report, null, 2));
console.log(report.ok ? "VERIFY_NEW_SERVICES_OK" : "VERIFY_NEW_SERVICES_FAIL", outDir);
process.exit(report.ok ? 0 : 1);
