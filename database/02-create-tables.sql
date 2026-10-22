USE ccn_portal;

CREATE TABLE IF NOT EXISTS contact_inquiries (
  id BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(120) NOT NULL,
  company VARCHAR(160) NULL,
  organization_type VARCHAR(100) NOT NULL,
  country VARCHAR(80) NOT NULL,
  email VARCHAR(190) NOT NULL,
  phone VARCHAR(40) NULL,
  product_interest VARCHAR(140) NOT NULL,
  subject VARCHAR(180) NOT NULL,
  message TEXT NOT NULL,
  assigned_to VARCHAR(100) NULL,
  internal_notes TEXT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'new',
  created_at DATETIME NOT NULL,
  updated_at DATETIME NULL,
  PRIMARY KEY (id),
  KEY ix_contact_inquiries_created_at (created_at),
  KEY ix_contact_inquiries_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS products (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(140) NOT NULL,
  slug VARCHAR(160) NOT NULL,
  category VARCHAR(80) NOT NULL,
  summary VARCHAR(500) NOT NULL,
  audience VARCHAR(180) NOT NULL,
  url VARCHAR(500) NULL,
  is_featured BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order INT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY ux_products_slug (slug),
  KEY ix_products_category_sort (category, sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
