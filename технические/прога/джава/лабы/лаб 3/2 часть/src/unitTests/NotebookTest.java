package unitTests;

import core.Notebook;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class NotebookTest {
    @Test
    void testConstructor() {
        Notebook notebook = new Notebook("Lenovo", "ThinkPad", "Intel i5", 8, 256, 1.5);
        assertEquals("Lenovo", notebook.getBrand());
        assertEquals("ThinkPad", notebook.getModel());
        assertEquals("Intel i5", notebook.getCpu());
        assertEquals(8, notebook.getRam());
        assertEquals(256, notebook.getStorage());
        assertEquals(1.5, notebook.getWeight());
    }

    @Test
    void testToString() {
        Notebook notebook = new Notebook("Lenovo", "ThinkPad", "Intel i5", 8, 256, 1.5);
        String expected = "Lenovo;ThinkPad;Intel i5;8;256;1.5";
        assertEquals(expected, notebook.toString());
    }

    @Test
    void testFromString() {
        String data = "Dell;XPS;Intel i7;16;512;1.3";
        Notebook notebook = Notebook.fromString(data);
        assertEquals("Dell", notebook.getBrand());
        assertEquals("XPS", notebook.getModel());
        assertEquals("Intel i7", notebook.getCpu());
        assertEquals(16, notebook.getRam());
        assertEquals(512, notebook.getStorage());
        assertEquals(1.3, notebook.getWeight());
    }

    @Test
    void testInvalidFromString() {
        assertThrows(ArrayIndexOutOfBoundsException.class, () -> {
            Notebook.fromString("Invalid;Data");
        });
    }

    @Test
    void testInvalidWeightInFromString() {
        assertThrows(NumberFormatException.class, () -> {
            Notebook.fromString("HP;Pavilion;AMD Ryzen 5;8;256;invalidWeight");
        });
    }
}
