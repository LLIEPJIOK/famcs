package stage2;

public class PearTree extends GardenTree {

    private static final long serialVersionUID = -868517587696779085L;

    public PearTree() {
        super(GardenTree.Type.PEAR, 0, false);
    }

    public PearTree(int age, boolean isFruiting) {
        super(GardenTree.Type.PEAR, age, isFruiting);
    }
}