package main;

import java.util.Collections;
import java.util.Scanner;
import java.util.Vector;

public class Main {
    public static boolean isPalindrome(String word) {
        String cleanedWord = word.toLowerCase();
        StringBuilder reversed = new StringBuilder(cleanedWord).reverse();
        return cleanedWord.equals(reversed.toString());
    }

    public static String[] splitNonWords(String input) {
        String regex = "[a-zA-Z]+";
        String[] words = input.split(regex);
        return words;
    }

    public static String[] splitWords(String input) {
        String regex = "[^(a-zA-Z)]+";
        String[] nonWords = input.split(regex);
        return nonWords;
    }

    private static void replacePalindromes(String[] words, Vector<String> palindromes) {
        int j = 0;
        for (int i = 0; i < words.length; ++i) {
            if (isPalindrome(words[i])) {
                words[i] = palindromes.elementAt(j);
                ++j;
            }
        }
    }


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] words;
        String[] splitters;
        Vector<String> palindromes = new Vector<>();
        String output = "";
        Vector<String> out = new Vector<>();
        String line;
        while (scanner.hasNextLine()) {
            line = scanner.nextLine();
            splitters = splitNonWords(line);
            words = splitWords(line);
            for (String a : words) {
                if (isPalindrome(a)) {
                    palindromes.add(a);
                }
            }
            if (palindromes.isEmpty()) {
                output = line;
            } else {
                Collections.sort(palindromes);
                replacePalindromes(words, palindromes);
                int i = 0, j = 0;
                while (i < words.length && j < splitters.length) {
                    output += splitters[j++];
                    output += (words[i++]);
                }
                if (j < splitters.length) {
                    output += splitters[j++];
                }
                if (i < words.length) {
                    output += words[i++];
                }

            }
            out.add(output);
            output = "";
            palindromes.clear();
        }
        for (String s : out) {
            System.out.println(s);
        }
        scanner.close();
    }
}
