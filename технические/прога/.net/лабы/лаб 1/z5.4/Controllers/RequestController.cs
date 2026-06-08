using Microsoft.AspNetCore.Mvc;
using System.Threading;

[Route("request")]
[ApiController]
public class RequestController : ControllerBase
{
    private static int _requestCount = 0;

    [HttpGet]
    public IActionResult GetRequestType()
    {
        int requestNumber = Interlocked.Increment(ref _requestCount);

        string type = requestNumber % 2 == 0 ? "Even request" : "Odd request";
        return Ok($"Request #{requestNumber}: {type}");
    }
}
