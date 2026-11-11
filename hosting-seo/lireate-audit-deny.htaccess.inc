# --- LIREATE audit 2026-11-11: deny web access to backups and sensitive files ---

# Site-wide: block downloadable backup / dump / archive patterns (files stay on disk).
<IfModule mod_authz_core.c>
  <FilesMatch "\.(log|sql|zip)(\.|$)|\.bak">
    Require all denied
  </FilesMatch>
</IfModule>
<IfModule !mod_authz_core.c>
  <FilesMatch "\.(log|sql|zip)(\.|$)|\.bak">
    Order allow,deny
    Deny from all
  </FilesMatch>
</IfModule>

# Document root named sensitive files (explicit).
<IfModule mod_authz_core.c>
  <FilesMatch "^(PHP_errors\.log|error_log_|cookie\.txt|everest\.zip)$">
    Require all denied
  </FilesMatch>
</IfModule>
<IfModule !mod_authz_core.c>
  <FilesMatch "^(PHP_errors\.log|error_log_|cookie\.txt|everest\.zip)$">
    Order allow,deny
    Deny from all
  </FilesMatch>
</IfModule>
# --- end LIREATE audit deny ---
