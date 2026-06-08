using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace app.Migrations
{
    /// <inheritdoc />
    public partial class Init : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Rosters",
                columns: table => new
                {
                    PlayerId = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    Jersey = table.Column<short>(type: "smallint", nullable: false),
                    Fname = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Sname = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Position = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Birthday = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Weight = table.Column<short>(type: "smallint", nullable: false),
                    Height = table.Column<short>(type: "smallint", nullable: false),
                    BirthCity = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    BirthState = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Rosters", x => x.PlayerId);
                });

            migrationBuilder.InsertData(
                table: "Rosters",
                columns: new[] { "PlayerId", "BirthCity", "BirthState", "Birthday", "Fname", "Height", "Jersey", "Position", "Sname", "Weight" },
                values: new object[,]
                {
                    { "adamlem", "Stamford", "CT", new DateTime(2001, 9, 21, 0, 0, 0, 0, DateTimeKind.Unspecified), "Mike", (short)197, (short)12, "RW", "Adamle", (short)73 },
                    { "adamles", "Columbus", "OH", new DateTime(1999, 3, 1, 0, 0, 0, 0, DateTimeKind.Unspecified), "Scott", (short)184, (short)17, "D", "Adamle", (short)70 },
                    { "armanova", "Minsk", "RU", new DateTime(1998, 10, 25, 0, 0, 0, 0, DateTimeKind.Unspecified), "Arkady", (short)197, (short)31, "LW", "Armanov", (short)71 },
                    { "boolea", "Kiev", "UK", new DateTime(1997, 9, 14, 0, 0, 0, 0, DateTimeKind.Unspecified), "Alexi", (short)194, (short)8, "RW", "Boole", (short)72 },
                    { "choakd", "Prague", "CZ", new DateTime(1997, 2, 22, 0, 0, 0, 0, DateTimeKind.Unspecified), "Dominick", (short)196, (short)11, "RW", "Choak", (short)72 },
                    { "clobberk", "Bangor", "ME", new DateTime(2002, 6, 21, 0, 0, 0, 0, DateTimeKind.Unspecified), "Kilroy", (short)200, (short)24, "D", "Clobber", (short)73 },
                    { "clubbes", "Paramus", "NJ", new DateTime(1999, 7, 26, 0, 0, 0, 0, DateTimeKind.Unspecified), "Sam", (short)190, (short)7, "LW", "Clubbe", (short)75 },
                    { "finleyp", "Denver", "CO", new DateTime(1987, 6, 8, 0, 0, 0, 0, DateTimeKind.Unspecified), "Peter", (short)194, (short)14, "D", "Finley", (short)76 },
                    { "fiskj", "Helsinki", "FI", new DateTime(2001, 11, 25, 0, 0, 0, 0, DateTimeKind.Unspecified), "Jerke", (short)193, (short)25, "D", "Fisk", (short)71 },
                    { "gruberh", "Munich", "DE", new DateTime(1991, 2, 11, 0, 0, 0, 0, DateTimeKind.Unspecified), "Hans", (short)175, (short)29, "D", "Gruber", (short)70 },
                    { "grunwala", "Buffalo", "NY", new DateTime(1990, 10, 17, 0, 0, 0, 0, DateTimeKind.Unspecified), "Allan", (short)189, (short)6, "C", "Grunwald", (short)74 },
                    { "ivanovv", "Moscow", "RU", new DateTime(2004, 9, 20, 0, 0, 0, 0, DateTimeKind.Unspecified), "Valerei", (short)175, (short)4, "C", "Ivanovich", (short)72 },
                    { "jeffriea", "Springfield", "MA", new DateTime(1995, 11, 8, 0, 0, 0, 0, DateTimeKind.Unspecified), "Angus", (short)185, (short)30, "G", "Jeffries", (short)70 },
                    { "jonesr", "Hartford", "CT", new DateTime(1997, 5, 22, 0, 0, 0, 0, DateTimeKind.Unspecified), "Robert", (short)189, (short)35, "C", "Jones", (short)73 },
                    { "lexourb", "Quincy", "IL", new DateTime(2001, 9, 5, 0, 0, 0, 0, DateTimeKind.Unspecified), "Bruce", (short)198, (short)9, "D", "Lexour", (short)75 },
                    { "lunds", "St. Paul", "MN", new DateTime(1997, 5, 22, 0, 0, 0, 0, DateTimeKind.Unspecified), "Steven", (short)193, (short)93, "D", "Lund", (short)71 },
                    { "maguirea", "Detroit", "MI", new DateTime(1999, 12, 8, 0, 0, 0, 0, DateTimeKind.Unspecified), "Andre", (short)191, (short)34, "LW", "Maguire", (short)75 },
                    { "meyersd", "Chicago", "IL", new DateTime(1998, 2, 11, 0, 0, 0, 0, DateTimeKind.Unspecified), "Doug", (short)195, (short)28, "G", "Meyers", (short)70 },
                    { "olsens", "Stockholm", "SW", new DateTime(1999, 8, 16, 0, 0, 0, 0, DateTimeKind.Unspecified), "Sandish", (short)192, (short)37, "D", "Olsen", (short)72 },
                    { "quivep", "Quebec", "QU", new DateTime(1991, 7, 19, 0, 0, 0, 0, DateTimeKind.Unspecified), "Pierre", (short)197, (short)20, "LW", "Quive", (short)71 },
                    { "springej", "Toronto", "ON", new DateTime(1995, 10, 14, 0, 0, 0, 0, DateTimeKind.Unspecified), "Junior", (short)184, (short)38, "C", "Springer", (short)71 },
                    { "sullivar", "Vancouver", "BC", new DateTime(2000, 3, 8, 0, 0, 0, 0, DateTimeKind.Unspecified), "Russel", (short)186, (short)39, "G", "Sullivan", (short)70 },
                    { "travisj", "Boston", "MA", new DateTime(2003, 6, 23, 0, 0, 0, 0, DateTimeKind.Unspecified), "John", (short)200, (short)19, "C", "Travis", (short)74 },
                    { "zauberz", "Moosehead", "MA", new DateTime(1988, 8, 31, 0, 0, 0, 0, DateTimeKind.Unspecified), "Zeke", (short)203, (short)22, "RW", "Zauber", (short)74 }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Rosters");
        }
    }
}
