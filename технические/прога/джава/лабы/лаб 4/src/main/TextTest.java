package main;

import java.util.ArrayList;
import java.util.List;

public class TextTest {
    public static void main(String[] args) {
        Text text = new Text("Это первое предложение.");
        System.out.println("Проверка конструктора:\n" + text + "\n");

        text.addSentence("Это третье предложение.");
        text.addSentence("Это 4 предложение.");
        System.out.println("Проверка добавления:\n" + text + "\n");

        text.removeSentence(2);
        System.out.println("Проверка удаления:\n" + text + "\n");

        text.insertSentence(1, "Это второе предложение.");
        System.out.println("Проверка вставки:\n" + text + "\n");

        System.out.println("Количество букв: " + text.getLetterCount());
        System.out.println("Количество слов: " + text.getWordCount());
        System.out.println("Количество предложений: " + text.getSentenceCount());

        List<String> l = new ArrayList<>();
        l.add("Это первое предложение.");
        l.add("Это второе предложение.");
        l.add("Это третье предложение.");

        Text anotherText = new Text(l);
        System.out.println("\nПроверка конструктора со списком:\n" + text + "\n");

        System.out.println("Проверка сравнения:");
        if (text.isEqual(anotherText)) {
            System.out.println("Тексты идентичны.");
        } else {
            System.out.println("Тексты различны.");
        }
    }
}
