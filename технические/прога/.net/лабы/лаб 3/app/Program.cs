using Microsoft.EntityFrameworkCore;
using app.Services;
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<RosterContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Add gRPC client service
builder.Services.AddSingleton<RosterHttpClient>();

builder.Services.AddRazorPages();

var app = builder.Build();

app.UseRouting();

app.MapRazorPages();

app.Run();
