using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace app.Migrations
{
    /// <inheritdoc />
    public partial class Procedures : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql(@"
                CREATE PROCEDURE GetRosterByPlayerId
                    @PlayerId NVARCHAR(50)
                AS
                BEGIN
                    SELECT PlayerId, Jersey, Fname, Sname, Position, Birthday, Weight, Height, BirthCity, BirthState
                    FROM Rosters
                    WHERE PlayerId = @PlayerId;
                END;
                GO

                CREATE PROCEDURE DeleteRosterByPlayerId
                    @PlayerId NVARCHAR(50)
                AS
                BEGIN
                    DELETE FROM Rosters
                    WHERE PlayerId = @PlayerId;
                END;
                GO

                CREATE PROCEDURE UpdateRoster
                    @PlayerId NVARCHAR(50),
                    @Jersey SMALLINT,
                    @Fname NVARCHAR(50),
                    @Sname NVARCHAR(50),
                    @Position NVARCHAR(50),
                    @Birthday DATETIME,
                    @Weight SMALLINT,
                    @Height SMALLINT,
                    @BirthCity NVARCHAR(50),
                    @BirthState NVARCHAR(50)
                AS
                BEGIN
                    UPDATE Rosters
                    SET 
                        Jersey = @Jersey,
                        Fname = @Fname,
                        Sname = @Sname,
                        Position = @Position,
                        Birthday = @Birthday,
                        Weight = @Weight,
                        Height = @Height,
                        BirthCity = @BirthCity,
                        BirthState = @BirthState
                    WHERE PlayerId = @PlayerId;
                END;
                GO

                CREATE PROCEDURE InsertRoster
                    @PlayerId NVARCHAR(50),
                    @Jersey SMALLINT,
                    @Fname NVARCHAR(50),
                    @Sname NVARCHAR(50),
                    @Position NVARCHAR(50),
                    @Birthday DATETIME,
                    @Weight SMALLINT,
                    @Height SMALLINT,
                    @BirthCity NVARCHAR(50),
                    @BirthState NVARCHAR(50)
                AS
                BEGIN
                    INSERT INTO Rosters (PlayerId, Jersey, Fname, Sname, Position, Birthday, Weight, Height, BirthCity, BirthState)
                    VALUES (@PlayerId, @Jersey, @Fname, @Sname, @Position, @Birthday, @Weight, @Height, @BirthCity, @BirthState);
                END;
                GO
            ");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql(@"
                DROP PROCEDURE IF EXISTS GetRosterByPlayerId;
                DROP PROCEDURE IF EXISTS DeleteRosterByPlayerId;
                DROP PROCEDURE IF EXISTS UpdateRoster;
                DROP PROCEDURE IF EXISTS InsertRoster;
            ");
        }
    }
}
