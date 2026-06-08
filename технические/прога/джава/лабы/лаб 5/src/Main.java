import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        System.out.println("------------Класс Pair------------");
        Pair pair1 = new Pair(10, 20);
        Pair pair2 = new Pair(5, 15);

        System.out.println("Первая пара: " + pair1);
        System.out.println("Вторая пара: " + pair2);

        Pair addedPair = pair1.add(pair2);
        System.out.println("\nСумма первой и второй пар: " + addedPair);

        Pair multipliedPair = pair1.multiply(3);
        System.out.println("Умноженная первая пара на 3: " + multipliedPair);

        System.out.println("\n\n------------Класс Money------------");
        Money money1 = new Money(100, 30);
        Money money2 = new Money(75, 30);

        Money sum = money1.add(money2);
        Money difference = money1.subtract(money2);
        Money product = money1.multiply(3);
        Money division = money1.divide(5);

        System.out.println("money1: " + money1);
        System.out.println("money2: " + money2);
        System.out.println("\nСумма: " + sum);
        System.out.println("Разница: " + difference);
        System.out.println("Умножение первого объекта на 3: " + product);
        System.out.println("Деление первого объекта на 5: " + division);

        String moneyString = "123 руб. 45 коп.";
        Money parsedMoney = Money.fromString(moneyString);
        System.out.println("\nПарсинг строки: " + parsedMoney);

        System.out.println("\nИтерирование по объекту money1:");
        for (Object value : money1) {
            System.out.println(value);
        }

        System.out.println("\nСравнение объектов Money:");
        money1.setCompareIdx(0);
        System.out.println("money1 и money2 сравниваем по рублям через compareTo: " + money1.compareTo(money2));
        money1.setCompareIdx(1);
        System.out.println("money1 и money2 сравниваем по копейкам через compare: " + money1.compare(money1, money2));

        Money[] monies = new Money[]{money1, money2, sum, difference, product, division, parsedMoney};
        for (Money money : monies) {
            money.setCompareIdx(1);
        }

        System.out.println("\nОтсортированный по копейкам массив:");
        Arrays.sort(monies);
        for (Money money : monies) {
            System.out.println(money);
        }
    }
}
