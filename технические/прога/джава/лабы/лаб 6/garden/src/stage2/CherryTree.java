package stage2;

public class CherryTree extends stage2.GardenTree {

    private static final long serialVersionUID = 2765106927816125373L;

    public CherryTree() {
        super(stage2.GardenTree.Type.CHERRY, 0, false);
    }

    public CherryTree(int age, boolean isFruiting) {
        super(stage2.GardenTree.Type.CHERRY, age, isFruiting);
    }
}