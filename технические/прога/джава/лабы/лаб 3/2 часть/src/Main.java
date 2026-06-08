import core.Computer;
import core.ComputerComparator;
import core.Desktop;
import core.Notebook;

import java.util.*;

/**
 * The {@code java.Main} class demonstrates the functionality of the {@code java.Computer}, {@code java.Desktop},
 * {@code java.Notebook}, and {@code java.ComputerComparator} classes.
 * <p>
 * This class creates a list of {@code java.Computer} objects, including desktops and notebooks, and
 * demonstrates sorting them by different fields.
 * </p>
 *
 * @version 1.0
 */
public class Main {

    /**
     * The main method is the entry point of the application.
     * It creates a list of {@code java.Computer} objects and demonstrates sorting them.
     *
     * @param args command-line arguments (not used)
     */
    public static void main(String[] args) {
        List<Computer> computers = new ArrayList<>();
        computers.add(new Desktop("Dell", "Optiplex", "Intel i7", 16, 512, "Tower"));
        computers.add(new Notebook("HP", "Envy", "AMD Ryzen 5", 8, 256, 1.5));
        computers.add(new Desktop("Lenovo", "ThinkCentre", "Intel i5", 8, 256, "Mini"));
        computers.add(new Notebook("Apple", "MacBook Air", "Apple M1", 16, 512, 1.2));

        // Display the list before sorting
        System.out.println("Before Sorting:");
        for (Computer computer : computers) {
            System.out.println(computer);
        }

        // Sort by brand
        computers.sort(new ComputerComparator("brand"));

        // Display the list after sorting by brand
        System.out.println("\nAfter Sorting by brand:");
        for (Computer computer : computers) {
            System.out.println(computer);
        }

        // Sort by RAM
        computers.sort(new ComputerComparator("ram"));

        // Display the list after sorting by RAM
        System.out.println("\nAfter Sorting by RAM:");
        for (Computer computer : computers) {
            System.out.println(computer);
        }
    }
}
