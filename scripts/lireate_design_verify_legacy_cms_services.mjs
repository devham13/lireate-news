#!/usr/bin/env node
const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
const paths = [
  "/poisk_tovarnyh_znakov/",
  "/ekspertiza_tovarnogo_znaka/",
  "/mezhdunarodnaja_registracija_tovarnogo_znaka/",
  "/registracija_torgovyh_marok_i_logotipov/",
];
let fail = 0;
for (const path of paths) {
  const html = await fetch(site + path, { headers: { "Cache-Control": "no-cache" } }).then((r) => r.text());
  const code = await fetch(site + path).then((r) => r.status);
  const h1 = (html.match(/<h1[\s>]/gi) || []).length;
  const legacyCss = html.includes("lireate-legacy-cms-lu.css");
  const bodyDark =
    html.includes("lireate-legacy-cms-lu") || html.includes("lireate-cms-page-dark");
  const ok = code === 200 && h1 === 1 && (legacyCss || bodyDark);
  console.log(ok ? "OK" : "FAIL", path, { code, h1, legacyCss, bodyDark });
  if (!ok) fail++;
}
process.exit(fail ? 1 : 0);
