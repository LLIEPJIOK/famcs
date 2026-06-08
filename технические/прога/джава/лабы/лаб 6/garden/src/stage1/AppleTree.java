package stage1;

public class AppleTree extends GardenTree {

    private static final long serialVersionUID = -3949314371553731193L;

    public AppleTree() {
        super(GardenTree.Type.APPLE, 0, false);
    }

    public AppleTree(int age, boolean isFruiting) {
        super(GardenTree.Type.APPLE, age, isFruiting);
    }
}