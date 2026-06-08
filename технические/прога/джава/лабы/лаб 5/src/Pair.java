import java.util.Iterator;

public class Pair {
    private int first;
    private int second;

    public Pair(int first, int second) {
        this.first = first;
        this.second = second;
    }

    public int getFirst() {
        return first;
    }

    public int getSecond() {
        return second;
    }

    public Pair multiply(int number) {
        return new Pair(first * number, second * number);
    }

    public Pair add(Pair other) {
        return new Pair(first + other.first, second + other.second);
    }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}
