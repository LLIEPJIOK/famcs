using asp_lab4.Areas.Identity.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace asp_lab4.Controllers;

[Authorize(Roles = "Admin")]
public class UsersController : Controller
{
    private readonly UserManager<User> _userManager;
    private readonly RoleManager<IdentityRole> _roleManager;

    public UsersController(UserManager<User> userManager, RoleManager<IdentityRole> roleManager)
    {
        _userManager = userManager;
        _roleManager = roleManager;
    }

    // GET: UsersController
    public async Task<IActionResult> Index()
    {
        var users = _userManager.Users.ToList();
        return View(users);
    }

    // GET: UsersController/Details/5
    public async Task<IActionResult> Details(string id)
    {
        if (string.IsNullOrEmpty(id))
            return BadRequest();

        var user = await _userManager.FindByIdAsync(id);
        if (user == null)
            return NotFound();

        var roles = await _userManager.GetRolesAsync(user);
        ViewBag.Roles = roles;

        return View(user);
    }


    // GET: UsersController/Edit/5
    public async Task<IActionResult> Edit(string id)
    {
        if (string.IsNullOrEmpty(id))
            return BadRequest();

        var user = await _userManager.FindByIdAsync(id);
        if (user == null)
            return NotFound();

        var userRoles = await _userManager.GetRolesAsync(user);
        ViewBag.AllRoles = _roleManager.Roles.Select(r => r.Name).ToList();
        ViewBag.UserRoles = userRoles;

        return View(user);
    }

    // POST: UsersController/Edit/5
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(string id, string email, string[] roles)
    {
        if (string.IsNullOrEmpty(id))
            return BadRequest();

        var user = await _userManager.FindByIdAsync(id);
        if (user == null)
            return NotFound();

        user.Email = email;
        user.UserName = email;
        var updateResult = await _userManager.UpdateAsync(user);
        if (!updateResult.Succeeded)
        {
            foreach (var error in updateResult.Errors)
                ModelState.AddModelError(string.Empty, error.Description);

            var userRoles = await _userManager.GetRolesAsync(user);
            ViewBag.AllRoles = _roleManager.Roles.Select(r => r.Name).ToList();
            ViewBag.UserRoles = userRoles;
            return View(user);
        }

        var currentRoles = await _userManager.GetRolesAsync(user);
        var rolesToAdd = roles.Except(currentRoles);
        var rolesToRemove = currentRoles.Except(roles);

        if (rolesToAdd.Any())
            await _userManager.AddToRolesAsync(user, rolesToAdd);

        if (rolesToRemove.Any())
            await _userManager.RemoveFromRolesAsync(user, rolesToRemove);

        return RedirectToAction(nameof(Index));
    }
}
