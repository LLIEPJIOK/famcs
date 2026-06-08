package stage2;

public class PlumTree extends GardenTree {

    private static final long serialVersionUID = 7094319283019512927L;

    public PlumTree() {
        super(GardenTree.Type.PLUM, 0, false);
    }

    public PlumTree(int age, boolean isFruiting) {
        super(GardenTree.Type.PLUM, age, isFruiting);
    }
}