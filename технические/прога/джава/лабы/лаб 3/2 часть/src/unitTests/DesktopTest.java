package unitTests;

import core.Desktop;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DesktopTest {

    @Test
    void testConstructor() {
        Desktop desktop = new Desktop("Dell", "XPS", "Intel i7", 16, 512, "Tower");
        assertEquals("Dell", desktop.getBrand());
        assertEquals("XPS", desktop.getModel());
        assertEquals("Intel i7", desktop.getCpu());
        assertEquals(16, desktop.getRam());
        assertEquals(512, desktop.getStorage());
        assertEquals("Tower", desktop.getFormFactor());
    }

    @Test
    void testToString() {
        Desktop desktop = new Desktop("Dell", "XPS", "Intel i7", 16, 512, "Tower");
        String expected = "Dell;XPS;Intel i7;16;512;Tower";
        assertEquals(expected, desktop.toString());
    }

    @Test
    void testFromString() {
        String data = "Apple;Mac Pro;M1;32;1024;Mini";
        Desktop desktop = Desktop.fromString(data);
        assertEquals("Apple", desktop.getBrand());
        assertEquals("Mac Pro", desktop.getModel());
        assertEquals("M1", desktop.getCpu());
        assertEquals(32, desktop.getRam());
        assertEquals(1024, desktop.getStorage());
        assertEquals("Mini", desktop.toString().split(";")[5]);
    }

    @Test
    void testInheritance() {
        Desktop desktop = new Desktop("HP", "Pavilion", "AMD Ryzen 5", 16, 512, "Tower");
        assertEquals("HP", desktop.getBrand());
        assertEquals("Pavilion", desktop.getModel());
        assertEquals("AMD Ryzen 5", desktop.getCpu());
        assertEquals(16, desktop.getRam());
        assertEquals(512, desktop.getStorage());
    }

    @Test
    void testInvalidFromString() {
        assertThrows(ArrayIndexOutOfBoundsException.class, () -> {
            Desktop.fromString("Invalid;Data");
        });
    }
}
