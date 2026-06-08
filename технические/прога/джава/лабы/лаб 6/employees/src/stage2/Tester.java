package stage2;

import java.io.Serial;

public class Tester extends Employee {
    @Serial
    private static final long serialVersionUID = 2765106927816125373L;
    private final boolean automated;

    public Tester(String name, int age, double salary, boolean automated) {
        super(Role.TESTER, name, age, salary);
        this.automated = automated;
    }

    public boolean isAutomated() {
        return automated;
    }

    @Override
    public void work() {
        System.out.println(getName() + " " + AppLocale.getString(AppLocale.writes) + " " +
                (automated ? AppLocale.getString(AppLocale.autoTest) : AppLocale.getString(AppLocale.manualTests)) + ".");
    }
}
