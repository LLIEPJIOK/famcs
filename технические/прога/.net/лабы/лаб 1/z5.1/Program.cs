var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

int requestCount = 0;

app.Use(async (context, next) =>
{
    if (context.Request.Path == "/request")
    {
    		int requestNumber = Interlocked.Increment(ref requestCount);

				string requestType = requestNumber % 2 == 0 ? "Even request" : "Odd request";

				await context.Response.WriteAsync($"Request #{requestNumber}: {requestType}");
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
