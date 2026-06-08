package stage1;

import java.io.Serial;

public class Designer extends Employee {
    @Serial
    private static final long serialVersionUID = 3742889772123546456L;
    private final String tool;

    public Designer(String name, int age, double salary, String tool) {
        super(Role.DESIGNER, name, age, salary);
        this.tool = tool;
    }

    public String getTool() {
        return tool;
    }

    @Override
    public void work() {
        System.out.println(getName() + " is designing using " + tool + ".");
    }
}
