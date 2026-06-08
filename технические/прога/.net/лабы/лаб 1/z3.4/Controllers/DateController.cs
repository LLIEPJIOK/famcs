using Microsoft.AspNetCore.Mvc;

[Route("date")]
[ApiController]
public class DateController : ControllerBase
{
    [HttpGet]
    public IActionResult GetDate()
    {
        string currentDate = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
        return Ok($"Current date and time: {currentDate}");
    }
}
