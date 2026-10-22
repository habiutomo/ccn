using CcnPortal.Data;
using CcnPortal.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace CcnPortal.Pages;

public sealed class IndexModel(PortalDbContext db) : PageModel
{
    [BindProperty] public ContactInquiry Input { get; set; } = new();
    [BindProperty] public string Website { get; set; } = "";
    [TempData] public bool Sent { get; set; }
    public IReadOnlyList<Product> Products { get; private set; } = [];

    public async Task OnGetAsync(CancellationToken cancellationToken) =>
        Products = await db.Products.AsNoTracking().OrderBy(p => p.SortOrder).ToListAsync(cancellationToken);

    public async Task<IActionResult> OnPostAsync(CancellationToken cancellationToken)
    {
        if (!string.IsNullOrWhiteSpace(Website))
        {
            Sent = true;
            return Redirect("/#contact");
        }
        if (!ModelState.IsValid)
        {
            Products = await db.Products.AsNoTracking().OrderBy(p => p.SortOrder).ToListAsync(cancellationToken);
            return Page();
        }
        Input.CreatedAt = DateTime.UtcNow;
        Input.Status = "new";
        db.ContactInquiries.Add(Input);
        await db.SaveChangesAsync(cancellationToken);
        Sent = true;
        return Redirect("/#contact");
    }
}
