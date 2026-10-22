using CcnPortal.Data;
using CcnPortal.Models;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace CcnPortal.Pages.Admin;

public sealed class IndexModel(PortalDbContext db) : PageModel
{
    public int TotalEnquiries { get; private set; }
    public int NewEnquiries { get; private set; }
    public int InProgressEnquiries { get; private set; }
    public int AnsweredEnquiries { get; private set; }
    public int ClosedEnquiries { get; private set; }
    public IReadOnlyList<ContactInquiry> Recent { get; private set; } = [];

    public async Task OnGetAsync(CancellationToken cancellationToken)
    {
        TotalEnquiries = await db.ContactInquiries.CountAsync(cancellationToken);
        NewEnquiries = await db.ContactInquiries.CountAsync(x => x.Status == "new", cancellationToken);
        InProgressEnquiries = await db.ContactInquiries.CountAsync(x => x.Status == "in_progress", cancellationToken);
        AnsweredEnquiries = await db.ContactInquiries.CountAsync(x => x.Status == "answered", cancellationToken);
        ClosedEnquiries = await db.ContactInquiries.CountAsync(x => x.Status == "closed", cancellationToken);
        Recent = await db.ContactInquiries.AsNoTracking().OrderByDescending(x => x.CreatedAt).Take(8).ToListAsync(cancellationToken);
    }

    public async Task<IActionResult> OnPostLogoutAsync()
    {
        await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
        return RedirectToPage("/Admin/Login");
    }
}
