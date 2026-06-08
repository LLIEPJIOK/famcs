package stage1;

import java.io.Serial;
import java.io.Serializable;

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

    public abstract void work();

    @Override
    public String toString() {
        return "Name: " + name + ", Age: " + age + ", Salary: $" + salary + ", Role: " + employeeRole.toString();
    }
}
