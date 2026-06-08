using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using app.Services;
using app.Grpc.Players;

namespace app.Pages.Rosters;

public class DetailsModel : PageModel
{
    private readonly RosterHttpClient _grpcClient;

    public Player Player { get; set; } = new Player();

    public DetailsModel(RosterHttpClient grpcClient)
    {
        _grpcClient = grpcClient;
    }

    public async Task<IActionResult> OnGetAsync(string id)
    {
        if (id == null)
        {
            return NotFound();
        }

        Player = await _grpcClient.GetPlayerAsync(id);
        if (Player == null)
        {
            return NotFound();
        }
        return Page();
    }
}
