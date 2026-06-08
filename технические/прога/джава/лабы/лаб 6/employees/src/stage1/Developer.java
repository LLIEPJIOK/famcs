package stage1;

import java.io.Serial;

public class Developer extends Employee {
    @Serial
    private static final long serialVersionUID = -3949314371553731193L;
    private final String programmingLanguage;

    public Developer(String name, int age, double salary, String programmingLanguage) {
        super(Role.DEVELOPER, name, age, salary);
        this.programmingLanguage = programmingLanguage;
    }

    public String getProgrammingLanguage() {
        return programmingLanguage;
    }

    @Override
    public void work() {
        System.out.println(getName() + " is coding in " + programmingLanguage + ".");
    }
}