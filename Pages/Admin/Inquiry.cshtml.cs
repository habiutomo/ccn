using CcnPortal.Data;
using CcnPortal.Models;
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace CcnPortal.Pages.Admin;

public sealed class InquiryModel(PortalDbContext db) : PageModel
{
    private static readonly string[] AllowedStatuses = ["new", "in_progress", "answered", "closed"];
    public ContactInquiry? Enquiry { get; private set; }
    [BindProperty] public long Id { get; set; }
    [BindProperty] public string Status { get; set; } = "new";
    [BindProperty, StringLength(100)] public string? AssignedTo { get; set; }
    [BindProperty, StringLength(4000)] public string? InternalNotes { get; set; }
    [TempData] public string? Notice { get; set; }

    public async Task<IActionResult> OnGetAsync(long id, CancellationToken cancellationToken)
    {
        var enquiry = await db.ContactInquiries.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id, cancellationToken);
        if (enquiry is null) return NotFound();
        Load(enquiry);
        return Page();
    }

    public async Task<IActionResult> OnPostSaveAsync(CancellationToken cancellationToken)
    {
        if (!AllowedStatuses.Contains(Status)) return BadRequest();
        if (!ModelState.IsValid) return await OnGetAsync(Id, cancellationToken);
        var enquiry = await db.ContactInquiries.FirstOrDefaultAsync(x => x.Id == Id, cancellationToken);
        if (enquiry is null) return NotFound();
        enquiry.Status = Status;
        enquiry.AssignedTo = string.IsNullOrWhiteSpace(AssignedTo) ? null : AssignedTo.Trim();
        enquiry.InternalNotes = string.IsNullOrWhiteSpace(InternalNotes) ? null : InternalNotes.Trim();
        enquiry.UpdatedAt = DateTime.UtcNow;
        await db.SaveChangesAsync(cancellationToken);
        Notice = "Enquiry details saved.";
        return RedirectToPage(new { id = Id });
    }

    private void Load(ContactInquiry enquiry)
    {
        Enquiry = enquiry;
        Id = enquiry.Id;
        Status = enquiry.Status;
        AssignedTo = enquiry.AssignedTo;
        InternalNotes = enquiry.InternalNotes;
    }
}
