import java.util.Scanner;
import java.util.Random;
import java.util.Date;

public class Main {
    public static void main(String args[]) {
        System.out.print("Enter n: ");
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        in.close();
        if (n <= 0) {
            System.err.println("Invalid n value, require n > 0");
            System.exit(1);
        }

        Random rnd = new Random((new Date()).getTime());
        int[][] arr = new int[n][n];
        System.out.println("Source values: ");
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                arr[i][j] = rnd.nextInt(2 * n + 1) - n;
                System.out.print(arr[i][j] + "\t");
            }

            System.out.println();
        }

        int inc = 0, dec = 0;
        boolean is_inc = false, is_dec = false;
        int type = 0;
        for (int i = 1; i < n * n; ++i) {
            if (arr[i / n][i % n] > arr[(i - 1) / n][(i - 1) % n]) {
                is_inc = true;
                inc += arr[i / n][i % n];
                if (type != 1) {
                    type = 1;
                    inc += arr[(i - 1) / n][(i - 1) % n];
                }
            } else if (arr[i / n][i % n] < arr[(i - 1) / n][(i - 1) % n]) {
                is_dec = true;
                dec += arr[i / n][i % n];
                if (type != -1) {
                    type = -1;
                    dec += arr[(i - 1) / n][(i - 1) % n];
                }
            } else {
                type = 0;
            }
        }

        System.out.println();
        if (!is_inc && !is_dec) {
            System.out.println("All elements are equal");
        } else if (!is_inc) {
            System.out.println("No increasing field");
        } else if (!is_dec) {
            System.out.println("No decreasing field");
        } else {
            System.out.println("Difference is " + (inc - dec));
        }
    }
}
