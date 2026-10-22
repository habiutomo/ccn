USE ccn_portal;

-- Run once to enable enquiry assignment and internal follow-up notes.
ALTER TABLE contact_inquiries
  ADD COLUMN assigned_to VARCHAR(100) NULL AFTER message,
  ADD COLUMN internal_notes TEXT NULL AFTER assigned_to,
  ADD COLUMN updated_at DATETIME NULL AFTER created_at;
