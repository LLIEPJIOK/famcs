package stage2;

import java.io.Serializable;
import java.text.DateFormat;
import java.util.Date;

public class GardenTree implements Serializable {

    public static enum Type {
        APPLE, CHERRY, PEAR, PLUM, ROWAN
    }

    private static final long serialVersionUID = -4741267363448938757L;
    private static int counter = 0;
    protected int treeNumber;
    protected Type treeType;
    protected int age;
    protected boolean isFruiting;
    public final Date creationDate = new Date();

    public int getTreeNumber() {
        return treeNumber;
    }

    public Type getTreeType() {
        return treeType;
    }

    public int getAge() {
        return age;
    }

    public boolean getIsFruiting() {
        return isFruiting;
    }

    public String getCreationDate() {
        DateFormat dateFormatter = DateFormat.getDateTimeInstance(
                DateFormat.DEFAULT, DateFormat.DEFAULT, AppLocale.get());
        return dateFormatter.format(creationDate);
    }


    protected GardenTree(Type type) {
        this.treeNumber = ++counter;
        this.treeType = type;
        this.age = 0;
        this.isFruiting = false;
    }

    public GardenTree(Type type, int age, boolean isFruiting) {
        this.treeNumber = ++counter;
        this.treeType = type;
        this.age = age;
        this.isFruiting = isFruiting;
    }

    public void transplant() {
        if (age > 5 && !isFruiting) {
            System.out.println(AppLocale.getString(AppLocale.tree) + " " + treeNumber + " " +
                    AppLocale.getString(AppLocale.transplant));
            isFruiting = true;
        } else {
            System.out.println(AppLocale.getString(AppLocale.tree) + " " + treeNumber + " " +
                    AppLocale.getString(AppLocale.notTransplant));
        }
    }

    public String toString() {
        return AppLocale.getString(AppLocale.number) + ": " + treeNumber + ", " +
                AppLocale.getString(AppLocale.type) + ": " + treeType.toString() + ", " +
                AppLocale.getString(AppLocale.age) + ": " + age + ", " +
                AppLocale.getString(AppLocale.isFruiting) + ": " +
                (isFruiting ? AppLocale.getString(AppLocale.yes) : AppLocale.getString(AppLocale.no)) +
                ", " +
                AppLocale.getString(AppLocale.creation) + ": " + getCreationDate();
    }
}