using asp_lab4.Areas.Identity.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using System.Net;

var builder = WebApplication.CreateBuilder(args);
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection") ?? throw new InvalidOperationException("Connection string 'IdentityContextConnection' not found.");

builder.Services.AddDbContext<IdentityContext>(options => options.UseSqlServer(connectionString));

builder.Services
    .AddDefaultIdentity<User>(options => options.SignIn.RequireConfirmedAccount = true)
    .AddRoles<IdentityRole>()
    .AddEntityFrameworkStores<IdentityContext>();

// Add services to the container.
builder.Services.AddControllersWithViews();

builder.Services.AddAuthentication().AddGoogle(opts =>
{
    opts.ClientId = builder.Configuration["Authentication:Google:ClientId"];
    opts.ClientSecret = builder.Configuration["Authentication:Google:ClientSecret"];
});

var app = builder.Build();

var allowedDomains = builder.Configuration
    .GetSection("AllowedDomains")
    .Get<List<string>>()!
    .Select(d => d.ToLowerInvariant())
    .ToHashSet();

var blockedIPs = builder.Configuration
    .GetSection("BlockedIPs")
    .Get<List<string>>()!
    .Select(IPAddress.Parse)
    .ToHashSet();

app.Use(async (context, next) =>
{
    var hostHeader = context.Request.Host.Host;

    // Если Host — доменное имя, проверяем AllowedDomains
    if (!IPAddress.TryParse(hostHeader, out var hostIp))
    {
        var hostName = hostHeader.ToLowerInvariant();
        if (!allowedDomains.Contains(hostName))
        {
            context.Response.StatusCode = StatusCodes.Status403Forbidden;
            await context.Response.WriteAsync($"Access forbidden: domain '{hostName}' is not allowed.");
            return;
        }
    }

    // Проверяем IP клиента
    var remoteIp = context.Connection.RemoteIpAddress;
    if (remoteIp is not null)
    {
        if (blockedIPs.Contains(remoteIp))
        {
            context.Response.StatusCode = StatusCodes.Status403Forbidden;
            await context.Response.WriteAsync($"Access forbidden: client IP '{remoteIp}' is blocked.");
            return;
        }
    }

    await next();
});


// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.MapRazorPages();

app.Run();
