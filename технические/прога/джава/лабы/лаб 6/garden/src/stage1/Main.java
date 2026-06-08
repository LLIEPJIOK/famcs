package stage1;

import java.io.File;

public class Main {
    public static GardenTree[] createGarden() {
        GardenTree[] garden = new GardenTree[5];
        garden[0] = new AppleTree(5, true);
        garden[1] = new CherryTree();
        garden[2] = new PearTree(4, false);
        garden[3] = new PlumTree(10, true);
        garden[4] = new RowanTree(12, false);
        return garden;
    }

    public static void main(String[] args) {
        try {
            Connector con = new Connector(new File("garden.dat"));
            con.write(createGarden());
            GardenTree[] garden = con.read();
            System.out.println("The garden: ");
            for (GardenTree n : garden) {
                System.out.println(n);
            }
            System.out.println();
            for (GardenTree n : garden) {
                n.transplant();
            }
        } catch (Exception e) {
            System.err.println(e);
        }
    }
}