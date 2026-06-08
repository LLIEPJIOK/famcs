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

    public static final String type = "type";
    public static final String creation = "creation";
    public static final String number = "number";
    public static final String age = "age";
    public static final String isFruiting = "isFruiting";
    public static final String yes = "yes";
    public static final String no = "no";
    public static final String theGarden = "theGarden";
    public static final String tree = "tree";
    public static final String transplant = "transplant";
    public static final String notTransplant = "notTransplant";
}
