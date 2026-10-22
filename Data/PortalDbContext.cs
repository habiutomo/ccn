using CcnPortal.Models;
using Microsoft.EntityFrameworkCore;

namespace CcnPortal.Data;

public sealed class PortalDbContext(DbContextOptions<PortalDbContext> options) : DbContext(options)
{
    public DbSet<ContactInquiry> ContactInquiries => Set<ContactInquiry>();
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ContactInquiry>(entity =>
        {
            entity.ToTable("contact_inquiries");
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Id).HasColumnName("id");
            entity.Property(x => x.Name).HasColumnName("name").HasMaxLength(120).IsRequired();
            entity.Property(x => x.Company).HasColumnName("company").HasMaxLength(160);
            entity.Property(x => x.OrganizationType).HasColumnName("organization_type").HasMaxLength(100).IsRequired();
            entity.Property(x => x.Country).HasColumnName("country").HasMaxLength(80).IsRequired();
            entity.Property(x => x.Email).HasColumnName("email").HasMaxLength(190).IsRequired();
            entity.Property(x => x.Phone).HasColumnName("phone").HasMaxLength(40);
            entity.Property(x => x.ProductInterest).HasColumnName("product_interest").HasMaxLength(140).IsRequired();
            entity.Property(x => x.Subject).HasColumnName("subject").HasMaxLength(180).IsRequired();
            entity.Property(x => x.Message).HasColumnName("message").HasColumnType("text").IsRequired();
            entity.Property(x => x.AssignedTo).HasColumnName("assigned_to").HasMaxLength(100);
            entity.Property(x => x.InternalNotes).HasColumnName("internal_notes").HasColumnType("text");
            entity.Property(x => x.Status).HasColumnName("status").HasMaxLength(20).HasDefaultValue("new");
            entity.Property(x => x.CreatedAt).HasColumnName("created_at").HasColumnType("datetime");
            entity.Property(x => x.UpdatedAt).HasColumnName("updated_at").HasColumnType("datetime");
            entity.HasIndex(x => x.CreatedAt).HasDatabaseName("ix_contact_inquiries_created_at");
            entity.HasIndex(x => x.Status).HasDatabaseName("ix_contact_inquiries_status");
        });

        modelBuilder.Entity<Product>(entity =>
        {
            entity.ToTable("products");
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Id).HasColumnName("id");
            entity.Property(x => x.Name).HasColumnName("name").HasMaxLength(140).IsRequired();
            entity.Property(x => x.Slug).HasColumnName("slug").HasMaxLength(160).IsRequired();
            entity.Property(x => x.Category).HasColumnName("category").HasMaxLength(80).IsRequired();
            entity.Property(x => x.Summary).HasColumnName("summary").HasMaxLength(500).IsRequired();
            entity.Property(x => x.Audience).HasColumnName("audience").HasMaxLength(180).IsRequired();
            entity.Property(x => x.Url).HasColumnName("url").HasMaxLength(500);
            entity.Property(x => x.IsFeatured).HasColumnName("is_featured").HasDefaultValue(false);
            entity.Property(x => x.SortOrder).HasColumnName("sort_order").HasDefaultValue(0);
            entity.HasIndex(x => x.Slug).IsUnique().HasDatabaseName("ux_products_slug");
            entity.HasIndex(x => new { x.Category, x.SortOrder }).HasDatabaseName("ix_products_category_sort");
        });
    }
}
