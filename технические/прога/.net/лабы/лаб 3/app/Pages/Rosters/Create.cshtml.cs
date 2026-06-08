using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using app.Services;
using app.Grpc.Players;
using Google.Protobuf.WellKnownTypes;

namespace app.Pages.Rosters;

public class CreateModel : PageModel
{
    private readonly RosterHttpClient _grpcClient;

    [BindProperty]
    public Player Player { get; set; } = new Player();

    public CreateModel(RosterHttpClient grpcClient)
    {
        _grpcClient = grpcClient;
    }

    public IActionResult OnGet()
    {
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            return Page();
        }

        Player.PlayerId = Guid.NewGuid().ToString();
        await _grpcClient.AddPlayerAsync(Player);

        return RedirectToPage("./Index");
    }
}
