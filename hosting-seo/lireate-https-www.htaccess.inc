# --- LIREATE audit 2026-11-11: single-hop http(s)://www → https://apex ---
# Replace legacy port-443 rule that kept SERVER_NAME (www).

RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [R=301,L]

RewriteCond %{SERVER_PORT} !^443$
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
