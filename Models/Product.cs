namespace CcnPortal.Models;

public sealed class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Slug { get; set; } = "";
    public string Category { get; set; } = "";
    public string Summary { get; set; } = "";
    public string Audience { get; set; } = "";
    public string? Url { get; set; }
    public bool IsFeatured { get; set; }
    public int SortOrder { get; set; }
}
