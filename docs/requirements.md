# CCN portal: scope and requirements

## Company and business context

Cargo Community Network (CCN) is a Singapore-headquartered digital solutions provider for the air cargo community. Public CCN materials describe services for airlines, freight forwarders, ground handlers, shippers, integrators and authorities, across cargo data exchange, operations, customs/compliance, visibility and payments. The portal is scoped as a public product discovery and enquiry site.

## User groups

- Air cargo businesses evaluating CCN solutions.
- Existing customers and integration partners looking for product or support information.
- CCN commercial staff receiving and routing business enquiries.
- CCN site administrators maintaining public product information.

## Functional requirements in the current release

1. Present CCN, its air cargo ecosystem and broad solution areas in English.
2. Display a MySQL-backed product catalogue grouped by solution area.
3. Search products by name, description or category; filter by category and cargo partner type.
4. Collect an enquiry with name, company, organisation type, country, business email, phone, solution interest, subject and a short message.
5. Store submitted enquiries in MySQL with a received timestamp and status.
6. Provide staff-only sign-in, enquiry totals, recent enquiries, search, status updates and CSV export.
7. Restrict public requests with a rate limit; use anti-forgery tokens and a hidden honeypot on the contact form.
8. Allow local database setup and inspection through HeidiSQL scripts.

## Non-functional requirements

- ASP.NET Core Razor Pages on .NET 8; MySQL 8 compatible with utf8mb4.
- Responsive layout for desktop and mobile.
- Use environment variables for admin and database secrets; do not commit live credentials.
- Production deployment must use HTTPS, encrypted MySQL transport, a least-privilege DB account, protected persistent data-protection keys, backups and a published privacy notice.
- Keep enquiry collection limited to business contact and routing information; do not request shipment documents or confidential operational data through the public form.

## Data model

- `products`: public product name, slug, category, summary, target audience, optional official URL and display order.
- `contact_inquiries`: sender/business contact, organisation type, country, solution interest, enquiry text, received time and follow-up status.

## Out of scope for this release

Live booking, shipment tracking, TradeNet submissions, payments, insurance binding, customer accounts, API documentation behind login and operational cargo-system integrations. These need CCN-owned API specifications, credentials, security review and product-owner approval.

## Content review before publication

Product names and general capabilities follow the public CCN product catalogue. The short descriptions in the seed script are summaries and must be checked by CCN product owners. Add approved product URLs, support contacts, privacy wording, regional details, accessibility review, and current brand assets before production launch.
