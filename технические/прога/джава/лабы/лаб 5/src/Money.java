import java.util.Comparator;
import java.util.Iterator;
import java.util.NoSuchElementException;

public class Money extends Pair implements Iterator<Object>, Iterable<Object>, Comparable<Money>, Comparator<Money> {
    private int iteratorIdx;

    private int compareIdx;

    public Money(int rubles, int kopecks) {
        super(rubles, kopecks);
        assert rubles >= 0 && kopecks >= 0;
        iteratorIdx = 0;
        compareIdx = 0;
    }

    public int getIteratorIdx() {
        return iteratorIdx;
    }

    public int getCompareIdx(){
        return compareIdx;
    }

    public void setCompareIdx(int compareIdx){
        this.compareIdx = compareIdx;
    }

    @Override
    public Money add(Pair other) {
        int newRubles = this.getFirst() + other.getFirst();
        int newKopecks = this.getSecond() + other.getSecond();
        newRubles += newKopecks / 100;
        newKopecks %= 100;
        return new Money(newRubles, newKopecks);
    }

    @Override
    public Money multiply(int number) {
        assert number >= 0;
        int newRubles = getFirst() * number;
        int newKopecks = getSecond() * number;
        newRubles += newKopecks / 100;
        newKopecks %= 100;
        return new Money(newRubles, newKopecks);
    }

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

    public Money divide(int divisor) {
        assert divisor > 0;
        int totalKopecks = getFirst() * 100 + getSecond();
        int resultKopecks = totalKopecks / divisor;
        int resultRubles = resultKopecks / 100;
        resultKopecks %= 100;
        return new Money(resultRubles, resultKopecks);
    }

    @Override
    public String toString() {
        return getFirst() + " руб. " + getSecond() + " коп.";
    }


    public static Money fromString(String moneyString) {
        String[] parts = moneyString.split(" ");
        assert parts.length == 4 && parts[1].equals("руб.") && parts[3].equals("коп.");
        int rubles = Integer.parseInt(parts[0]);
        int kopecks = Integer.parseInt(parts[2]);
        return new Money(rubles, kopecks);
    }

    @Override
    public Iterator<Object> iterator() {
        resetIterator();
        return this;
    }

    private void resetIterator() {
        iteratorIdx = 0;
    }

    @Override
    public boolean hasNext() {
        return iteratorIdx < 2;
    }

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

    @Override
    public int compareTo(Money other) {
        switch (compareIdx)
        {
            case 0:
                return Integer.compare(getFirst(), other.getFirst());
            case 1:
                return Integer.compare(getSecond(), other.getSecond());
            default:
                throw new NoSuchElementException();
        }
    }

    @Override
    public int compare(Money l, Money r) {
        return l.compareTo(r);
    }
}
