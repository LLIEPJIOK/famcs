import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedDeque;

public class AnswersToBeChecked {
    Queue<Answer> answers;

    public AnswersToBeChecked() {
        this.answers = new ConcurrentLinkedDeque<>();
    }

    public void addAnswer(Answer answer) {
        answers.add(answer);
    }

    public Answer takeAnswer() {
        return answers.poll();
    }
}
