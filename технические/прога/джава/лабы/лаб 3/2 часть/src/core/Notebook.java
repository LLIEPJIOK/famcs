package core;

/**
 * The {@code java.Notebook} class represents a notebook (laptop) computer and extends the {@code java.Computer} class.
 * It introduces a unique property, {@code weight}, to describe the weight of the notebook.
 * <p>
 * This class inherits common properties from the {@code java.Computer} class and adds functionality specific to notebooks.
 * </p>
 *
 * @version 1.0
 */
public class Notebook extends Computer {
    private double weight;   // The weight of the notebook in kilograms

    /**
     * Returns the weight of the notebook.
     *
     * @return the weight in kilograms as a {@code double}
     */
    public double getWeight() {
        return weight;
    }


    /**
     * Constructs a new {@code java.Notebook} with the specified parameters.
     *
     * @param brand   the brand of the notebook
     * @param model   the model of the notebook
     * @param cpu     the CPU type of the notebook
     * @param ram     the amount of RAM in GB
     * @param storage the amount of storage in GB
     * @param weight  the weight of the notebook in kilograms
     */
    public Notebook(String brand, String model, String cpu, int ram, int storage, double weight) {
        super(brand, model, cpu, ram, storage);
        this.weight = weight;
    }

    /**
     * Returns a string representation of the {@code java.Notebook} object.
     * The string includes all inherited fields plus the weight, separated by semicolons.
     *
     * @return a string representation of the {@code java.Notebook}
     */
    @Override
    public String toString() {
        return super.toString() + ";" + weight;
    }

    /**
     * Constructs a new {@code java.Notebook} from a string representation.
     *
     * @param str the string containing the fields of the {@code java.Notebook} separated by semicolons
     * @return a new {@code java.Notebook} object
     */
    public static Notebook fromString(String str) {
        String[] fields = str.split(";");
        return new Notebook(fields[0], fields[1], fields[2], Integer.parseInt(fields[3]), Integer.parseInt(fields[4]), Double.parseDouble(fields[5]));
    }
}