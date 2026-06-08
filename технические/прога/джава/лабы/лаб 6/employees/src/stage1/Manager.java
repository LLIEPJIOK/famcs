package stage1;

import java.io.Serial;

public class Manager extends Employee {
    @Serial
    private static final long serialVersionUID = 7094319283019512927L;
    private final int teamSize;

    public Manager(String name, int age, double salary, int teamSize) {
        super(Role.MANAGER, name, age, salary);
        this.teamSize = teamSize;
    }

    public int getTeamSize() {
        return teamSize;
    }

    @Override
    public void work() {
        System.out.println(getName() + " is managing a team of " + teamSize + " members.");
    }
}