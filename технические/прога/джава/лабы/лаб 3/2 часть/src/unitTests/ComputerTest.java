package unitTests;

import core.Computer;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Iterator;

public class ComputerTest {

    @Test
    void testConstructor() {
        Computer computer = new Computer("Dell", "XPS", "Intel i7", 16, 512);
        assertEquals("Dell", computer.getBrand());
        assertEquals("XPS", computer.getModel());
        assertEquals("Intel i7", computer.getCpu());
        assertEquals(16, computer.getRam());
        assertEquals(512, computer.getStorage());

    }

    @Test
    void testToString() {
        Computer computer = new Computer("Dell", "XPS", "Intel i7", 16, 512);
        String expected = "Dell;XPS;Intel i7;16;512";
        assertEquals(expected, computer.toString());
    }

    @Test
    void testFromString() {
        String data = "Apple;MacBook;M1;8;256";
        Computer computer = Computer.fromString(data);
        assertEquals("Apple", computer.getBrand());
        assertEquals("MacBook", computer.getModel());
        assertEquals("M1", computer.getCpu());
        assertEquals(8, computer.getRam());
        assertEquals(256, computer.getStorage());
    }

    @Test
    void testCompareTo() {
        Computer computer1 = new Computer("Apple", "MacBook", "M1", 8, 256);
        Computer computer2 = new Computer("Dell", "XPS", "Intel i7", 16, 512);
        Computer computer3 = new Computer("Apple", "MacBook", "M1", 8, 256);

        assertTrue(computer1.compareTo(computer2) < 0);
        assertTrue(computer2.compareTo(computer1) > 0);
        assertEquals(0, computer1.compareTo(computer3));
    }

    @Test
    void testIterator() {
        Computer computer = new Computer("Apple", "MacBook", "M1", 8, 256);
        Iterator<String> iterator = computer.iterator();

        assertTrue(iterator.hasNext());
        assertEquals("Apple", iterator.next());

        assertTrue(iterator.hasNext());
        assertEquals("MacBook", iterator.next());

        assertTrue(iterator.hasNext());
        assertEquals("M1", iterator.next());

        assertTrue(iterator.hasNext());
        assertEquals("8", iterator.next());

        assertTrue(iterator.hasNext());
        assertEquals("256", iterator.next());

        assertFalse(iterator.hasNext());
    }

    @Test
    void testInvalidFromString() {
        assertThrows(ArrayIndexOutOfBoundsException.class, () -> {
            Computer.fromString("Invalid;Data");
        });
    }
}
