# --- LIREATE SEO 2026-11-10 (do not remove backups: *.bak-2026-11-10-seo) ---

# www -> https apex (also used when port rule already forced HTTPS on www host)
RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [R=301,L]

# Junk query helpers -> canonical path without bad params (page still works if needed)
RewriteCond %{QUERY_STRING} (^|&)(test|mode)(=|&|$) [NC]
RewriteCond %{REQUEST_URI} !^/mail\.php$ [NC]
RewriteRule ^(.*)$ /$1? [R=301,L]

# Legacy blog duplicate
RewriteRule ^blog/?$ /news [R=301,L]

# CMS views: strip trailing slash (wrong title when slash present)
RewriteRule ^(news|kontaktyi|docs|team|mktu|patent|patent_prom_obr|reviews|portfolio|o_kompanii|partners|payment|personalArea|spasibo)/$ /$1 [R=301,L]

# Service landings: enforce trailing slash (matches in-page canonical)
RewriteRule ^(registraciya_tovarnogo_znaka|registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat|findtz|prodlenie_tovarnogo_znaka)$ /$1/ [R=301,L]

# Sitemap article slugs: add trailing slash (virtual CMS URLs, not files/dirs/admin)
RewriteCond %{REQUEST_METHOD} !POST
RewriteCond %{REQUEST_URI} !^/mail\.php$ [NC]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !/$
RewriteCond %{REQUEST_URI} !\.[a-zA-Z0-9]{2,5}$
RewriteCond %{REQUEST_URI} !^/(admin|template|upload|images|data|engine)(/|$) [NC]
RewriteCond %{REQUEST_URI} !^/registraciya_tovarnogo_znaka/?$ [NC]
RewriteCond %{REQUEST_URI} !^/registraciya_tovarnogo_znaka_s_oplatoy_za_rezultat/?$ [NC]
RewriteCond %{REQUEST_URI} !^/findtz/?$ [NC]
RewriteCond %{REQUEST_URI} !^/prodlenie_tovarnogo_znaka/?$ [NC]
RewriteCond %{REQUEST_URI} !^/(news|kontaktyi|docs|team|mktu|patent|patent_prom_obr|reviews|portfolio|o_kompanii|partners|payment|personalArea|spasibo|test|test2|test3|tester|check|docs2|pdf_book_1|blog|reg-tz-main)(/?)$ [NC]
RewriteRule ^([a-zA-Z0-9_\-]+)$ /$1/ [R=301,L]

<IfModule mod_headers.c>
  SetEnvIf Request_URI "^/(test|test2|test3|tester|check|docs2|personalArea|payment|pdf_book_1|blog|spasibo)(/)?$" lireate_noindex=1
  SetEnvIf Request_URI "^/goods/(8|11)/?$" lireate_noindex=1
  SetEnvIf Query_String "(^|&)(test|mode)(=|&|$)" lireate_noindex=1
  Header always set X-Robots-Tag "noindex, follow" env=lireate_noindex
</IfModule>
# --- end LIREATE SEO 2026-11-10 ---
