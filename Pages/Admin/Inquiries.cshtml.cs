using System.Text;
using CcnPortal.Data;
using CcnPortal.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace CcnPortal.Pages.Admin;

public sealed class InquiriesModel(PortalDbContext db) : PageModel
{
    private static readonly string[] AllowedStatuses = ["new", "in_progress", "answered", "closed"];
    public IReadOnlyList<ContactInquiry> Enquiries { get; private set; } = [];
    public string? StatusFilter { get; private set; }
    public string? Search { get; private set; }
    public int PageNumber { get; private set; } = 1;
    public int TotalCount { get; private set; }
    public int PageCount => Math.Max(1, (int)Math.Ceiling(TotalCount / 25d));
    [TempData] public string? Notice { get; set; }

    public async Task OnGetAsync(string? status, string? q, int page, CancellationToken cancellationToken)
    {
        StatusFilter = status;
        Search = q?.Trim();
        var query = db.ContactInquiries.AsNoTracking().AsQueryable();
        if (!string.IsNullOrWhiteSpace(StatusFilter) && AllowedStatuses.Contains(StatusFilter))
            query = query.Where(x => x.Status == StatusFilter);
        if (!string.IsNullOrWhiteSpace(Search))
            query = query.Where(x => x.Name.Contains(Search) || x.Company!.Contains(Search) || x.Email.Contains(Search));
        TotalCount = await query.CountAsync(cancellationToken);
        PageNumber = Math.Clamp(page, 1, PageCount);
        Enquiries = await query.OrderByDescending(x => x.CreatedAt).Skip((PageNumber - 1) * 25).Take(25).ToListAsync(cancellationToken);
    }

    public async Task<IActionResult> OnPostUpdateAsync(long id, string status, CancellationToken cancellationToken)
    {
        if (!AllowedStatuses.Contains(status)) return BadRequest();
        var enquiry = await db.ContactInquiries.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);
        if (enquiry is null) return NotFound();
        enquiry.Status = status;
        enquiry.UpdatedAt = DateTime.UtcNow;
        await db.SaveChangesAsync(cancellationToken);
        Notice = "Enquiry status updated.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnGetExportAsync(CancellationToken cancellationToken)
    {
        var records = await db.ContactInquiries.AsNoTracking().OrderByDescending(x => x.CreatedAt).ToListAsync(cancellationToken);
        var csv = new StringBuilder("id,received_at,name,company,organization_type,country,email,phone,product_interest,subject,message,status\r\n");
        foreach (var item in records)
        {
            var fields = new[]
            {
                item.Id.ToString(), item.CreatedAt.ToString("O"), item.Name, item.Company ?? "", item.OrganizationType,
                item.Country, item.Email, item.Phone ?? "", item.ProductInterest, item.Subject, item.Message, item.Status
            };
            csv.AppendLine(string.Join(',', fields.Select(CsvField)));
        }
        var bytes = Encoding.UTF8.GetPreamble().Concat(Encoding.UTF8.GetBytes(csv.ToString())).ToArray();
        return File(bytes, "text/csv; charset=utf-8", $"ccn-enquiries-{DateTime.UtcNow:yyyyMMdd}.csv");
    }

    private static string CsvField(string value)
    {
        var safe = value.Length > 0 && "=+-@\t\r".Contains(value[0]) ? "'" + value : value;
        return "\"" + safe.Replace("\"", "\"\"") + "\"";
    }
}
