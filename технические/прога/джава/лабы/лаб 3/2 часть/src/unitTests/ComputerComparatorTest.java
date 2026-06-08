package unitTests;

import core.Computer;
import core.ComputerComparator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ComputerComparatorTest {

    private Computer computer1;
    private Computer computer2;

    @BeforeEach
    void setUp() {
        computer1 = new Computer("Apple", "MacBook Pro", "M1", 16, 512);
        computer2 = new Computer("Dell", "XPS", "Intel i7", 16, 1024);
    }

    @Test
    void testCompareByBrand() {
        ComputerComparator comparator = new ComputerComparator("brand");
        assertTrue(comparator.compare(computer1, computer2) < 0); // Apple < Dell
    }

    @Test
    void testCompareByModel() {
        ComputerComparator comparator = new ComputerComparator("model");
        assertTrue(comparator.compare(computer1, computer2) < 0); // MacBook Pro < XPS
    }

    @Test
    void testCompareByCpu() {
        ComputerComparator comparator = new ComputerComparator("cpu");
        assertTrue(comparator.compare(computer1, computer2) > 0); // M1 > Intel i7
    }

    @Test
    void testCompareByRam() {
        ComputerComparator comparator = new ComputerComparator("ram");
        assertEquals(0, comparator.compare(computer1, computer2)); // Both have 16GB RAM
    }

    @Test
    void testCompareByStorage() {
        ComputerComparator comparator = new ComputerComparator("storage");
        assertTrue(comparator.compare(computer1, computer2) < 0); // 512GB < 1024GB
    }

    @Test
    void testInvalidField() {
        ComputerComparator comparator = new ComputerComparator("invalidField");
        assertThrows(IllegalArgumentException.class, () -> {
            comparator.compare(computer1, computer2);
        });
    }
}
