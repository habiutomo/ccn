using System.Security.Claims;
using CcnPortal.Models;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CcnPortal.Pages.Admin;

public sealed class LoginModel(IConfiguration configuration) : PageModel
{
    [BindProperty] public LoginInput Input { get; set; } = new();
    public string? ErrorMessage { get; private set; }

    public void OnGet() { }

    public async Task<IActionResult> OnPostAsync(string? returnUrl = null)
    {
        var adminEmail = configuration["Admin:Email"];
        var adminPassword = configuration["Admin:Password"];
        if (string.IsNullOrWhiteSpace(adminEmail) || string.IsNullOrWhiteSpace(adminPassword))
        {
            ErrorMessage = "Staff sign-in has not been configured for this server.";
            return Page();
        }

        var hasher = new PasswordHasher<object>();
        var passwordHash = hasher.HashPassword(this, adminPassword);
        var passwordCheck = hasher.VerifyHashedPassword(this, passwordHash, Input.Password ?? "");
        if (!string.Equals(Input.Email?.Trim(), adminEmail.Trim(), StringComparison.OrdinalIgnoreCase)
            || passwordCheck == PasswordVerificationResult.Failed)
        {
            ErrorMessage = "Email or password is incorrect.";
            return Page();
        }

        var claims = new[]
        {
            new Claim(ClaimTypes.Name, adminEmail.Trim()),
            new Claim(ClaimTypes.Role, "Admin")
        };
        var identity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);
        await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, new ClaimsPrincipal(identity));

        if (!string.IsNullOrWhiteSpace(returnUrl) && Url.IsLocalUrl(returnUrl)) return LocalRedirect(returnUrl);
        return RedirectToPage("/Admin/Index");
    }

    public sealed class LoginInput
    {
        public string? Email { get; set; }
        public string? Password { get; set; }
    }
}
