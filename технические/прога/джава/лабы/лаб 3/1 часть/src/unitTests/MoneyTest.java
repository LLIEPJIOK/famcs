package unitTests;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;
import core.Money;

import java.util.NoSuchElementException;

public class MoneyTest {

    @Test
    public void testConstructorAndGetters() {
        Money money = new Money(10, 50);
        assertEquals(10, money.getFirst(), "Количество рублей должно быть 10");
        assertEquals(50, money.getSecond(), "Количество копеек должно быть 50");
        assertEquals(0, money.getIteratorIdx(), "Айди итератора должно равняться нулю");
        assertEquals(0, money.getCompareIdx(), "Айди сравнения должно равняться нулю");
    }

    @Test
    public void testConstructorNegativeRubles() {
        assertThrows(AssertionError.class, () -> new Money(-1, 50), "Конструктор должен выбрасывать исключение при отрицательных рублях");
    }

    @Test
    public void testConstructorNegativeKopecks() {
        assertThrows(AssertionError.class, () -> new Money(5, -10), "Конструктор должен выбрасывать исключение при отрицательных копейках");
    }

    @Test
    public void testConstructorManyKopecks() {
        assertThrows(AssertionError.class, () -> new Money(5, 111), "Конструктор должен выбрасывать исключение при отрицательных копейках");
    }

    @Test
    public void testAdd() {
        Money money1 = new Money(5, 75);
        Money money2 = new Money(3, 50);
        Money result = money1.add(money2);
        assertEquals(9, result.getFirst(), "Количество рублей должно быть 9");
        assertEquals(25, result.getSecond(), "Количество копеек должно быть 25");
    }

    @Test
    public void testMultiply() {
        Money money = new Money(2, 50);
        Money result = money.multiply(3);
        assertEquals(7, result.getFirst(), "Количество рублей должно быть 7");
        assertEquals(50, result.getSecond(), "Количество копеек должно быть 50");
    }

    @Test
    public void testMultiplyNull() {
        Money money = new Money(2, 50);
        Money result = money.multiply(0);
        assertEquals(0, result.getFirst(), "Количество рублей должно быть 7");
        assertEquals(0, result.getSecond(), "Количество копеек должно быть 50");
    }

    @Test
    public void testMultiplyNegativeNumber() {
        assertThrows(AssertionError.class, () -> {
            Money money = new Money(3, 25);
            money.multiply(-2);
        }, "Метод multiply должен выбрасывать исключение при отрицательном множителе");
    }

    @Test
    public void testSubtract() {
        Money money1 = new Money(10, 50);
        Money money2 = new Money(3, 75);
        Money result = money1.subtract(money2);
        assertEquals(6, result.getFirst(), "Количество рублей должно быть 6");
        assertEquals(75, result.getSecond(), "Количество копеек должно быть 75");
    }

    @Test
    public void testSubtractMuchMoney() {
        assertThrows(AssertionError.class, () -> {
            Money money1 = new Money(10, 50);
            Money money2 = new Money(10, 75);
            money1.subtract(money2);
        }, "Итоговое количество монет должно быть больше нуля");
    }

    @Test
    public void testDivide() {
        Money money = new Money(5, 50);
        Money result = money.divide(3);
        assertEquals(1, result.getFirst(), "Количество рублей должно быть 1");
        assertEquals(83, result.getSecond(), "Количество копеек должно быть 83");
    }

    @Test
    public void testDivideByZero() {
        assertThrows(AssertionError.class, () -> {
            Money money = new Money(5, 50);
            money.divide(0);
        }, "Метод divide должен выбрасывать исключение при делении на ноль");
    }

    @Test
    public void testDivideNegativeNumber() {
        assertThrows(AssertionError.class, () -> {
            Money money = new Money(5, 50);
            money.divide(-2);
        }, "Метод divide должен выбрасывать исключение при отрицательном делителе");
    }

    @Test
    public void testToString() {
        Money money = new Money(7, 99);
        assertEquals("7 руб. 99 коп.", money.toString(), "Строковое представление должно быть '7 руб. 99 коп.'");
    }

    @Test
    public void testFromString() {
        Money money = Money.fromString("8 руб. 15 коп.");
        assertEquals(8, money.getFirst(), "Количество рублей должно быть 8");
        assertEquals(15, money.getSecond(), "Количество копеек должно быть 15");
    }

    @Test
    public void testFromStringWithNotEnoughWords() {
        assertThrows(AssertionError.class, () -> Money.fromString("Invalid format"), "Метод fromString должен выбрасывать исключение при неправильном формате строки");
    }

    @Test
    public void testFromStringWithInvalidFormat() {
        assertThrows(AssertionError.class, () -> Money.fromString("Inva lid form at"), "Метод fromString должен выбрасывать исключение при неправильном формате строки");
    }

    @Test
    public void testFromStringInvalidNumbers() {
        assertThrows(IllegalArgumentException.class, () -> Money.fromString("Inv руб. for коп."), "Метод fromString должен выбрасывать исключение при неправильном формате строки");
    }

    @Test
    public void testIterator() {
        Money money = new Money(3, 25);
        int count = 0;
        for (Object value : money) {
            if (count == 0) {
                assertEquals(3, value, "Первый элемент итератора должен быть 3");
            } else if (count == 1) {
                assertEquals(25, value, "Второй элемент итератора должен быть 25");
            }
            count++;
        }
        assertEquals(2, count, "Итератор должен вернуть 2 элемента");
    }

    @Test
    public void testIteratorNoSuchElementException() {
        Money money = new Money(1, 1);
        assertTrue(money.hasNext(), "Должны быть ещё элементов");
        money.next();
        assertTrue(money.hasNext(), "Должны быть ещё элементов");
        money.next();
        assertFalse(money.hasNext(), "Не должно быть больше элементов");
        assertThrows(NoSuchElementException.class, money::next, "Метод next должен выбрасывать исключение при попытке доступа к следующему несуществующему элементу");
    }

    @Test
    public void testCompareTo() {
        Money money1 = new Money(5, 50);
        Money money2 = new Money(3, 25);
        Money money3 = new Money(5, 50);
        money1.setCompareIdx(0);  // Сравнение по рублям
        assertTrue(money1.compareTo(money2) > 0, "5 рублей должно быть больше чем 3 рубля");
        money1.setCompareIdx(1);  // Сравнение по копейкам
        assertTrue(money1.compareTo(money2) > 0, "50 копеек должно быть больше чем 25 копеек");
        money1.setCompareIdx(0);  // Сравнение по рублям
        assertEquals(0, money1.compareTo(money3), "Два одинаковых объекта Money должны быть равны");
    }

    @Test
    public void testCompareToInvalidIndex() {
        Money money = new Money(1, 1);
        money.setCompareIdx(2);  // Некорректный индекс
        assertThrows(NoSuchElementException.class, () -> money.compareTo(new Money(1, 1)), "Метод compareTo должен выбрасывать исключение при некорректном значении compareIdx");
    }

    @Test
    public void testComparator() {
        Money money1 = new Money(5, 50);
        Money money2 = new Money(6, 25);
        Money money3 = new Money(5, 50);
        assertTrue(money1.compare(money1, money2) < 0, "5 руб. 50 коп. должно быть меньше 6 руб. 25 коп., сравнивая по рублям");
        assertEquals(0, money1.compare(money1, money3), "5 руб. 50 коп. должно быть равно 5 руб. 50 коп., сравнивая по рублям");

        money1.setCompareIdx(1);
        assertTrue(money1.compare(money1, money2) > 0, "5 руб. 50 коп. должно быть больше 6 руб. 25 коп., сравнивая по копейкам");
        assertEquals(0, money1.compare(money1, money3), "5 руб. 50 коп. должно быть равно 5 руб. 50 коп., сравнивая по копейкам");
    }
}
