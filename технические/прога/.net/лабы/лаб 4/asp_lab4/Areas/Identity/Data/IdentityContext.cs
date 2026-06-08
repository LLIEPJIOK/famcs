using asp_lab4.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace asp_lab4.Areas.Identity.Data;

public class IdentityContext : IdentityDbContext<User>
{
    public IdentityContext(DbContextOptions<IdentityContext> options)
        : base(options)
    {
    }

    public DbSet<Roster> Rosters { get; set; }

    public async Task<List<Roster>> GetRosterByIdAsync(string playerId)
    {
        return await Rosters
            .FromSqlRaw("EXEC GetRosterByPlayerId @p0", playerId)
            .ToListAsync();
    }

    public async Task AddRosterAsync(Roster roster)
    {
        await Database.ExecuteSqlRawAsync(
            "EXEC InsertRoster @p0, @p1, @p2, @p3, @p4, @p5, @p6, @p7, @p8, @p9",
            roster.PlayerId, roster.Jersey, roster.Fname, roster.Sname,
            roster.Position, roster.Birthday, roster.Weight,
            roster.Height, roster.BirthCity,
            roster.BirthState
        );
    }

    public async Task UpdateRosterAsync(Roster roster)
    {
        await Database.ExecuteSqlRawAsync(
            "EXEC UpdateRoster @p0, @p1, @p2, @p3, @p4, @p5, @p6, @p7, @p8, @p9",
            roster.PlayerId, roster.Jersey, roster.Fname, roster.Sname,
            roster.Position, roster.Birthday, roster.Weight,
            roster.Height, roster.BirthCity ?? (object)DBNull.Value,
            roster.BirthState ?? (object)DBNull.Value
        );
    }

    public async Task DeleteRosterAsync(string playerId)
    {
        await Database.ExecuteSqlRawAsync("EXEC DeleteRosterByPlayerId @p0", playerId);
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        modelBuilder.Entity<Roster>()
            .HasKey(r => r.PlayerId);

        modelBuilder.Entity<Roster>().HasData(
            new Roster { PlayerId = "adamlem", Jersey = 12, Fname = "Mike", Sname = "Adamle", Position = "RW", Birthday = new DateTime(2001, 9, 21), Weight = 73, Height = 197, BirthCity = "Stamford", BirthState = "CT" },
            new Roster { PlayerId = "adamles", Jersey = 17, Fname = "Scott", Sname = "Adamle", Position = "D", Birthday = new DateTime(1999, 3, 1), Weight = 70, Height = 184, BirthCity = "Columbus", BirthState = "OH" },
            new Roster { PlayerId = "armanova", Jersey = 31, Fname = "Arkady", Sname = "Armanov", Position = "LW", Birthday = new DateTime(1998, 10, 25), Weight = 71, Height = 197, BirthCity = "Minsk", BirthState = "RU" },
            new Roster { PlayerId = "boolea", Jersey = 8, Fname = "Alexi", Sname = "Boole", Position = "RW", Birthday = new DateTime(1997, 9, 14), Weight = 72, Height = 194, BirthCity = "Kiev", BirthState = "UK" },
            new Roster { PlayerId = "choakd", Jersey = 11, Fname = "Dominick", Sname = "Choak", Position = "RW", Birthday = new DateTime(1997, 2, 22), Weight = 72, Height = 196, BirthCity = "Prague", BirthState = "CZ" },
            new Roster { PlayerId = "clobberk", Jersey = 24, Fname = "Kilroy", Sname = "Clobber", Position = "D", Birthday = new DateTime(2002, 6, 21), Weight = 73, Height = 200, BirthCity = "Bangor", BirthState = "ME" },
            new Roster { PlayerId = "clubbes", Jersey = 7, Fname = "Sam", Sname = "Clubbe", Position = "LW", Birthday = new DateTime(1999, 7, 26), Weight = 75, Height = 190, BirthCity = "Paramus", BirthState = "NJ" },
            new Roster { PlayerId = "finleyp", Jersey = 14, Fname = "Peter", Sname = "Finley", Position = "D", Birthday = new DateTime(1987, 6, 8), Weight = 76, Height = 194, BirthCity = "Denver", BirthState = "CO" },
            new Roster { PlayerId = "fiskj", Jersey = 25, Fname = "Jerke", Sname = "Fisk", Position = "D", Birthday = new DateTime(2001, 11, 25), Weight = 71, Height = 193, BirthCity = "Helsinki", BirthState = "FI" },
            new Roster { PlayerId = "gruberh", Jersey = 29, Fname = "Hans", Sname = "Gruber", Position = "D", Birthday = new DateTime(1991, 2, 11), Weight = 70, Height = 175, BirthCity = "Munich", BirthState = "DE" },
            new Roster { PlayerId = "grunwala", Jersey = 6, Fname = "Allan", Sname = "Grunwald", Position = "C", Birthday = new DateTime(1990, 10, 17), Weight = 74, Height = 189, BirthCity = "Buffalo", BirthState = "NY" },
            new Roster { PlayerId = "ivanovv", Jersey = 4, Fname = "Valerei", Sname = "Ivanovich", Position = "C", Birthday = new DateTime(2004, 9, 20), Weight = 72, Height = 175, BirthCity = "Moscow", BirthState = "RU" },
            new Roster { PlayerId = "jeffriea", Jersey = 30, Fname = "Angus", Sname = "Jeffries", Position = "G", Birthday = new DateTime(1995, 11, 8), Weight = 70, Height = 185, BirthCity = "Springfield", BirthState = "MA" },
            new Roster { PlayerId = "jonesr", Jersey = 35, Fname = "Robert", Sname = "Jones", Position = "C", Birthday = new DateTime(1997, 5, 22), Weight = 73, Height = 189, BirthCity = "Hartford", BirthState = "CT" },
            new Roster { PlayerId = "lexourb", Jersey = 9, Fname = "Bruce", Sname = "Lexour", Position = "D", Birthday = new DateTime(2001, 9, 5), Weight = 75, Height = 198, BirthCity = "Quincy", BirthState = "IL" },
            new Roster { PlayerId = "lunds", Jersey = 93, Fname = "Steven", Sname = "Lund", Position = "D", Birthday = new DateTime(1997, 5, 22), Weight = 71, Height = 193, BirthCity = "St. Paul", BirthState = "MN" },
            new Roster { PlayerId = "maguirea", Jersey = 34, Fname = "Andre", Sname = "Maguire", Position = "LW", Birthday = new DateTime(1999, 12, 8), Weight = 75, Height = 191, BirthCity = "Detroit", BirthState = "MI" },
            new Roster { PlayerId = "meyersd", Jersey = 28, Fname = "Doug", Sname = "Meyers", Position = "G", Birthday = new DateTime(1998, 2, 11), Weight = 70, Height = 195, BirthCity = "Chicago", BirthState = "IL" },
            new Roster { PlayerId = "olsens", Jersey = 37, Fname = "Sandish", Sname = "Olsen", Position = "D", Birthday = new DateTime(1999, 8, 16), Weight = 72, Height = 192, BirthCity = "Stockholm", BirthState = "SW" },
            new Roster { PlayerId = "quivep", Jersey = 20, Fname = "Pierre", Sname = "Quive", Position = "LW", Birthday = new DateTime(1991, 7, 19), Weight = 71, Height = 197, BirthCity = "Quebec", BirthState = "QU" },
            new Roster { PlayerId = "springej", Jersey = 38, Fname = "Junior", Sname = "Springer", Position = "C", Birthday = new DateTime(1995, 10, 14), Weight = 71, Height = 184, BirthCity = "Toronto", BirthState = "ON" },
            new Roster { PlayerId = "sullivar", Jersey = 39, Fname = "Russel", Sname = "Sullivan", Position = "G", Birthday = new DateTime(2000, 3, 8), Weight = 70, Height = 186, BirthCity = "Vancouver", BirthState = "BC" },
            new Roster { PlayerId = "travisj", Jersey = 19, Fname = "John", Sname = "Travis", Position = "C", Birthday = new DateTime(2003, 6, 23), Weight = 74, Height = 200, BirthCity = "Boston", BirthState = "MA" },
            new Roster { PlayerId = "zauberz", Jersey = 22, Fname = "Zeke", Sname = "Zauber", Position = "RW", Birthday = new DateTime(1988, 8, 31), Weight = 74, Height = 203, BirthCity = "Moosehead", BirthState = "MA" }
        );

        modelBuilder.Entity<IdentityRole>().HasData(
            new IdentityRole { Id = "role-admin-id", Name = "Admin", NormalizedName = "ADMIN" },
            new IdentityRole { Id = "role-user-id", Name = "User", NormalizedName = "USER" }
        );
    }
}
