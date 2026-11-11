#!/usr/bin/env node
/** reviews / portfolio / spasibo: dark body classes, 1 h1, no hero overlap at 375/1024/1280 (DOM) */
import { chromium } from "playwright";

const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const paths = ["/reviews/", "/portfolio/", "/spasibo/", "/uslugi/"];
const widths = [375, 1024, 1280];
const browser = await chromium.launch({ headless: true });
let fail = 0;

for (const path of paths) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(site + path, { waitUntil: "domcontentloaded", timeout: 60000 });
    const content = await page.content();
    if (content.includes('</script>" />') || content.includes("</script>\" />")) {
      console.log("FAIL", path, w, "stray_script_quote_tail");
      fail++;
      await page.close();
      continue;
    }
    const data = await page.evaluate((p) => {
      const body = document.body;
      const h1 = document.querySelectorAll("h1").length;
      const dark =
        body.classList.contains("lireate-cms-page-dark") &&
        (body.classList.contains("lireate-reviews-body") ||
          body.classList.contains("lireate-portfolio-body") ||
          body.classList.contains("lireate-spasibo-body"));
      const hero = document.querySelector(".main-screen.main_back:not(.lireate-hero-v4)");
      const heroVisible = hero && hero.getBoundingClientRect().height > 8;
      const bar = document.querySelectorAll(".lx-mobile-bar").length;
      const h2 = document.querySelectorAll("h2").length;
      const face = document.querySelector("#face");
      const bgMain = document.querySelector("#face .bg_main");
      const bgMainHidden =
        !bgMain || getComputedStyle(bgMain).display === "none" || bgMain.offsetHeight < 2;
      const faceBg = face ? getComputedStyle(face).backgroundColor : "";
      let strayText = false;
      const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = tw.nextNode())) {
        const t = (node.textContent || "").trim();
        if (t === '" />' || t === '"/>' ) {
          strayText = true;
          break;
        }
      }
      const box = face ? face.querySelector(".contentBox") : null;
      const faceH = face ? face.getBoundingClientRect().height : 0;
      const boxH = box ? box.getBoundingClientRect().height : 0;
      let faceTailGap = 0;
      if (face && box) {
        const stats = box.querySelectorAll(".titleDesc");
        let last = null;
        for (let i = stats.length - 1; i >= 0; i--) {
          const el = stats[i];
          if (el && getComputedStyle(el).display !== "none" && (el.textContent || "").trim()) {
            last = el;
            break;
          }
        }
        if (last) {
          const faceBot = face.getBoundingClientRect().bottom;
          const lastBot = last.getBoundingClientRect().bottom;
          faceTailGap = Math.max(0, Math.round(faceBot - lastBot));
        }
      }
      return {
        h1,
        h2,
        dark,
        heroVisible,
        bar,
        cls: body.className,
        bgMainHidden,
        faceBg,
        path: p,
        strayText,
        faceH,
        boxH,
        faceTailGap,
      };
    }, path);
    const headingOk = data.h1 === 1 || (path === "/spasibo/" && data.h1 === 0 && data.h2 >= 1);
    const faceOk = path === "/spasibo/" || data.h1 >= 1;
    const portfolioMobileOk =
      path !== "/portfolio/" ||
      w > 768 ||
      (data.boxH > 0 && data.boxH < 320 && data.faceH < 340 && data.faceTailGap < 80);
    let ok;
    if (path === "/uslugi/") {
      ok = !data.strayText;
    } else {
      ok =
        headingOk &&
        data.dark &&
        !data.heroVisible &&
        faceOk &&
        !data.strayText &&
        portfolioMobileOk;
    }
    console.log(ok ? "OK" : "FAIL", path, w, data);
    if (!ok) fail++;
    await page.close();
  }
}
await browser.close();
process.exit(fail ? 1 : 0);
