using System.ComponentModel.DataAnnotations;

namespace CcnPortal.Models;

public sealed class ContactInquiry
{
    public long Id { get; set; }
    [Required, StringLength(120)] public string Name { get; set; } = "";
    [Required, StringLength(160)] public string Company { get; set; } = "";
    [Required, StringLength(100)] public string OrganizationType { get; set; } = "";
    [Required, StringLength(80)] public string Country { get; set; } = "";
    [Required, EmailAddress, StringLength(190)] public string Email { get; set; } = "";
    [Phone, StringLength(40)] public string? Phone { get; set; }
    [Required, StringLength(140)] public string ProductInterest { get; set; } = "";
    [Required, StringLength(180)] public string Subject { get; set; } = "";
    [Required, StringLength(5000, MinimumLength = 10)] public string Message { get; set; } = "";
    [StringLength(100)] public string? AssignedTo { get; set; }
    [StringLength(4000)] public string? InternalNotes { get; set; }
    public string Status { get; set; } = "new";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
}
