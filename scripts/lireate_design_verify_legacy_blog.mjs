#!/usr/bin/env node
/** Sample blog URLs: .lireate-blog-page in article + body legacy class + 1 h1 */
const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const paths =
  process.env.LIREATE_VERIFY_BLOG_PATHS?.split(",").filter(Boolean) ||
  [
    "/chto_delat_esli_tovarnyiy_znak_zanyat/",
    "/kak-zaregistrirovat-tovarnyy-znak-samostoyatelno-2026/",
    "/proverka_tovarnogo_znaka_pered_registraciey_chek_list_po_reestram_rospatenta/",
  ];

let fail = 0;
for (const path of paths) {
  const url = site + path;
  const html = await fetch(url, { headers: { "Cache-Control": "no-cache" } }).then((r) => r.text());
  const code = await fetch(url, { headers: { "Cache-Control": "no-cache" } }).then((r) => r.status);
  const h1 = (html.match(/<h1[\s>]/gi) || []).length;
  const blog = /id=["']articleBox["'][^>]*>[\s\S]*class=["']lireate-blog-page/.test(html);
  const dark = html.includes("lireate-legacy-article-lu") || html.includes("lireate-cms-page-dark");
  const ok = code === 200 && h1 === 1 && blog && dark;
  console.log(ok ? "OK" : "FAIL", path, { code, h1, blog, dark });
  if (!ok) fail++;
}
process.exit(fail ? 1 : 0);
