package stage2;

import java.io.Serial;
import java.io.Serializable;
import java.text.DateFormat;
import java.util.Date;

public abstract class Employee implements Serializable {

    public enum Role {
        MANAGER,
        ANALYST,
        DEVELOPER,
        TESTER,
        DESIGNER
    }

    @Serial
    private static final long serialVersionUID = -4741267363448938757L;
    private final String name;
    private final int age;
    private double salary;
    protected Role employeeRole;
    public final Date creationDate = new Date();

    public Employee(Role role, String name, int age, double salary) {
        this.name = name;
        this.age = age;
        this.salary = salary;
        this.employeeRole = role;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    public String getCreationDate() {
        DateFormat dateFormatter = DateFormat.getDateTimeInstance(
                DateFormat.DEFAULT, DateFormat.DEFAULT, AppLocale.get());
        return dateFormatter.format(creationDate);
    }

    public abstract void work();

    @Override
    public String toString() {
        return AppLocale.getString(AppLocale.name) + ": " + name + ", " +
                AppLocale.getString(AppLocale.age) + ": " + age + ", " +
                AppLocale.getString(AppLocale.salary) + ": $" + salary + ", " +
                AppLocale.getString(AppLocale.role) + ": " + employeeRole.toString() + ", " +
                AppLocale.getString(AppLocale.creation) + ": " + getCreationDate();
    }

}
