import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedDeque;

public class TaskToBeSolved {
    private Queue<Task> tasks;

    public TaskToBeSolved() {
        this.tasks = new ConcurrentLinkedDeque<>();
    }

    public void addTask(Task task) {
        tasks.add(task);
    }

    public Task takeTask() {
        return tasks.isEmpty() ? null : tasks.remove();
    }
}
