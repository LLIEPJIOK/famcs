var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Use(async (HttpContext context, RequestDelegate next) =>
{
    var path = context.Request.Path.Value?.ToLower();

    if (path == "/hello")
    {
        await context.Response.WriteAsync("Hello, world!");
    }
    else
    {
        await next.Invoke(context);
    }
});

app.Use(async (HttpContext context, RequestDelegate next) =>
{
    var path = context.Request.Path.Value?.ToLower();

    if (path == "/goodbye")
    {
        await context.Response.WriteAsync("Goodbye!");
    }
    else
    {
        await next.Invoke(context);
    }
});

app.Use(async (HttpContext context, RequestDelegate next) =>
{
    await next.Invoke(context);
});

app.Run(async context =>
{
    context.Response.StatusCode = 404;
    await context.Response.WriteAsync("Route not found.");
});

app.Run();