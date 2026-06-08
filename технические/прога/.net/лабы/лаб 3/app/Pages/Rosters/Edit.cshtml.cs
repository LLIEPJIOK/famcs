using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using app.Services;
using app.Grpc.Players;

namespace app.Pages.Rosters;

public class EditModel : PageModel
{
    private readonly RosterHttpClient _grpcClient;

    [BindProperty]
    public Player Player { get; set; } = new Player();

    public EditModel(RosterHttpClient grpcClient)
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

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            return Page();
        }

        await _grpcClient.UpdatePlayerAsync(Player);

        return RedirectToPage("./Index");
    }
}
