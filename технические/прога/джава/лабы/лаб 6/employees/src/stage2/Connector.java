package stage2;

import java.io.*;

public class Connector {

    private final File file;

    public File getFile() {
        return file;
    }

    public Connector(String filename) {
        this.file = new File(filename);
    }

    public Connector(File file) {
        this.file = file;
    }

    public void write(Employee[] employees) throws IOException {
        FileOutputStream fos = new FileOutputStream(file);
        try (ObjectOutputStream oos = new ObjectOutputStream(fos)) {
            oos.writeInt(employees.length);
            for (Employee employee : employees) {
                oos.writeObject(employee);
            }
            oos.flush();
        }
    }

    public Employee[] read() throws IOException, ClassNotFoundException {
        FileInputStream fis = new FileInputStream(file);
        try (ObjectInputStream oin = new ObjectInputStream(fis)) {
            int length = oin.readInt();
            Employee[] result = new Employee[length];
            for (int i = 0; i < length; i++) {
                result[i] = (Employee) oin.readObject();
            }
            return result;
        }
    }
}