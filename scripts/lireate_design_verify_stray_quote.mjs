#!/usr/bin/env node
/** No `</script>" />` in HTML and no visible `" />` near top of body. */
const site = (process.env.LIREATE_PUBLIC_SITE_URL || "").replace(/\/$/, "");
if (!site) {
  console.error("LIREATE_PUBLIC_SITE_URL required");
  process.exit(2);
}

const paths = ["/reviews/", "/portfolio/", "/uslugi/", "/spasibo/"];
let fail = 0;

for (const path of paths) {
  const html = await fetch(site + path, { headers: { "Cache-Control": "no-cache" } }).then((r) =>
    r.text(),
  );
  if (html.includes('</script>" />') || html.includes("</script>\" />")) {
    console.log("FAIL", path, "stray_script_tail_in_html");
    fail++;
    continue;
  }
  const bodyM = html.match(/<body[^>]*>([\s\S]{0,6000})/i);
  const head = bodyM ? bodyM[1] : "";
  if (/>\s*"\s*\/>\s*(?=<|$)/.test(head.replace(/<[^>]+>/g, ">"))) {
    console.log("FAIL", path, "stray_quote_slash_text");
    fail++;
    continue;
  }
  if (/" \/>(?![^<]*<)/.test(head.slice(0, 500))) {
    console.log("FAIL", path, "stray_quote_slash_early_body");
    fail++;
    continue;
  }
  console.log("OK", path);
}

process.exit(fail ? 1 : 0);
