package stage2;

import java.io.Serial;

public class Analyst extends Employee {
    @Serial
    private static final long serialVersionUID = -868517587696779085L;

    private final String specialization;

    public Analyst(String name, int age, double salary, String specialization) {
        super(Role.ANALYST, name, age, salary);
        this.specialization = specialization;
    }

    public String getSpecialization() {
        return specialization;
    }

    @Override
    public void work() {
        System.out.println(getName() + " " + AppLocale.getString(AppLocale.analyst) + " " + specialization + ".");
    }
}