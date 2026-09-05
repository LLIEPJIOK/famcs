import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

import javax.swing.JButton;
import javax.swing.JTextArea;

public class CheckThread extends Thread {
    private final String extension = ".OUT";
    private final JTextArea log;
    private final JButton startButton;
    private final JButton stopButton;
    private final AnswersToBeChecked atbc;
    private final WorkingThread workingThread;
    private boolean isWorking;

    CheckThread(JTextArea _log, JButton start, JButton stop, AnswersToBeChecked atbc, WorkingThread wt) {
        this.log = _log;
        this.startButton = start;
        this.stopButton = stop;
        this.atbc = atbc;
        this.workingThread = wt;
        this.isWorking = true;
    }

    public void stopThread() {
        isWorking = false;
    }

    @Override
    public void run() {
        while (true) {
            Answer answer;
            synchronized (atbc) {
                answer = atbc.takeAnswer();
            }
            if (!isWorking || answer == null && !workingThread.isAlive()) {
                break;
            }
            if (answer != null) {
                try {
                    Scanner scanner = new Scanner(new FileReader(answer.fileName + extension));
                    int n = scanner.nextInt();
                    String name = answer.fileName;
                    name = name.substring(name.lastIndexOf("\\") + 1);
                    if (n != answer.info.size()) {
                        log.append(name + ":wrong size\n");
                        scanner.close();
                        continue;
                    }
                    boolean is_correct = true;
                    for (int i = 0; i < n; ++i) {
                        int from = scanner.nextInt();
                        int to = scanner.nextInt();
                        int dist = scanner.nextInt();
                        ShortestPath path = answer.info.get(i);
                        if (path.from != from || path.vertex != to || path.dist != dist) {
                            log.append(name + ": wrong path\n");
                            scanner.close();
                            is_correct = false;
                            break;
                        }
                    }
                    if (is_correct) {
                        log.append(name + ": correct result\n");
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        startButton.setEnabled(true);
        stopButton.setEnabled(false);
    }
}
