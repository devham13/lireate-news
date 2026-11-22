/* Browser regression checks against the actual home, without submitting forms. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');

async function snapshot(page) {
  return page.evaluate(() => ({
    title: document.title,
    description: document.querySelector('meta[name="description"]')?.content,
    canonical: document.querySelector('link[rel="canonical"]')?.href,
    robots: document.querySelector('meta[name="robots"]')?.content,
    headings: [...document.querySelectorAll('h1,h2,h3,h4')].map(e=>[e.tagName,e.textContent.trim()]),
    links: [...document.querySelectorAll('a[href]')].map(e=>e.getAttribute('href')),
    schema: [...document.querySelectorAll('script[type="application/ld+json"]')].map(e=>e.textContent),
    forms: [...document.querySelectorAll('form')].map(e=>[e.getAttribute('action'),e.getAttribute('method'),[...e.elements].map(x=>[x.name,x.type])]),
    sidebar: (()=>{const e=document.querySelector('#leftSideBar');if(!e)return null;const s=getComputedStyle(e);return[s.width,s.backgroundColor,s.fontFamily];})(),
  }));
}

(async () => {
  const css = await fs.readFile(path.join(__dirname,'../hosting-design/template/css/lireate-home-unslop.css'),'utf8');
  const dir = process.env.LIREATE_QA_OUTPUT || 'output/home-unslop';
  await fs.mkdir(dir,{recursive:true});
  const browser = await chromium.launch({headless:true});
  const reports=[];
  try {
    for (const width of [320,375,768,1024,1366,1920]) {
      const page = await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
      let deniedSubmissions=0;
      await page.route('**/*', route=>{
        const req=route.request();
        if(req.method()!=='GET' || /mc\.yandex|top-fwz1|vk\.com\/rtrg|google-analytics|googletagmanager/.test(req.url())) {
          if(req.method()!=='GET')deniedSubmissions++;
          return route.abort();
        }
        return route.continue();
      });
      const response=await page.goto('https://lireate.ru/',{waitUntil:'domcontentloaded',timeout:90000});
      assert.equal(response.status(),200);
      await page.locator('#lireate-home h1').waitFor();
      await page.evaluate(()=>Promise.race([document.fonts.ready,new Promise(resolve=>setTimeout(resolve,5000))]));
      await page.waitForTimeout(800);
      const original=await snapshot(page);
      assert.equal(original.headings.filter(x=>x[0]==='H1').length,1);
      if([375,1366].includes(width))await page.screenshot({path:path.join(dir,`before-${width}.png`),fullPage:true});
      await page.addStyleTag({content:css});
      await page.waitForFunction(()=>getComputedStyle(document.querySelector('.lireate-hero-v4__btn--primary')).backgroundColor==='rgb(49, 93, 221)',{},{timeout:5000});
      assert.deepEqual(await snapshot(page),original,'SEO, links, forms and navigation must be preserved');
      const metrics=await page.evaluate(()=>{
        const box=e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom};};
        const root=document.querySelector('#lireate-home');
        const cards=[...document.querySelectorAll('#modals > .advant')].map(box);
        const primary=document.querySelector('.lireate-hero-v4__btn--primary');
        const s=getComputedStyle(primary);
        const grid=document.querySelector('#modals');
        return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,root:box(root),cards,grid:{display:getComputedStyle(grid).display,columns:getComputedStyle(grid).gridTemplateColumns,items:[...grid.children].slice(0,4).map(e=>({column:getComputedStyle(e).gridColumn,row:getComputedStyle(e).gridRow}))},primary:{...box(primary),background:s.background,color:s.color,shadow:s.boxShadow},h1Weight:getComputedStyle(root.querySelector('h1')).fontWeight};
      });
      console.log('LAYOUT '+JSON.stringify(metrics));
      assert.ok(metrics.scrollWidth<=width+1,'Horizontal overflow at '+width);
      assert.equal(metrics.cards.length,4);
      const columns=width<768?1:2;
      if(columns===2) {
        assert.ok(Math.abs(metrics.cards[0].y-metrics.cards[1].y)<2,'Desktop cards must share a row');
        assert.ok(metrics.cards[1].x>=metrics.cards[0].right,'Cards must not overlap');
      } else {
        assert.ok(metrics.cards[1].y>=metrics.cards[0].bottom,'Mobile cards must not overlap');
      }
      for(const card of metrics.cards)assert.ok(card.x>=0&&card.right<=width+1,'Clipped card');
      assert.ok(Number(metrics.h1Weight)<=600);
      assert.ok(!metrics.primary.background.includes('gradient'));
      assert.ok(metrics.primary.background.includes('49, 93, 221'),'Primary accent must remain visible');
      assert.equal(metrics.primary.shadow,'none');
      assert.ok(metrics.primary.h>=44,'Touch target too small');
      if(width===375)assert.ok(metrics.primary.bottom<=900,'Consultation should be visible in the first phone screen');
      if([375,1366].includes(width)) {
        await page.screenshot({path:path.join(dir,`after-${width}.png`),fullPage:true});
        await page.locator('.lireate-hero-v4__btn--primary').click();
        await page.locator('.modal.in input[name="tel"], .modal.show input[name="tel"]').first().waitFor({state:'visible',timeout:10000});
        assert.ok(await page.locator('.modal.in input[name="name"], .modal.show input[name="name"]').first().isVisible());
      }
      reports.push({...metrics,columns,seoPreserved:true});
      await page.close();
    }
    await fs.writeFile(path.join(dir,'report.json'),JSON.stringify(reports,null,2));
    console.log(JSON.stringify(reports.map(r=>({width:r.width,columns:r.columns,overflow:r.scrollWidth>r.width,primaryBottom:r.primary.bottom,seoPreserved:r.seoPreserved})),null,2));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
