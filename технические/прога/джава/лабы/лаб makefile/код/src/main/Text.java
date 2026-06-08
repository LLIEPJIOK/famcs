package main;

import java.util.ArrayList;
import java.util.List;

public class Text {
    private final List<String> sentences;

    public Text() {
        this.sentences = new ArrayList<>();
    }

    public Text(List<String> sentences) {
        assert sentences != null : "List of sentences cannot be null";
        this.sentences = new ArrayList<>(sentences);
    }

    public Text(String text) {
        assert text != null : "Input text cannot be null";
        this.sentences = new ArrayList<>();
        for (String sentence : text.split("(?<=[.!?])")) {
            sentence = sentence.trim();
            assert !sentence.isEmpty() : "Sentences cannot be empty";
            this.sentences.add(sentence);
        }
    }

    public void addSentence(String sentence) {
        assert sentence != null : "Sentence cannot be null";
        assert !sentence.isEmpty() : "Sentence cannot be empty";
        assert sentence.matches(".*[.!?]$") : "Sentence must end with a punctuation mark (. ! ?)";
        this.sentences.add(sentence.trim());
    }

    public void removeSentence(int index) {
        assert index >= 0 && index < sentences.size() : "Index out of bounds";
        sentences.remove(index);
    }

    public void insertSentence(int index, String sentence) {
        assert sentence != null : "Sentence cannot be null";
        assert !sentence.isEmpty() : "Sentence cannot be empty";
        assert sentence.matches(".*[.!?]$") : "Sentence must end with a punctuation mark (. ! ?)";
        assert index >= 0 && index <= sentences.size() : "Index out of bounds";

        sentences.add(index, sentence.trim());
    }

    public int getLetterCount() {
        int count = 0;
        for (String sentence : sentences) {
            for (char c : sentence.toCharArray()) {
                if (Character.isLetter(c)) {
                    count++;
                }
            }
        }
        return count;
    }


    public int getWordCount() {
        int count = 0;
        for (String sentence : sentences) {
            count += sentence.split("\\s+").length;
        }

        return count;
    }

    public int getSentenceCount() {
        return sentences.size();
    }

    public boolean equals(Text other) {
        assert other != null : "Other text cannot be null";
        return this.sentences.equals(other.sentences);
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (String sentence : sentences) {
            result.append(sentence).append(" ");
        }

        return result.toString().trim();
    }
}
