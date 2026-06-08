using asp_lab4.Areas.Identity.Data;
using asp_lab4.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace asp_lab4.Controllers
{
    [Authorize]
    public class RostersController : Controller
    {
        private readonly IdentityContext _context;

        public RostersController(IdentityContext context)
        {
            _context = context;
        }

        // GET: Rosters
        public async Task<IActionResult> Index()
        {
            return View(await _context.Rosters.ToListAsync());
        }

        // GET: Rosters/Details/5
        public async Task<IActionResult> Details(string id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var roster = await _context.Rosters
                .FirstOrDefaultAsync(m => m.PlayerId == id);
            if (roster == null)
            {
                return NotFound();
            }

            return View(roster);
        }

        // GET: Rosters/Create
        [Authorize(Roles = "Admin")]
        public IActionResult Create()
        {
            return View();
        }

        // POST: Rosters/Create
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Create([Bind("PlayerId,Jersey,Fname,Sname,Position,Birthday,Weight,Height,BirthCity,BirthState")] Roster roster)
        {
            if (ModelState.IsValid)
            {
                _context.Add(roster);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            return View(roster);
        }

        // GET: Rosters/Edit/5
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Edit(string id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var roster = await _context.Rosters.FindAsync(id);
            if (roster == null)
            {
                return NotFound();
            }
            return View(roster);
        }

        // POST: Rosters/Edit/5
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Edit(string id, [Bind("PlayerId,Jersey,Fname,Sname,Position,Birthday,Weight,Height,BirthCity,BirthState")] Roster roster)
        {
            if (id != roster.PlayerId)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    _context.Update(roster);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!RosterExists(roster.PlayerId))
                    {
                        return NotFound();
                    }
                    else
                    {
                        throw;
                    }
                }
                return RedirectToAction(nameof(Index));
            }
            return View(roster);
        }

        // GET: Rosters/Delete/5
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> Delete(string id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var roster = await _context.Rosters
                .FirstOrDefaultAsync(m => m.PlayerId == id);
            if (roster == null)
            {
                return NotFound();
            }

            return View(roster);
        }

        // POST: Rosters/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> DeleteConfirmed(string id)
        {
            var roster = await _context.Rosters.FindAsync(id);
            if (roster != null)
            {
                _context.Rosters.Remove(roster);
            }

            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        private bool RosterExists(string id)
        {
            return _context.Rosters.Any(e => e.PlayerId == id);
        }
    }
}
