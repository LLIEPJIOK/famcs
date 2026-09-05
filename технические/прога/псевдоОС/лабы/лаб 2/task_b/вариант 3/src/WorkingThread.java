import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class WorkingThread extends Thread {
    private final String extension = ".ANSWER";

    static class Path implements Comparable<Path> {
        int vertex;
        int dist;

        Path(int vertex, int dist) {
            this.vertex = vertex;
            this.dist = dist;
        }

        @Override
        public int compareTo(Path another) {
            return Integer.compare(dist, another.dist);
        }
    }

    private final TaskToBeSolved ttbs;
    private final AnswersToBeChecked atbc;
    private final ReadThread readThread;

    private List<ShortestPath> shortestPaths;

    private boolean isWorking;

    public WorkingThread(TaskToBeSolved ttbs, AnswersToBeChecked atbc, ReadThread rt) {
        this.ttbs = ttbs;
        this.atbc = atbc;
        this.readThread = rt;
        isWorking = true;
    }

    private void dijkstra(Task task, int from) {
        PriorityQueue<Path> pq = new PriorityQueue<>();
        boolean[] vis = new boolean[task.n];
        pq.add(new Path(from, 0));
        while (!pq.isEmpty()) {
            Path curPath = pq.remove();
            if (curPath.dist > task.k) {
                break;
            }
            if (vis[curPath.vertex]) {
                continue;
            }
            if (curPath.dist != 0) {
                shortestPaths.add(new ShortestPath(from + 1, curPath.vertex + 1, curPath.dist));
            }
            vis[curPath.vertex] = true;
            for (int i = 0; i < task.n; ++i) {
                if (!vis[i] && task.curves.elementAt(curPath.vertex).elementAt(i) != 0) {
                    pq.add(new Path(i, curPath.dist + task.curves.elementAt(curPath.vertex).elementAt(i)));
                }
            }
        }
    }

    public void stopThread() {
        isWorking = false;
    }

    @Override
    public void run() {
        while (isWorking) {
            Task task;
            synchronized (ttbs) {
                task = ttbs.takeTask();
            }
            if (task == null && !readThread.isAlive()) {
                break;
            }
            if (task != null) {
                shortestPaths = new ArrayList<>();
                for (int i = 0; i < task.n; ++i) {
                    dijkstra(task, i);
                }
                try {
                    Writer writer = new FileWriter(task.name + extension);
                    writer.write(shortestPaths.size() + "\n");
                    for (ShortestPath shortestPath : shortestPaths) {
                        writer.write(shortestPath + "\n");
                    }
                    writer.close();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                synchronized (atbc) {
                    atbc.addAnswer(new Answer(task.name, shortestPaths));
                }
            }
        }
    }
}
