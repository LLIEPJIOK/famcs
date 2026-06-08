package main;

import java.util.ArrayList;
import java.util.List;

public class Text {
    private final String letters =  "qwertyuiopasdfghjklzxcvbnm" +
                                    "QWERTYUIOPASDFGHJKLZXCVBNM" +
                                    "йцукенгшщзхъфывапролджэячсмитьбю" +
                                    "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ";
    private final List<String> sentences;

    public Text() {
        this.sentences = new ArrayList<>();
    }

    public Text(String sentence) {
        assert (sentence != null);
        this.sentences = new ArrayList<>();
        String tmp = sentence.replaceAll("\\s+", " ").trim();
        if (!tmp.isEmpty()) {
            this.sentences.add(tmp);
        }
    }

    public Text(List<String> sentences) {
        this.sentences = new ArrayList<>();
        for (String sentence : sentences) {
            String tmp = sentence.replaceAll("\\s+", " ").trim();
            if (!tmp.isEmpty()) {
                this.sentences.add(tmp);
            }
        }
    }

    public void addSentence(String sentence) {
        String tmp = sentence.replaceAll("\\s+", " ").trim();
        if (!tmp.isEmpty()) {
            this.sentences.add(tmp);
        }
    }

    public void removeSentence(int index) {
        assert (index >= 0 && index < sentences.size());
        sentences.remove(index);
    }

    public void insertSentence(int index, String sentence) {
        assert (index >= 0 && index <= sentences.size());
        String tmp = sentence.replaceAll("\\s+", " ").trim();
        if (!tmp.isEmpty()) {
            this.sentences.add(index, tmp);
        }
    }

    public int getLetterCount() {
        int count = 0;
        for (String sentence : sentences) {
            for (int i = 0; i < sentence.length(); ++i) {
                if (letters.indexOf(sentence.charAt(i)) != -1) {
                    ++count;
                }
            }
        }
        return count;
    }

    public int getWordCount() {
        int count = 0;
        for (String sentence : sentences) {
            count += sentence.trim().split("\\s+").length;
        }
        return count;
    }

    public int getSentenceCount() {
        return sentences.size();
    }

    public boolean isEqual(Text otherText) {
        return this.toString().equals(otherText.toString());
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
