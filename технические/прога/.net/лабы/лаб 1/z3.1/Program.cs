var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Use(async (context, next) =>
{
    if (context.Request.Path == "/date")
    {
        string currentDate = DateTime.Now.ToString("dd.MM.yyyy HH:mm:ss");
        await context.Response.WriteAsync($"Current date and time: {currentDate}");
    }
    else
    {
        await next();
    }
});

app.Run(async context =>
{
    context.Response.StatusCode = 404;
    await context.Response.WriteAsync("Not Found");
});

app.Run();
