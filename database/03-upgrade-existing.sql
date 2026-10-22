USE ccn_portal;

-- Run this upgrade once if the original contact_inquiries table is already present.
ALTER TABLE contact_inquiries
  ADD COLUMN organization_type VARCHAR(100) NOT NULL DEFAULT 'Other' AFTER company,
  ADD COLUMN country VARCHAR(80) NOT NULL DEFAULT 'Not provided' AFTER organization_type,
  ADD COLUMN product_interest VARCHAR(140) NOT NULL DEFAULT 'General enquiry' AFTER phone;

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
