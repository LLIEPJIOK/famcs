import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;
import java.util.Vector;

public class ReadThread extends Thread {
    private final String directoryPath;

    final TaskToBeSolved ttbs;
    private final String extension = ".IN";
    private boolean isWorking;

    public ReadThread(String directoryPath, TaskToBeSolved ttbs) {
        this.directoryPath = directoryPath;
        this.ttbs = ttbs;
        this.isWorking = true;
    }

    public void stopThread() {
        isWorking = false;
    }

    @Override
    public void run() {
        File directory = new File(directoryPath);
        if (directory.exists() && directory.isDirectory()) {
            File[] files = directory.listFiles((name, dir) -> dir.endsWith(extension));
            if (files != null) {
                for (File file : files) {
                    if (!isWorking) {
                        break;
                    }
                    try {
                        Task task = new Task();
                        task.name = file.getAbsolutePath();
                        task.name = task.name.substring(0, task.name.lastIndexOf("."));
                        BufferedReader reader = new BufferedReader(new FileReader(file.getAbsolutePath()));
                        String firstLine = reader.readLine();
                        StringTokenizer tokenizer = new StringTokenizer(firstLine);
                        task.n = Integer.parseInt(tokenizer.nextToken());
                        if (task.n < 2 || task.n > 1e4) {
                            continue;
                        }
                        task.k = Integer.parseInt(tokenizer.nextToken());
                        if (task.k < 1 || task.k > 1e7) {
                            continue;
                        }
                        task.curves = new Vector<>(task.n);
                        boolean flag = false;
                        for (int j = 0; j < task.n; j++) {
                            String curveLine = reader.readLine();
                            StringTokenizer curveTokenizer = new StringTokenizer(curveLine);
                            Vector<Integer> curve = new Vector<>(task.k);
                            for (int k = 0; k < task.n; k++) {
                                curve.add(Integer.parseInt(curveTokenizer.nextToken()));
                                if (curve.lastElement() < 0 || curve.lastElement() > 1e3) {
                                    flag = true;
                                    break;
                                }
                            }
                            if (flag) {
                                break;
                            }
                            task.curves.add(curve);
                        }
                        if (flag || !Files.exists(Path.of(task.name + ".OUT"))) {
                            continue;
                        }
                        synchronized (ttbs) {
                            ttbs.addTask(task);
                        }
                    } catch (IOException e) {
                        System.out.println(e.getMessage());
                    }
                }
            }
        }
    }
}
