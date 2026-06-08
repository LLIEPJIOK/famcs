using Microsoft.AspNetCore.Mvc.RazorPages;
using app.Services;
using app.Grpc.Players;

namespace app.Pages.Rosters;

public class IndexModel : PageModel
{
    private readonly RosterHttpClient _grpcClient;
    public List<Player> Players { get; set; } = new List<Player>();

    public IndexModel(RosterHttpClient grpcClient)
    {
        _grpcClient = grpcClient;
    }

    public async Task OnGetAsync()
    {
        Players = await _grpcClient.ListPlayersAsync();
    }
}
