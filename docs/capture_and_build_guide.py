from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from playwright.sync_api import sync_playwright
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SHOTS = DOCS / "screenshots"
PDF = DOCS / "CCN-Portal-User-Guide.pdf"
BASE_URL = os.environ.get("CCN_PORTAL_URL", "http://127.0.0.1:5080")
ADMIN_EMAIL = os.environ["CCN_ADMIN_EMAIL"]
ADMIN_PASSWORD = os.environ["CCN_ADMIN_PASSWORD"]
SHOTS.mkdir(parents=True, exist_ok=True)


def capture_screenshots() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 980}, device_scale_factor=1)
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(700)
        page.screenshot(path=str(SHOTS / "01-homepage.png"))

        page.goto(f"{BASE_URL}/products", wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        page.screenshot(path=str(SHOTS / "02-solution-catalogue.png"))

        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.locator("#contact").scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        page.screenshot(path=str(SHOTS / "03-enquiry-form.png"))

        page.goto(f"{BASE_URL}/Admin/Login", wait_until="domcontentloaded")
        page.locator('input[name="Input.Email"]').fill(ADMIN_EMAIL)
        page.locator('input[name="Input.Password"]').fill(ADMIN_PASSWORD)
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_url("**/Admin**")
        page.wait_for_timeout(350)
        page.screenshot(path=str(SHOTS / "04-admin-dashboard.png"))

        page.goto(f"{BASE_URL}/Admin/Inquiries", wait_until="domcontentloaded")
        page.wait_for_timeout(350)
        page.screenshot(path=str(SHOTS / "05-admin-enquiries.png"))
        detail_link = page.locator('a[href*="/Admin/Inquiry?id="]').first
        if detail_link.count():
            detail_link.click()
            page.wait_for_url("**/Admin/Inquiry**")
            page.screenshot(path=str(SHOTS / "06-enquiry-follow-up.png"), full_page=True)
        browser.close()


def build_pdf() -> None:
    navy = colors.HexColor("#092b3c")
    teal = colors.HexColor("#69d2c0")
    ink = colors.HexColor("#18313b")
    muted = colors.HexColor("#66777c")
    pale = colors.HexColor("#edf1e7")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27, leading=32, textColor=navy, alignment=TA_LEFT, spaceAfter=8))
    styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=12, leading=18, textColor=muted, spaceAfter=12))
    styles.add(ParagraphStyle(name="H1CCN", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=19, leading=24, textColor=navy, spaceBefore=0, spaceAfter=10))
    styles.add(ParagraphStyle(name="H2CCN", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=ink, spaceBefore=8, spaceAfter=5))
    styles.add(ParagraphStyle(name="BodyCCN", parent=styles["BodyText"], fontSize=9.3, leading=14, textColor=ink, spaceAfter=6))
    styles.add(ParagraphStyle(name="SmallCCN", parent=styles["BodyText"], fontSize=8, leading=11, textColor=muted, spaceAfter=4))
    styles.add(ParagraphStyle(name="CaptionCCN", parent=styles["BodyText"], fontSize=8, leading=11, textColor=muted, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8))
    styles.add(ParagraphStyle(name="StepCCN", parent=styles["BodyText"], fontSize=9, leading=13, textColor=ink, leftIndent=11, firstLineIndent=-11, spaceAfter=5))

    doc = SimpleDocTemplate(str(PDF), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=17 * mm, title="CCN Portal User Guide", author="Cargo Community Network Portal")
    story = []

    def p(text: str, style: str = "BodyCCN") -> Paragraph:
        return Paragraph(text, styles[style])

    def screenshot(name: str, caption: str, max_height: float = 105 * mm) -> list:
        path = SHOTS / name
        image = Image(str(path))
        max_w, max_h = doc.width, max_height
        scale = min(max_w / image.imageWidth, max_h / image.imageHeight)
        image.drawWidth = image.imageWidth * scale
        image.drawHeight = image.imageHeight * scale
        image.hAlign = "CENTER"
        return [image, p(caption, "CaptionCCN")]

    def bullet(text: str) -> Paragraph:
        return p("• " + text, "StepCCN")

    def styled_table(rows: list, widths: list[float]) -> Table:
        table = Table(rows, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), pale), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dbe2dc")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        return table

    story += [Spacer(1, 5 * mm), p("CARGO COMMUNITY NETWORK", "SmallCCN"), p("CCN Portal<br/>User Guide", "CoverTitle"), p("A practical operating guide for exploring cargo solutions, submitting enquiries and managing business follow-up.", "CoverSub")]
    story += [p("Inside this guide", "H2CCN"), bullet("Public portal and solution catalogue."), bullet("Business enquiry submission and staff workflow."), bullet("HeidiSQL database reference and local setup."), bullet("Security, privacy and troubleshooting guidance.")]
    story += [Spacer(1, 2 * mm)] + screenshot("01-homepage.png", "CCN portal home — air cargo community overview.", 83 * mm)
    story += [p("Local portal: http://127.0.0.1:5080 · Staff area: /Admin/Login", "SmallCCN"), p(f"Prepared {date.today().strftime('%d %B %Y')} · English edition · 10 pages", "SmallCCN"), PageBreak()]

    story += [p("1. Portal overview", "H1CCN"), p("The CCN portal is an English-language discovery and enquiry site for Cargo Community Network's air cargo digital solutions. It helps business visitors find the right conversation and gives staff a small workspace to manage incoming enquiries.")]
    overview = [[p("Area", "SmallCCN"), p("What it is for", "SmallCCN")], [p("Home", "SmallCCN"), p("Company and air cargo ecosystem introduction, solution highlights and contact entry point.", "SmallCCN")], [p("Solutions", "SmallCCN"), p("Search and filter the seeded product catalogue by category and cargo-partner audience.", "SmallCCN")], [p("Contact", "SmallCCN"), p("Structured form that records business enquiries in MySQL.", "SmallCCN")], [p("Staff admin", "SmallCCN"), p("Private enquiry dashboard, assignment, internal notes, status updates and CSV export.", "SmallCCN")]]
    story += [styled_table(overview, [31 * mm, doc.width - 31 * mm]), p("Who should use this guide", "H2CCN"), bullet("Business visitors: browse solution summaries and contact CCN about a use case."), bullet("CCN staff: review records, assign follow-up, update status and export the enquiry register."), bullet("Local operators: start the .NET application and inspect the MySQL database with HeidiSQL.")]
    story += [p("Scope at a glance", "H2CCN"), p("This portal handles discovery and enquiry intake. It does not perform live bookings, shipment tracking, customs declarations or customer account transactions. Those require approved CCN services and integrations.") , PageBreak()]

    story += [p("2. Browse the solution catalogue", "H1CCN"), p("Choose <b>Solutions</b> in the navigation or open <b>/products</b>. The catalogue currently contains 20 seeded solution summaries. Use the search box for product names, capabilities or solution areas, then narrow results with the category and cargo-partner filters.")]
    story += [p("A useful search sequence", "H2CCN"), bullet("Start with a workflow term such as booking, compliance, visibility or data exchange."), bullet("Select a solution area to reduce the list to a related capability."), bullet("Choose the closest audience, such as airline, forwarder, shipper, trucker or integrator."), bullet("Open the product link when available, or use Talk to CCN to ask the team for guidance.")]
    story += [Spacer(1, 2 * mm)] + screenshot("02-solution-catalogue.png", "Catalogue with keyword search, solution-area and audience filters.", 91 * mm)
    story += [p("Catalogue notes", "H2CCN"), p("Product summaries are short discovery descriptions. Check official CCN product information for current scope. The source records are in MySQL's <b>products</b> table; changes made directly in HeidiSQL affect the live catalogue and should be reviewed before editing.") , PageBreak()]

    story += [p("3. Submit a business enquiry", "H1CCN"), p("Select <b>Talk to our team</b> or scroll to the Contact section. Provide enough context for CCN to route your request to the right team. A valid submission is saved with status <b>new</b> and a UTC received timestamp.")]
    fields = [[p("Field", "SmallCCN"), p("Guidance", "SmallCCN")], [p("Name and company", "SmallCCN"), p("Use your business identity and organisation name.", "SmallCCN")], [p("Organisation and country", "SmallCCN"), p("Choose the closest cargo-partner type and operating country/region.", "SmallCCN")], [p("Business email", "SmallCCN"), p("Use an address the team can use to reply.", "SmallCCN")], [p("Solution and subject", "SmallCCN"), p("Select an area of interest and describe the request briefly.", "SmallCCN")], [p("Message", "SmallCCN"), p("Explain the workflow, goal and preferred next step. Minimum 10 characters.", "SmallCCN")]]
    story += [styled_table(fields, [39 * mm, doc.width - 39 * mm]), Spacer(1, 2 * mm)] + screenshot("03-enquiry-form.png", "Contact form fields shown on the public portal.", 82 * mm)
    story += [p("After sending", "H2CCN"), p("The page confirms receipt. If the form reports validation errors, correct the marked fields and submit again. Do not include passwords, shipment documents, personal data about third parties or confidential operational details.") , PageBreak()]

    story += [p("4. Staff sign-in and dashboard", "H1CCN"), p("Open <b>/Admin/Login</b> and enter the staff credentials supplied to the local operator. Admin pages require a signed-in session. Credentials are configured outside the source files using environment variables or the local launcher.")]
    story += [bullet("The dashboard counts all enquiries and shows New, In progress, Answered and Closed totals."), bullet("The recent list provides a quick route to the latest enquiry records."), bullet("Select a name or Manage enquiries to open the record/work queue."), bullet("Use Sign out when finished. The cookie session expires after four hours.")]
    story += [Spacer(1, 2 * mm)] + screenshot("04-admin-dashboard.png", "Staff dashboard. The guide screenshot uses illustrative sample data.", 97 * mm)
    story += [p("If sign-in fails", "H2CCN"), p("Confirm that the portal was launched with the same admin email and password you are entering. Restarting with different launcher parameters changes the credentials for that running process. The local launcher does not store them in project files.") , PageBreak()]

    story += [p("5. Work the enquiry queue", "H1CCN"), p("Open <b>Manage enquiries</b>. Search by contact name, company or email; combine search with a status filter to focus on a subset. The list displays 25 records at a time. Previous and Next navigate the result pages.")]
    story += [bullet("Select a contact name to open the full enquiry record."), bullet("Use the inline status control for a quick stage change, or use the detail view for the full follow-up update."), bullet("Export CSV downloads all database enquiries, even when the visible list is filtered or paginated."), bullet("Treat the export as confidential because it contains contact details and enquiry messages.")]
    story += [Spacer(1, 2 * mm)] + screenshot("05-admin-enquiries.png", "Enquiry work queue with search, status filter and CSV export.", 87 * mm)
    status_data = [[p("Status", "SmallCCN"), p("Meaning", "SmallCCN")], [p("New", "SmallCCN"), p("Received and awaiting review.", "SmallCCN")], [p("In progress", "SmallCCN"), p("Owned by the team for active follow-up.", "SmallCCN")], [p("Answered", "SmallCCN"), p("A response has been sent; retain for tracking.", "SmallCCN")], [p("Closed", "SmallCCN"), p("Follow-up is complete.", "SmallCCN")]]
    story += [styled_table(status_data, [35 * mm, doc.width - 35 * mm]), PageBreak()]

    story += [p("6. Assign and document follow-up", "H1CCN"), p("Open a record from the queue or dashboard. The detail page includes submitted business contact information and the full message. In the Follow-up section, set a staff owner or team, choose the current workflow status and record internal handover notes.")]
    story += [bullet("Use a consistent owner name or team label so colleagues can identify responsibility."), bullet("Write concise notes about contact attempts, next action and handover context."), bullet("Internal notes are only for staff; they are not sent to the customer."), bullet("Save follow-up to update the record's last-updated time. The next staff member can use this context.")]
    if (SHOTS / "06-enquiry-follow-up.png").exists():
        story += [Spacer(1, 2 * mm)] + screenshot("06-enquiry-follow-up.png", "Illustrative enquiry detail with assignment, status and internal notes.", 112 * mm)
    story += [p("Privacy reminder", "H2CCN"), p("Keep notes factual and business-appropriate. Do not store passwords, payment data, shipment documents or unnecessary personal information in internal notes.") , PageBreak()]

    story += [p("7. Database reference in HeidiSQL", "H1CCN"), p("The application stores catalogue content and enquiry workflow data in the <b>ccn_portal</b> MySQL database. HeidiSQL can be used to inspect tables and run the supplied setup or migration scripts.")]
    db_rows = [[p("Table", "SmallCCN"), p("Purpose / key fields", "SmallCCN")], [p("products", "SmallCCN"), p("Solution catalogue: name, slug, category, summary, audience, URL and sort order.", "SmallCCN")], [p("contact_inquiries", "SmallCCN"), p("Contact and request: company, email, country, product interest, subject, message and received time.", "SmallCCN")], [p("Follow-up fields", "SmallCCN"), p("On contact_inquiries: status, assigned_to, internal_notes and updated_at.", "SmallCCN")]]
    story += [styled_table(db_rows, [39 * mm, doc.width - 39 * mm]), p("Safe inspection examples", "H2CCN")]
    query_box = Table([[p("USE ccn_portal;<br/>SELECT id, name, company, product_interest, status, created_at<br/>FROM contact_inquiries ORDER BY created_at DESC LIMIT 25;<br/><br/>SELECT category, COUNT(*) AS solution_count<br/>FROM products GROUP BY category ORDER BY category;", "SmallCCN")]], colWidths=[doc.width])
    query_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), pale), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dfd7")), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story += [query_box, p("Use SELECT queries for routine inspection. Avoid editing enquiry rows directly unless you understand the audit and operational impact. Restrict database access to authorised operators.") , PageBreak()]

    story += [p("8. Install, migrate and run locally", "H1CCN"), p("Prerequisites: Windows, .NET 8 SDK, MySQL 8 and HeidiSQL (or another MySQL client). Start the MySQL service before launching the app.")]
    story += [p("Fresh database", "H2CCN"), bullet("In HeidiSQL run <b>01-create-database.sql</b>, then <b>02-create-tables.sql</b>, then <b>04-seed-products.sql</b>."), p("Existing prototype database", "H2CCN"), bullet("Run <b>03-upgrade-existing.sql</b> once, then <b>04-seed-products.sql</b> and <b>05-add-enquiry-follow-up.sql</b> once."), p("Start from PowerShell", "H2CCN")]
    code = Table([[p("./run-local.ps1 -AdminEmail 'staff@ccn.com.sg' -AdminPassword 'Your-Unique-Password'", "SmallCCN")]], colWidths=[doc.width])
    code.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), pale), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dfd7")), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story += [code, Spacer(1, 2 * mm), p("The launcher configures a restricted local MySQL user and starts the site at <b>http://127.0.0.1:5080</b>. Stop it with Ctrl+C. It assumes local MySQL root access without a password; adjust the launcher if your local MySQL authentication differs.")]
    story += [p("Common troubleshooting", "H2CCN"), bullet("Port busy: stop the other local app using 5080 or change the --urls value."), bullet("Database connection error: confirm MySQL is running, the schema exists and scripts were applied in order."), bullet("Unknown column after upgrade: apply migration 05 once, then restart the app."), bullet("Static page changes missing: stop the running process, rebuild and start again."), PageBreak()]

    story += [p("9. Security, privacy and operations", "H1CCN"), p("The current launcher is designed for local development. Before any public deployment, have the hosting, security and privacy configuration reviewed by qualified CCN administrators.")]
    story += [p("Operational checklist", "H2CCN"), bullet("Use HTTPS and secure cookie settings; do not expose the development launcher directly to the internet."), bullet("Store admin credentials in a secret manager and rotate them under the organisation's policy."), bullet("Use encrypted MySQL transport, a least-privilege database account and firewall restrictions."), bullet("Protect and back up the database and ASP.NET data-protection keys; test restore procedures."), bullet("Limit access to CSV exports and enquiry records; define retention and deletion rules."), bullet("Review product content, privacy notice, consent language and contact routing before public launch."), bullet("Add monitoring, error handling, email notifications and audit requirements if operations need them.")]
    story += [p("Implemented safeguards", "H2CCN"), p("The application uses authenticated admin pages, HTTP-only admin cookies, anti-forgery protection on forms, a hidden bot-trap field and request rate limiting. These measures support a prototype but do not replace a deployment security review.")]
    story += [p("Current functional boundary", "H2CCN"), p("The portal collects and manages enquiries. Live air cargo booking, shipment tracking, TradeNet filing, payments, customer accounts, email delivery and CCN system integrations are outside the current implementation and require approved APIs, credentials and business workflows.")]
    story += [Spacer(1, 5 * mm), p("Guide note", "H2CCN"), p("Screenshots of admin pages use illustrative sample data. Product summaries are concise discovery content and should be verified by CCN product owners. For application setup and database scripts, see README.md and the database folder in the project.", "BodyCCN")]

    def page_decor(canvas, document):
        canvas.saveState()
        page_width, page_height = A4
        canvas.setFillColor(navy)
        canvas.rect(0, page_height - 8 * mm, page_width, 8 * mm, stroke=0, fill=1)
        canvas.setFillColor(teal)
        canvas.rect(18 * mm, page_height - 8 * mm, 15 * mm, 1.2 * mm, stroke=0, fill=1)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(muted)
        canvas.drawString(18 * mm, 9 * mm, "Cargo Community Network · CCN Portal")
        canvas.drawRightString(page_width - 18 * mm, 9 * mm, f"{document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=page_decor, onLaterPages=page_decor)


if __name__ == "__main__":
    capture_screenshots()
    build_pdf()
    print(f"Created {PDF}")
