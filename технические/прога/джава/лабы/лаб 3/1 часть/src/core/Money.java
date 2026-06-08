package core;

import java.util.Comparator;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * Класс Money представляет собой пару значений "рубли-копейки" и предоставляет
 * методы для выполнения различных операций с деньгами, таких как сложение, вычитание, умножение и деление.
 * Также реализованы интерфейсы для итерации и сравнения объектов Money.
 *
 * @author Лебедев Денис
 * @version 1.0
 */
public class Money extends Pair implements Iterator<Object>, Iterable<Object>, Comparable<Money>, Comparator<Money> {
    /**
     * Индекс для итерации по значениям рубли-копейки.
     */
    private int iteratorIdx;

    /**
     * Индекс для сравнения объектов Money.
     */
    private int compareIdx;

    /**
     * Конструктор для создания объекта Money с заданными рублями и копейками.
     *
     * @param rubles  количество рублей, должно быть неотрицательным
     * @param kopecks количество копеек, должно быть неотрицательным
     * @throws IllegalArgumentException если рубли или копейки отрицательны
     */
    public Money(int rubles, int kopecks) {
        super(rubles, kopecks);
        assert rubles >= 0 && kopecks >= 0 && kopecks < 100;
        iteratorIdx = 0;
        compareIdx = 0;
    }

    /**
     * Возвращает текущий индекс итератора.
     *
     * @return индекс итератора
     */
    public int getIteratorIdx() {
        return iteratorIdx;
    }

    /**
     * Возвращает текущий индекс сравнения.
     *
     * @return индекс сравнения
     */
    public int getCompareIdx() {
        return compareIdx;
    }

    /**
     * Устанавливает индекс сравнения для метода compareTo.
     *
     * @param compareIdx новый индекс сравнения
     */
    public void setCompareIdx(int compareIdx) {
        this.compareIdx = compareIdx;
    }

    /**
     * Складывает текущее значение Money с другим объектом Pair, возвращая результат.
     *
     * @param other объект Pair, который нужно добавить к текущему Money
     * @return новый объект Money с результатом сложения
     */
    @Override
    public Money add(Pair other) {
        int newRubles = this.getFirst() + other.getFirst();
        int newKopecks = this.getSecond() + other.getSecond();
        newRubles += newKopecks / 100;
        newKopecks %= 100;
        return new Money(newRubles, newKopecks);
    }

    /**
     * Умножает текущее значение Money на заданное число.
     *
     * @param number множитель, должен быть неотрицательным
     * @return новый объект Money с результатом умножения
     * @throws IllegalArgumentException если множитель отрицательный
     */
    @Override
    public Money multiply(int number) {
        assert number >= 0;
        int newRubles = getFirst() * number;
        int newKopecks = getSecond() * number;
        newRubles += newKopecks / 100;
        newKopecks %= 100;
        return new Money(newRubles, newKopecks);
    }

    /**
     * Вычитает другое значение Money из текущего.
     *
     * @param other объект Money для вычитания
     * @return новый объект Money с результатом вычитания
     * @throws IllegalArgumentException если результат отрицательный
     */
    public Money subtract(Money other) {
        int newRubles = getFirst() - other.getFirst();
        int newKopecks = getSecond() - other.getSecond();
        if (newKopecks < 0) {
            newRubles--;
            newKopecks += 100;
        }
        assert newRubles >= 0;
        return new Money(newRubles, newKopecks);
    }

    /**
     * Делит текущее значение Money на заданный делитель.
     *
     * @param divisor делитель, должен быть больше нуля
     * @return новый объект Money с результатом деления
     * @throws IllegalArgumentException если делитель меньше или равен нулю
     */
    public Money divide(int divisor) {
        assert divisor > 0;
        int totalKopecks = getFirst() * 100 + getSecond();
        int resultKopecks = totalKopecks / divisor;
        int resultRubles = resultKopecks / 100;
        resultKopecks %= 100;
        return new Money(resultRubles, resultKopecks);
    }

    /**
     * Возвращает строковое представление объекта Money в формате "руб. коп.".
     *
     * @return строковое представление текущего Money
     */
    @Override
    public String toString() {
        return getFirst() + " руб. " + getSecond() + " коп.";
    }

    /**
     * Создает объект Money из строкового представления.
     *
     * @param moneyString строковое представление денег в формате "руб. коп."
     * @return новый объект Money
     * @throws IllegalArgumentException если строка не соответствует ожидаемому формату
     */
    public static Money fromString(String moneyString) {
        String[] parts = moneyString.split(" ");
        assert parts.length == 4 && parts[1].equals("руб.") && parts[3].equals("коп.");
        int rubles = Integer.parseInt(parts[0]);
        int kopecks = Integer.parseInt(parts[2]);
        return new Money(rubles, kopecks);
    }

    /**
     * Возвращает итератор для объекта Money.
     *
     * @return итератор для текущего Money
     */
    @Override
    public Iterator<Object> iterator() {
        resetIterator();
        return this;
    }

    /**
     * Сбрасывает индекс итератора в начальное состояние.
     */
    private void resetIterator() {
        iteratorIdx = 0;
    }

    /**
     * Проверяет, есть ли следующий элемент для итерации.
     *
     * @return true, если следующий элемент существует; false в противном случае
     */
    @Override
    public boolean hasNext() {
        return iteratorIdx < 2;
    }

    /**
     * Возвращает следующий элемент итерации: рубли или копейки.
     *
     * @return следующий элемент итерации
     * @throws NoSuchElementException если больше нет элементов для итерации
     */
    @Override
    public Object next() {
        switch (iteratorIdx++) {
            case 0:
                return getFirst();
            case 1:
                return getSecond();
            default:
                throw new NoSuchElementException();
        }
    }

    /**
     * Сравнивает текущий объект Money с другим объектом Money в зависимости от compareIdx.
     *
     * @param other объект Money для сравнения
     * @return отрицательное число, ноль или положительное число в зависимости от сравнения
     * @throws NoSuchElementException если compareIdx имеет некорректное значение
     */
    @Override
    public int compareTo(Money other) {
        switch (compareIdx) {
            case 0:
                return Integer.compare(getFirst(), other.getFirst());
            case 1:
                return Integer.compare(getSecond(), other.getSecond());
            default:
                throw new NoSuchElementException();
        }
    }

    /**
     * Сравнивает два объекта Money.
     *
     * @param l первый объект Money для сравнения
     * @param r второй объект Money для сравнения
     * @return результат сравнения двух объектов Money
     */
    @Override
    public int compare(Money l, Money r) {
        return l.compareTo(r);
    }
}
