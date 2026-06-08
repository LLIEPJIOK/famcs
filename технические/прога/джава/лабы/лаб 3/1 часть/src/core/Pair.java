package core;

/**
 * Класс Pair представляет пару целых чисел и предоставляет методы для выполнения
 * базовых математических операций над этими числами.
 *
 * @author Лебедев Денис
 * @version 1.0
 */
public class Pair {
    /**
     * Первое целое число в паре.
     */
    private int first;

    /**
     * Второе целое число в паре.
     */
    private int second;

    /**
     * Конструктор для создания пары с заданными значениями.
     *
     * @param first  первое целое число в паре
     * @param second второе целое число в паре
     */
    public Pair(int first, int second) {
        this.first = first;
        this.second = second;
    }

    /**
     * Возвращает первое целое число в паре.
     *
     * @return значение первого числа в паре
     */
    public int getFirst() {
        return first;
    }

    /**
     * Возвращает второе целое число в паре.
     *
     * @return значение второго числа в паре
     */
    public int getSecond() {
        return second;
    }

    /**
     * Умножает оба числа в паре на заданное число и возвращает новый объект Pair с результатом.
     *
     * @param number число, на которое нужно умножить оба значения в паре
     * @return новый объект Pair, содержащий результаты умножения
     */
    public Pair multiply(int number) {
        return new Pair(first * number, second * number);
    }

    /**
     * Складывает значения этой пары с другой парой и возвращает новый объект Pair с результатом.
     *
     * @param other другая пара для сложения
     * @return новый объект Pair, содержащий результаты сложения
     */
    public Pair add(Pair other) {
        return new Pair(first + other.first, second + other.second);
    }

    /**
     * Возвращает строковое представление пары в формате "(first, second)".
     *
     * @return строковое представление текущей пары
     */
    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}
