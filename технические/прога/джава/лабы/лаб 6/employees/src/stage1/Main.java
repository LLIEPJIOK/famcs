package stage1;

import java.io.File;

public class Main {
    public static Employee[] createEmployees() {
        Employee[] employees = new Employee[5];
        employees[0] = new Analyst("Alice", 30, 65000, "financial systems");
        employees[1] = new Designer("Mike", 35, 60000, "Figma");
        employees[2] = new Developer("Bob", 25, 70000, "Java");
        employees[3] = new Manager("John", 40, 80000, 10);
        employees[4] = new Tester("Eve", 28, 55000, true);
        return employees;
    }

    public static void main(String[] args) {
        try {
            Connector con = new Connector(new File("employee.dat"));
            con.write(createEmployees());

            Employee[] garden = con.read();
            System.out.println("Employees: ");
            for (Employee n : garden) {
                System.out.println(n);
            }

            System.out.println();
            for (Employee n : garden) {
                n.work();
            }
        } catch (Exception e) {
            System.err.println(e);
        }
    }
}