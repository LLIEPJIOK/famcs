package core;


/**
 * The {@code java.Desktop} class represents a desktop computer and extends the {@code java.Computer} class.
 * It introduces a unique property, {@code formFactor}, to describe the type of the desktop's case.
 * <p>
 * This class inherits common properties from the {@code java.Computer} class and adds functionality specific to desktops.
 * </p>
 *
 * @version 1.0
 */
public class Desktop extends Computer {
    private String formFactor;   // The form factor of the desktop (e.g., Tower, Mini)

    /**
     * Returns the form factor of the desktop.
     *
     * @return the form factor as a {@code String}
     */
    public String getFormFactor() {
        return formFactor;
    }


    /**
     * Constructs a new {@code java.Desktop} with the specified parameters.
     *
     * @param brand      the brand of the desktop
     * @param model      the model of the desktop
     * @param cpu        the CPU type of the desktop
     * @param ram        the amount of RAM in GB
     * @param storage    the amount of storage in GB
     * @param formFactor the form factor of the desktop
     */
    public Desktop(String brand, String model, String cpu, int ram, int storage, String formFactor) {
        super(brand, model, cpu, ram, storage);
        this.formFactor = formFactor;
    }

    /**
     * Returns a string representation of the {@code java.Desktop} object.
     * The string includes all inherited fields plus the form factor, separated by semicolons.
     *
     * @return a string representation of the {@code java.Desktop}
     */
    @Override
    public String toString() {
        return super.toString() + ";" + formFactor;
    }

    /**
     * Constructs a new {@code java.Desktop} from a string representation.
     *
     * @param str the string containing the fields of the {@code java.Desktop} separated by semicolons
     * @return a new {@code java.Desktop} object
     */
    public static Desktop fromString(String str) {
        String[] fields = str.split(";");
        return new Desktop(fields[0], fields[1], fields[2], Integer.parseInt(fields[3]), Integer.parseInt(fields[4]), fields[5]);
    }
}
