package stage1;

public class RowanTree extends GardenTree {

    private static final long serialVersionUID = 3742889772123546456L;

    public RowanTree() {
        super(GardenTree.Type.ROWAN, 0, false);
    }

    public RowanTree(int age, boolean isFruiting) {
        super(GardenTree.Type.ROWAN, age, isFruiting);
    }
}