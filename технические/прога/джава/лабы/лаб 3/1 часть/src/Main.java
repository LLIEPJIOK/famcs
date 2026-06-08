import java.util.Arrays;

import core.Pair;
import core.Money;

/**
 * Главный класс для демонстрации работы с классами Pair и Money.
 * В классе выполняются основные операции над объектами этих классов, такие как сложение, вычитание, умножение и сортировка.
 *
 * @author Лебедев Денис
 * @version 1.0
 */
public class Main {
    /**
     * Главный метод, с которого начинается выполнение программы.
     *
     * @param args аргументы командной строки (не используются в данной программе)
     */
    public static void main(String[] args) {
        System.out.println("------------Класс Pair------------");

        // Создание двух объектов Pair
        Pair pair1 = new Pair(10, 20);
        Pair pair2 = new Pair(5, 15);

        // Вывод созданных объектов
        System.out.println("Первая пара: " + pair1);
        System.out.println("Вторая пара: " + pair2);

        // Сложение двух объектов Pair
        Pair addedPair = pair1.add(pair2);
        System.out.println("\nСумма первой и второй пар: " + addedPair);

        // Умножение объекта Pair на число
        Pair multipliedPair = pair1.multiply(3);
        System.out.println("Умноженная первая пара на 3: " + multipliedPair);

        System.out.println("\n\n------------Класс Money------------");

        // Создание двух объектов Money
        Money money1 = new Money(100, 30);
        Money money2 = new Money(75, 30);

        // Выполнение операций над объектами Money
        Money sum = money1.add(money2);           // Сложение
        Money difference = money1.subtract(money2); // Вычитание
        Money product = money1.multiply(3);        // Умножение
        Money division = money1.divide(5);         // Деление

        // Вывод результатов операций
        System.out.println("money1: " + money1);
        System.out.println("money2: " + money2);
        System.out.println("\nСумма: " + sum);
        System.out.println("Разница: " + difference);
        System.out.println("Умножение первого объекта на 3: " + product);
        System.out.println("Деление первого объекта на 5: " + division);

        // Парсинг строки и создание объекта Money
        String moneyString = "123 руб. 45 коп.";
        Money parsedMoney = Money.fromString(moneyString);
        System.out.println("\nПарсинг строки: " + parsedMoney);

        // Итерация по объекту Money
        System.out.println("\nИтерирование по объекту money1:");
        for (Object value : money1) {
            System.out.println(value);
        }

        // Сравнение объектов Money
        System.out.println("\nСравнение объектов Money:");
        money1.setCompareIdx(0); // Сравнение по рублям
        System.out.println("money1 и money2 сравниваем по рублям через compareTo: " + money1.compareTo(money2));
        money1.setCompareIdx(1); // Сравнение по копейкам
        System.out.println("money1 и money2 сравниваем по копейкам через compare: " + money1.compare(money1, money2));

        // Создание массива объектов Money и сортировка
        Money[] monies = new Money[]{money1, money2, sum, difference, product, division, parsedMoney};
        for (Money money : monies) {
            money.setCompareIdx(1);
        }

        // Сортировка и вывод отсортированного массива
        System.out.println("\nОтсортированный по копейкам массив:");
        Arrays.sort(monies);
        for (Money money : monies) {
            System.out.println(money);
        }
    }
}
