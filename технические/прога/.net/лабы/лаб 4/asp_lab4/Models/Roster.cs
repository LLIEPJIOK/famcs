namespace asp_lab4.Models;

public class Roster
{
    public required string PlayerId { get; set; }
    public short Jersey { get; set; }
    public required string Fname { get; set; }
    public required string Sname { get; set; }
    public required string Position { get; set; }
    public DateTime Birthday { get; set; }
    public short Weight { get; set; }
    public short Height { get; set; }
    public required string BirthCity { get; set; }
    public required string BirthState { get; set; }
}
