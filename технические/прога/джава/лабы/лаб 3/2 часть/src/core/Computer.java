package core;

import java.util.Arrays;
import java.util.Iterator;

/**
 * The {@code java.Computer} class serves as a superclass representing a generic computer.
 * It implements the {@code Comparable} interface for comparing computers by brand and
 * the {@code Iterable} interface to allow iteration over its fields.
 * <p>
 * This class defines common properties shared among different types of computers, such as brand,
 * model, CPU, RAM, and storage.
 * </p>
 *
 * @author Matvey Kvetko
 * @version 1.0
 */
public class Computer implements Comparable<Computer>, Iterable<String> {
    protected String brand;   // The brand of the computer
    protected String model;   // The model of the computer
    protected String cpu;     // The CPU type of the computer
    protected int ram;        // The amount of RAM in GB
    protected int storage;    // The amount of storage in GB

    /**
     * Returns the brand of the computer.
     *
     * @return the brand as a {@code String}
     */
    public String getBrand() {
        return brand;
    }

    /**
     * Returns the model of the computer.
     *
     * @return the model as a {@code String}
     */
    public String getModel() {
        return model;
    }

    /**
     * Returns the CPU type of the computer.
     *
     * @return the CPU type as a {@code String}
     */
    public String getCpu() {
        return cpu;
    }

    /**
     * Returns the amount of RAM in the computer.
     *
     * @return the RAM amount in GB as an {@code int}
     */
    public int getRam() {
        return ram;
    }


    public int getStorage() {
        return storage;
    }


    /**
     * Constructs a new {@code java.Computer} with the specified parameters.
     *
     * @param brand   the brand of the computer
     * @param model   the model of the computer
     * @param cpu     the CPU type of the computer
     * @param ram     the amount of RAM in GB
     * @param storage the amount of storage in GB
     */
    public Computer(String brand, String model, String cpu, int ram, int storage) {
        this.brand = brand;
        this.model = model;
        this.cpu = cpu;
        this.ram = ram;
        this.storage = storage;
    }

    /**
     * Returns a string representation of the {@code java.Computer} object.
     * The string contains all the fields separated by semicolons.
     *
     * @return a string representation of the {@code java.Computer}
     */
    @Override
    public String toString() {
        return brand + ";" + model + ";" + cpu + ";" + ram + ";" + storage;
    }

    /**
     * Constructs a new {@code java.Computer} from a string representation.
     *
     * @param str the string containing the fields of the {@code java.Computer} separated by semicolons
     * @return a new {@code java.Computer} object
     */
    public static Computer fromString(String str) {
        String[] fields = str.split(";");
        return new Computer(fields[0], fields[1], fields[2], Integer.parseInt(fields[3]), Integer.parseInt(fields[4]));
    }

    /**
     * Compares this {@code java.Computer} to another by brand.
     *
     * @param o the {@code java.Computer} to compare to
     * @return a negative integer, zero, or a positive integer as this object's brand is less than, equal to, or greater than the specified object's brand
     */
    @Override
    public int compareTo(Computer o) {
        return this.brand.compareTo(o.brand);
    }

    /**
     * Returns an iterator over elements of type {@code String}.
     * The iterator allows iteration over the fields of the {@code java.Computer} object.
     *
     * @return an {@code Iterator<String>} over the fields of the {@code java.Computer}
     */
    @Override
    public Iterator<String> iterator() {
        return Arrays.asList(brand, model, cpu, String.valueOf(ram), String.valueOf(storage)).iterator();
    }
}
