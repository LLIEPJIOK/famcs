import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        String vowels = "ауыиеёяэоюАУЫИЕЁЯЭОЯ";
        String consonants = "бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ";
        Scanner in = new Scanner( System.in );
        while ( in.hasNextLine() ) {
            String s = in.nextLine();
            int cnt_vowels = 0, cnt_consonants = 0;
            for (int i = 0; i < s.length(); ++i)
            {
                if (vowels.indexOf(s.charAt(i)) != -1)
                {
                    ++cnt_vowels;
                }
                else if (consonants.indexOf(s.charAt(i)) != -1)
                {
                    ++cnt_consonants;
                }
            }

            System.out.println("Количество гласных: " + cnt_vowels);
            System.out.println("Количество согласных: " + cnt_consonants);
        }

        in.close();
    }
}