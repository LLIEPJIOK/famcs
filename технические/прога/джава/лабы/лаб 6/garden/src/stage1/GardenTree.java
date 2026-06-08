package stage1;

import java.io.Serializable;

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


    public GardenTree(Type type) {
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
            System.out.println("Tree " + treeNumber + " is being transplanted.");
            isFruiting = true;
        } else {
            System.out.println("Tree " + treeNumber + " does not need to be transplanted yet.");
        }
    }

    public String toString() {
        return "Number: " + treeNumber + ", type: " + treeType.toString() + ", age: " +
                age + ", isFruiting: " + (isFruiting ? "yes" : "no");
    }
}