package stage2;

import java.util.*;
import java.io.*;

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

    static Locale createLocale(String[] args) {
        if (args.length == 2) {
            return new Locale(args[0], args[1]);
        }
        if (args.length == 4) {
            return new Locale(args[2], args[3]);
        }
        return null;
    }

    static void setupConsole(String[] args) {
        if (args.length >= 2) {
            if (args[0].equals("-encoding")) {
                try {
                    System.setOut(new PrintStream(System.out, true, args[1]));
                } catch (UnsupportedEncodingException ex) {
                    System.err.println("Unsupported encoding: " + args[1]);
                    System.exit(1);
                }
            }
        }
    }

    public static void main(String[] args) {

        try {
            setupConsole(args);
            Locale loc = createLocale(args);
            if (loc == null) {
                System.err.println("Invalid argument(s)\n"
                        + "Syntax: [-encoding ENCODING_ID] language country\n"
                        + "Example: -encoding Cp855 be BY");
                System.exit(1);
            }
            AppLocale.set(loc);
            Connector con = new Connector(new File("garden.dat"));
            con.write(createEmployees());
            Employee[] garden = con.read();

            System.out.println(AppLocale.getString(AppLocale.employees) + ":");
            for (Employee e : garden) {
                System.out.println(e);
            }
            System.out.println();
            for (Employee e : garden) {
                e.work();
            }
        } catch (Exception e) {
            System.err.println(e);
        }
    }
}