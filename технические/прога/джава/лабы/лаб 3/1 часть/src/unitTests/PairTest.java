package unitTests;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;
import core.Pair;

public class PairTest {

    @Test
    public void testConstructorAndGetters() {
        Pair pair = new Pair(5, 10);
        assertEquals(5, pair.getFirst(), "Первое число должно быть 5");
        assertEquals(10, pair.getSecond(), "Второе число должно быть 10");
    }

    @Test
    public void testMultiplyPositive() {
        Pair pair = new Pair(3, 7);
        Pair result = pair.multiply(2);
        assertEquals(6, result.getFirst(), "Первое число должно быть 6 после умножения на 2");
        assertEquals(14, result.getSecond(), "Второе число должно быть 14 после умножения на 2");
    }


    @Test
    public void testMultiplyWithZero() {
        Pair pair = new Pair(3, 9);
        Pair result = pair.multiply(0);
        assertEquals(0, result.getFirst(), "Первое число должно быть 0 после умножения на 0");
        assertEquals(0, result.getSecond(), "Второе число должно быть 0 после умножения на 0");
    }

    @Test
    public void testMultiplyWithNegativeNumber() {
        Pair pair = new Pair(4, 6);
        Pair result = pair.multiply(-2);
        assertEquals(-8, result.getFirst(), "Первое число должно быть -8 после умножения на -2");
        assertEquals(-12, result.getSecond(), "Второе число должно быть -12 после умножения на -2");
    }

    @Test
    public void testMultiplyWithDifferentSignedNumber() {
        Pair pair = new Pair(4, -6);
        Pair result = pair.multiply(-3);
        assertEquals(-12, result.getFirst(), "Первое число должно быть -12 после умножения на -2");
        assertEquals(18, result.getSecond(), "Второе число должно быть 18 после умножения на -2");
    }

    @Test
    public void testAddPositive() {
        Pair pair1 = new Pair(4, 5);
        Pair pair2 = new Pair(1, 2);
        Pair result = pair1.add(pair2);
        assertEquals(5, result.getFirst(), "Первое число должно быть 5 после сложения");
        assertEquals(7, result.getSecond(), "Второе число должно быть 7 после сложения");
    }

    @Test
    public void testAddNegativeNumbers() {
        Pair pair1 = new Pair(-3, -5);
        Pair pair2 = new Pair(-2, -7);
        Pair result = pair1.add(pair2);
        assertEquals(-5, result.getFirst(), "Первое число должно быть -5 после сложения с отрицательными числами");
        assertEquals(-12, result.getSecond(), "Второе число должно быть -12 после сложения с отрицательными числами");
    }

    @Test
    public void testAddDifferentSignedNumbers() {
        Pair pair1 = new Pair(-3, -5);
        Pair pair2 = new Pair(-2, 7);
        Pair result = pair1.add(pair2);
        assertEquals(-5, result.getFirst(), "Первое число должно быть -5 после сложения с отрицательными числами");
        assertEquals(2, result.getSecond(), "Второе число должно быть 2 после сложения с отрицательными числами");
    }

    @Test
    public void testToStringPositive() {
        Pair pair = new Pair(8, 12);
        assertEquals("(8, 12)", pair.toString(), "Строковое представление пары должно быть (8, 12)");
    }
}
