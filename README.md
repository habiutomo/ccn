# Cargo Community Network portal

An English-language air cargo solutions website and enquiry workflow built with ASP.NET Core Razor Pages (.NET 8), Entity Framework Core and MySQL. HeidiSQL is used to inspect and manage the database.

## Features

- Searchable product catalogue with category and cargo-partner filters.
- Solution cards seeded from CCN's public product catalogue.
- Structured business enquiries recording contact, company, organisation type, country, selected solution and message.
- Staff sign-in with cookie authentication and protected admin pages.
- Enquiry dashboard with counts for all four workflow stages, search, status filters, pagination and CSV export.
- Enquiry detail pages with contact details, assignment, private internal notes and last-updated timestamps.
- MySQL schema and product catalogue scripts for HeidiSQL.
- Request rate limiting, anti-forgery tokens and a hidden bot-trap field on the enquiry form.

## Database setup in HeidiSQL

For a fresh database:

1. Start MySQL and open a local connection in HeidiSQL.
2. Run `database/01-create-database.sql`.
3. Select `ccn_portal` and run `database/02-create-tables.sql`.
4. Run `database/04-seed-products.sql` to add the initial product catalogue.

For the database created by the earlier prototype, run `database/03-upgrade-existing.sql` **once**, then run `database/04-seed-products.sql`. The upgrade adds enquiry fields and creates the product table while preserving existing enquiries.

For an existing upgraded database, run `database/05-add-enquiry-follow-up.sql` **once** to add staff assignment and internal notes. Fresh databases created from `02-create-tables.sql` already include these columns.

## Run locally on Windows

Install .NET 8 SDK and MySQL 8. Start the MySQL service. From PowerShell in this folder, choose an admin email and a unique password, then run:

```powershell
./run-local.ps1 -AdminEmail 'staff@ccn.com.sg' -AdminPassword 'Choose-A-Long-Unique-Password'
```

The launcher creates or resets a restricted local MySQL user, sets connection secrets for the running process, and starts the portal at `http://127.0.0.1:5080`. It assumes a local MySQL `root` account without a password; edit `run-local.ps1` if the local MySQL installation uses a different root setup. The admin credentials are not written to the project files.

Sign in at `http://127.0.0.1:5080/Admin/Login`. The enquiries dashboard is at `http://127.0.0.1:5080/Admin` after sign-in.

Alternatively, provide the following environment variables and run `dotnet run`:

- `ConnectionStrings__DefaultConnection`
- `Admin__Email`
- `Admin__Password`

## Production deployment

Use HTTPS, a strong admin password stored in a secret manager, a least-privilege MySQL account, and an encrypted database connection (`SslMode=Required`). Configure a persistent data-protection key store for the deployment identity. Do not use the local launcher or its `SslMode=None` connection string in production. Restrict and back up the `contact_inquiries` table because it contains business contact data.

## Content and scope

Product names and broad capabilities are based on CCN's public site. Product descriptions are concise summaries for discovery and should be reviewed by CCN product owners before publication. This portal collects enquiries; it does not implement live cargo booking, shipment tracking, TradeNet declarations, payment processing, insurance binding, or authenticated customer integrations. Those require CCN system access, API specifications and business approval.
