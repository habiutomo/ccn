using CcnPortal.Data;
using CcnPortal.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace CcnPortal.Pages.Products;

public sealed class IndexModel(PortalDbContext db) : PageModel
{
    public string? Q { get; private set; }
    public string? Category { get; private set; }
    public string? Audience { get; private set; }
    public IReadOnlyList<Product> Products { get; private set; } = [];
    public IReadOnlyList<string> Categories { get; private set; } = [];

    public async Task OnGetAsync(string? q, string? category, string? audience, CancellationToken cancellationToken)
    {
        Q = q?.Trim();
        Category = category;
        Audience = audience;
        var query = db.Products.AsNoTracking().AsQueryable();
        if (!string.IsNullOrWhiteSpace(Q))
            query = query.Where(p => p.Name.Contains(Q) || p.Summary.Contains(Q) || p.Category.Contains(Q));
        if (!string.IsNullOrWhiteSpace(Category)) query = query.Where(p => p.Category == Category);
        if (!string.IsNullOrWhiteSpace(Audience)) query = query.Where(p => p.Audience.Contains(Audience));
        Products = await query.OrderBy(p => p.SortOrder).ThenBy(p => p.Name).ToListAsync(cancellationToken);
        Categories = await db.Products.AsNoTracking().Select(p => p.Category).Distinct().OrderBy(c => c).ToListAsync(cancellationToken);
    }
}
