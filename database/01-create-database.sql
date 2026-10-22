CREATE DATABASE IF NOT EXISTS ccn_portal
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Untuk penggunaan nyata, buat user aplikasi tersendiri dan batasi host serta hak aksesnya.
-- Contoh (ganti password sebelum dijalankan):
-- CREATE USER 'ccn_app'@'localhost' IDENTIFIED BY 'GANTI_PASSWORD';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ccn_portal.* TO 'ccn_app'@'localhost';
