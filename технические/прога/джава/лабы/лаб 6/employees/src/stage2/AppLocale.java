package stage2;

import java.util.*;

public class AppLocale {
    private static final String strMsg = "Msg";
    private static Locale loc = Locale.getDefault();
    private static ResourceBundle res =
            ResourceBundle.getBundle(AppLocale.strMsg, AppLocale.loc);

    static Locale get() {
        return AppLocale.loc;
    }

    static void set(Locale loc) {
        AppLocale.loc = loc;
        res = ResourceBundle.getBundle(AppLocale.strMsg, AppLocale.loc);
    }

    static ResourceBundle getBundle() {
        return AppLocale.res;
    }

    static String getString(String key) {
        return AppLocale.res.getString(key);
    }

    public static final String employees = "employees";
    public static final String name = "name";
    public static final String age = "age";
    public static final String salary = "salary";
    public static final String role = "role";
    public static final String creation = "creation";
    public static final String analyst = "analyst";
    public static final String designer = "designer";
    public static final String developer = "developer";
    public static final String manager = "manager";
    public static final String members = "members";
    public static final String writes = "writes";
    public static final String autoTest = "autoTest";
    public static final String manualTests = "manualTests";
}
