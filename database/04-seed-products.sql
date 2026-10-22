USE ccn_portal;

INSERT INTO products (name, slug, category, summary, audience, is_featured, sort_order) VALUES
('Air Cargo Booking API', 'air-cargo-booking-api', 'Booking & Rates', 'Connect cargo booking workflows with airline capacity and freight management systems through APIs.', 'airlines, freight forwarders and integrators', TRUE, 1),
('Booking Concierge 3.0', 'booking-concierge', 'Booking & Rates', 'A digital booking experience designed to help cargo partners find and manage air freight options.', 'freight forwarders and shippers', TRUE, 2),
('Quotation Request', 'quotation-request', 'Booking & Rates', 'Create and manage air freight rate requests through a shared digital workflow.', 'freight forwarders and shippers', TRUE, 3),
('Manage Rates', 'manage-rates', 'Booking & Rates', 'Maintain multilingual quotations, rate history and links to billing or reservation systems.', 'airlines and freight forwarders', FALSE, 4),
('Aircargo eXchange Information System (AXIS)', 'axis', 'Visibility & Operations', 'Web-based shipment tracking with status updates and operational visibility.', 'freight forwarders and airlines', TRUE, 5),
('Control Tower', 'control-tower', 'Visibility & Operations', 'Bring cargo status, alerts and key operational indicators into a real-time dashboard.', 'airlines and freight forwarders', TRUE, 6),
('Cool Chain', 'cool-chain', 'Visibility & Operations', 'Track shipment milestones and report performance for temperature-sensitive cargo workflows.', 'shippers and freight forwarders', FALSE, 7),
('Truck Dock Slot Booking', 'truck-dock-slot-booking', 'Visibility & Operations', 'Coordinate advance truck dock appointments to improve cargo facility scheduling.', 'truckers, ground handlers and shippers', FALSE, 8),
('eFreight & eAWB Services', 'efreight-eawb', 'Digital Cargo', 'Support electronic air waybill and freight processes with digital data exchange.', 'airlines and freight forwarders', TRUE, 9),
('FWB/FHL API', 'fwb-fhl-api', 'Digital Cargo', 'Exchange electronic air waybill and house waybill messages through system integrations.', 'airlines, freight forwarders and integrators', FALSE, 10),
('TradeNet', 'tradenet', 'Customs & Compliance', 'Prepare and submit trade permit declarations through a digital customs workflow.', 'freight forwarders and shippers', TRUE, 11),
('TradeNet OCR', 'tradenet-ocr', 'Customs & Compliance', 'Use OCR-assisted data capture to support cargo manifest declaration preparation.', 'freight forwarders and shippers', TRUE, 12),
('Pre-Arrival Compliance', 'pre-arrival-compliance', 'Customs & Compliance', 'Support pre-arrival customs processes with data checks and workflow visibility.', 'freight forwarders and shippers', FALSE, 13),
('Pre-Departure Compliance', 'pre-departure-compliance', 'Customs & Compliance', 'Support air cargo screening and pre-departure compliance workflows.', 'airlines and freight forwarders', FALSE, 14),
('DGOffice', 'dgoffice', 'Customs & Compliance', 'Manage dangerous goods documentation and related compliance workflows.', 'airlines and freight forwarders', FALSE, 15),
('HS Code Match', 'hs-code-match', 'Customs & Compliance', 'Support product classification workflows using Harmonized System code information.', 'freight forwarders and shippers', FALSE, 16),
('Electronic Payment and Invoicing for Cargo (EPIC)', 'epic', 'Payments & Protection', 'Digitalize cargo payments, invoicing, billing status and dispute workflows.', 'airlines and freight forwarders', TRUE, 17),
('CargoProtect', 'cargoprotect', 'Payments & Protection', 'Explore shipment insurance options and a digital claims experience for cargo movements.', 'freight forwarders and shippers', FALSE, 18),
('ONE Record', 'one-record', 'Data & Integration', 'Support adoption of IATA ONE Record for connected air cargo data exchange.', 'airlines, freight forwarders and integrators', FALSE, 19),
('Shipment Visibility Services (SVS)', 'shipment-visibility-services', 'Visibility & Operations', 'Bring shipment milestones together to improve supply chain visibility across partners.', 'freight forwarders, shippers and integrators', FALSE, 20)
ON DUPLICATE KEY UPDATE
  name = VALUES(name), category = VALUES(category), summary = VALUES(summary),
  audience = VALUES(audience), is_featured = VALUES(is_featured), sort_order = VALUES(sort_order);
