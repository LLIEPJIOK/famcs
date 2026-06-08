package stage2;

import java.util.*;
import java.io.*;

public class Main {
    public static GardenTree[] createGarden() {
        GardenTree[] garden = new GardenTree[5];
        garden[0] = new stage2.AppleTree(5, true);
        garden[1] = new CherryTree();
        garden[2] = new PearTree(4, false);
        garden[3] = new PlumTree(10, true);
        garden[4] = new RowanTree(12, false);
        return garden;
    }

    static Locale createLocale(String[] args) {
        if (args.length == 2) {
            return new Locale(args[0], args[1]);
        }
        if (args.length == 4) {
            return new Locale(args[2], args[3]);
        }
        return null;
    }

    static void setupConsole(String[] args) {
        if (args.length >= 2) {
            if (args[0].equals("-encoding")) {
                try {
                    System.setOut(new PrintStream(System.out, true, args[1]));
                } catch (UnsupportedEncodingException ex) {
                    System.err.println("Unsupported encoding: " + args[1]);
                    System.exit(1);
                }
            }
        }
    }

    public static void main(String[] args) {

        try {
            setupConsole(args);
            Locale loc = createLocale(args);
            if (loc == null) {
                System.err.println("Invalid argument(s)\n"
                        + "Syntax: [-encoding ENCODING_ID] language country\n"
                        + "Example: -encoding Cp855 be BY");
                System.exit(1);
            }
            AppLocale.set(loc);
            Connector con = new Connector(new File("garden.dat"));
            con.write(createGarden());
            GardenTree[] garden = con.read();
            System.out.println(AppLocale.getString(AppLocale.theGarden) + ":");
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