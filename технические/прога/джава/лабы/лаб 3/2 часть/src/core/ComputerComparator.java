package core;


import java.util.Comparator;

/**
 * The {@code java.ComputerComparator} class implements the {@code Comparator<java.Computer>} interface
 * and allows for comparing {@code java.Computer} objects based on a specified field.
 * <p>
 * This class supports comparisons by brand, model, CPU, RAM, and storage.
 * </p>
 *
 * @version 1.0
 */
public class ComputerComparator implements Comparator<Computer> {
    private String field;   // The field by which to compare the java.Computer objects

    /**
     * Constructs a new {@code java.ComputerComparator} with the specified field.
     *
     * @param field the field by which to compare the {@code java.Computer} objects
     */
    public ComputerComparator(String field) {
        this.field = field;
    }

    /**
     * Compares two {@code java.Computer} objects based on the specified field.
     *
     * @param o1 the first {@code java.Computer} to compare
     * @param o2 the second {@code java.Computer} to compare
     * @return a negative integer, zero, or a positive integer as the first object is less than, equal to, or greater than the second
     * @throws IllegalArgumentException if the specified field is invalid
     */
    @Override
    public int compare(Computer o1, Computer o2) {
        switch (field) {
            case "brand":
                return o1.brand.compareTo(o2.brand);
            case "model":
                return o1.model.compareTo(o2.model);
            case "cpu":
                return o1.cpu.compareTo(o2.cpu);
            case "ram":
                return Integer.compare(o1.ram, o2.ram);
            case "storage":
                return Integer.compare(o1.storage, o2.storage);
            default:
                throw new IllegalArgumentException("Invalid field: " + field);
        }
    }
}